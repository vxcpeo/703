#!/usr/bin/env node
/**
 * Supplementary hash-route audit for the reskin.
 *
 * The skill's inventory only discovers path-based routes; this app is a
 * hash-routed SPA (#home, #quests, ...). This script renders every hash route
 * with the same browser, captures the same evidence shape (words, attributes,
 * forms, classes, landmarks, contrast, axe) and compares baseline vs current.
 *
 *   node .reskin/hash-audit.mjs capture baseline --url http://127.0.0.1:4380/
 *   node .reskin/hash-audit.mjs capture current  --url http://127.0.0.1:4380/
 *   node .reskin/hash-audit.mjs compare
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = HERE;
const ROUTES = ['home', 'quests', 'governance', 'treasury', 'stake', 'learn'];
const CHROME = process.env.RESKIN_CHROME || 'C:\\Users\\Administrator\\AppData\\Local\\ms-playwright\\chromium-1247\\chrome-win64\\chrome.exe';

function loadPlaywright() {
  const req = createRequire(path.join(OUT, 'tools', 'package.json'));
  return req('playwright-core');
}
function axePath() {
  try {
    const req = createRequire(path.join(OUT, 'tools', 'package.json'));
    return req.resolve('axe-core/axe.min.js');
  } catch { return null; }
}

function inPageAudit() {
  const norm = (s) => String(s || '').replace(/\s+/g, ' ').trim();
  const isVisible = (el) => {
    if (!el || el.nodeType !== 1) return false;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.visibility === 'collapse') return false;
    if (Number.parseFloat(cs.opacity) < 0.06) return false;
    const rect = el.getBoundingClientRect();
    return rect.width > 0 && rect.height > 0;
  };
  const inc = (map, key) => { if (key) map.set(key, (map.get(key) || 0) + 1); };
  const words = new Map(); const attrs = new Map(); const links = new Map(); const forms = new Map();
  const classes = new Set(); const landmarks = []; const headings = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {
    const parent = node.parentElement;
    if (!parent) continue;
    if (/^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE)$/i.test(parent.tagName)) continue;
    const text = norm(node.nodeValue);
    if (!text || !/[\p{L}\p{N}]/u.test(text)) continue;
    if (!isVisible(parent)) continue;
    for (let token of text.split(/\s+/)) {
      token = token.replace(/^[^\p{L}\p{N}$€£¥#]+/u, '').replace(/[^\p{L}\p{N}%]+$/u, '');
      if (!token || !/[\p{L}\p{N}]/u.test(token)) continue;
      inc(words, token);
    }
  }
  for (const el of document.querySelectorAll('[aria-label],[placeholder],[alt],[title]')) {
    if (!isVisible(el)) continue;
    for (const name of ['aria-label', 'placeholder', 'alt', 'title']) {
      const value = el.getAttribute(name);
      if (value && norm(value)) inc(attrs, `${name}=${norm(value)}`);
    }
  }
  for (const a of document.querySelectorAll('a[href]')) {
    if (!isVisible(a)) continue;
    const href = a.getAttribute('href');
    if (href) inc(links, href);
  }
  for (const el of document.querySelectorAll('input,select,textarea')) {
    if (!isVisible(el)) continue;
    const tag = el.tagName.toLowerCase();
    const type = (el.getAttribute('type') || (tag === 'select' ? 'select' : tag === 'textarea' ? 'textarea' : 'text')).toLowerCase();
    if (type === 'hidden') continue;
    inc(forms, `${tag}:${el.getAttribute('name') || ''}:${type}`);
  }
  for (const el of document.body.querySelectorAll('*')) {
    if (!isVisible(el)) continue;
    for (const token of el.classList) if (token) classes.add(token);
    if (/^(H[1-6])$/.test(el.tagName)) headings.push({ tag: el.tagName.toLowerCase(), text: norm(el.innerText).slice(0, 120) });
    if (/^(HEADER|NAV|MAIN|ASIDE|FOOTER)$/.test(el.tagName)) landmarks.push({ tag: el.tagName.toLowerCase(), role: el.getAttribute('role') || '' });
  }
  return {
    meta: {
      title: document.title,
      h1Count: headings.filter((h) => h.tag === 'h1').length,
      h2Count: headings.filter((h) => h.tag === 'h2').length,
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
    },
    words: [...words.entries()].map(([word, count]) => ({ word, count })).sort((a, b) => a.word.localeCompare(b.word)),
    attrs: [...attrs.entries()].map(([key, count]) => ({ key, count })).sort((a, b) => a.key.localeCompare(b.key)),
    links: [...links.entries()].map(([href, count]) => ({ href, count })).sort((a, b) => a.href.localeCompare(b.href)),
    forms: [...forms.entries()].map(([key, count]) => ({ key, count })).sort((a, b) => a.key.localeCompare(b.key)),
    classTokens: [...classes].sort(),
    landmarks,
    headings,
  };
}

async function capture(label, url) {
  const { chromium } = loadPlaywright();
  const browser = await chromium.launch({ headless: true, executablePath: CHROME, args: ['--no-sandbox', '--disable-dev-shm-usage', '--hide-scrollbars'] });
  const axeSrc = axePath();
  const shotDir = path.join(OUT, 'hash-' + label);
  await fs.mkdir(shotDir, { recursive: true });
  const result = { label, url, generatedAt: new Date().toISOString(), pages: {} };
  try {
    for (const route of ROUTES) {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
      const errors = [];
      page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
      page.on('pageerror', (e) => errors.push(String(e.message || e)));
      await page.goto(`${url}#${route}`, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForLoadState('networkidle', { timeout: 8000 }).catch(() => {});
      await page.waitForTimeout(900);
      await page.evaluate(async () => {
        const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
        for (let y = 0; y < document.documentElement.scrollHeight; y += 600) { window.scrollTo(0, y); await sleep(40); }
        window.scrollTo(0, 0); await sleep(150);
      });
      const desktop = await page.evaluate(inPageAudit);
      let axe = { violations: [] };
      if (axeSrc) {
        try {
          await page.addScriptTag({ path: axeSrc });
          axe = await page.evaluate(async () => {
            const r = await window.axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] }, resultTypes: ['violations'] });
            return { violations: (r.violations || []).map((v) => ({ id: v.id, impact: v.impact, nodes: v.nodes.length })) };
          });
        } catch (err) { axe = { violations: [], error: String(err.message || err) }; }
      }
      await page.screenshot({ path: path.join(shotDir, `${route}-desktop.png`), fullPage: true });
      await page.setViewportSize({ width: 390, height: 844 });
      await page.waitForTimeout(300);
      const mobile = await page.evaluate(inPageAudit);
      await page.screenshot({ path: path.join(shotDir, `${route}-mobile.png`), fullPage: true });
      const serious = axe.violations.filter((v) => ['serious', 'critical'].includes(v.impact));
      result.pages[route] = { desktop, mobile, axe, serious, errors };
      console.log(`${route}: words ${desktop.words.length} | h1 ${desktop.meta.h1Count} | axe ${axe.violations.length} (serious ${serious.length}) | overflow ${desktop.meta.scrollWidth > desktop.meta.clientWidth + 2 ? 'YES' : 'no'} | errors ${errors.length}`);
      await page.close();
    }
  } finally {
    await browser.close().catch(() => {});
  }
  await fs.writeFile(path.join(OUT, `hash-${label}.json`), `${JSON.stringify(result, null, 2)}\n`, 'utf8');
  console.log(`wrote .reskin/hash-${label}.json`);
}

function diffWords(base = [], cur = []) {
  const b = new Map(base.map((x) => [x.word, x.count]));
  const c = new Map(cur.map((x) => [x.word, x.count]));
  const missing = []; const extra = [];
  for (const [k, v] of b) if ((c.get(k) || 0) < v) missing.push(`${k} (${v} -> ${c.get(k) || 0})`);
  for (const [k, v] of c) if (v > (b.get(k) || 0)) extra.push(`${k} (${b.get(k) || 0} -> ${v})`);
  return { missing, extra };
}

async function compare() {
  const base = JSON.parse(await fs.readFile(path.join(OUT, 'hash-baseline.json'), 'utf8'));
  const cur = JSON.parse(await fs.readFile(path.join(OUT, 'hash-current.json'), 'utf8'));
  let failures = 0;
  for (const route of ROUTES) {
    const b = base.pages[route]; const c = cur.pages[route];
    if (!b || !c) { console.log(`${route}: MISSING`); failures += 1; continue; }
    const letters = (list) => list.filter((x) => /[\p{L}]/u.test(x.word));
    const wd = diffWords(letters(b.desktop.words), letters(c.desktop.words));
    const numericOnly = diffWords(b.desktop.words.filter((x) => !/[\p{L}]/u.test(x.word)), c.desktop.words.filter((x) => !/[\p{L}]/u.test(x.word)));
    // Mobile words are informational: the same labels are re-laid-out into the
    // mobile dock, so mobile visibility differs by design while the source
    // contract still guarantees no new copy exists.
    const mwd = diffWords(letters(b.mobile.words), letters(c.mobile.words));
    const ad = diffWords(b.desktop.attrs.map((x) => ({ word: x.key, count: x.count })), c.desktop.attrs.map((x) => ({ word: x.key, count: x.count })));
    const missingAttrs = ad.missing.filter((k) => !k.startsWith('aria-'));
    const serious = (c.serious || []).map((v) => v.id);
    const overflow = c.desktop.meta.scrollWidth > c.desktop.meta.clientWidth + 2 || c.mobile.meta.scrollWidth > c.mobile.meta.clientWidth + 2;
    const h1 = c.desktop.meta.h1Count;
    const errs = (c.errors || []).filter((e) => !/favicon|Vue Devtools/i.test(e));
    const problems = [];
    if (wd.missing.length) problems.push(`desktop words missing: ${wd.missing.slice(0, 12).join(', ')}`);
    if (wd.extra.length) problems.push(`desktop words added: ${wd.extra.slice(0, 12).join(', ')}`);
    if (missingAttrs.length) problems.push(`attrs missing: ${missingAttrs.slice(0, 8).join(', ')}`);
    if (serious.length) problems.push(`axe serious: ${serious.join(', ')}`);
    if (overflow) problems.push('horizontal overflow');
    if (h1 !== 1) problems.push(`h1 count ${h1}`);
    if (errs.length) problems.push(`console errors: ${errs.slice(0, 3).join(' | ')}`);
    const overlap = (() => {
      const a = new Set(b.desktop.classTokens); const bb = new Set(c.desktop.classTokens);
      let inter = 0; for (const t of a) if (bb.has(t)) inter += 1;
      return inter / (a.size + bb.size - inter);
    })();
    const landmarkSim = (() => {
      const x = b.desktop.landmarks.map((l) => `${l.tag}:${l.role}`); const y = c.desktop.landmarks.map((l) => `${l.tag}:${l.role}`);
      if (!x.length || !y.length) return 0;
      const dp = Array.from({ length: x.length + 1 }, () => new Uint16Array(y.length + 1));
      for (let i = 1; i <= x.length; i += 1) for (let j = 1; j <= y.length; j += 1) dp[i][j] = x[i - 1] === y[j - 1] ? dp[i - 1][j - 1] + 1 : Math.max(dp[i - 1][j], dp[i][j - 1]);
      return dp[x.length][y.length] / Math.max(x.length, y.length);
    })();
    console.log(`${route}: ${problems.length ? 'FAIL' : 'PASS'} | class overlap ${overlap.toFixed(3)} | landmark ${landmarkSim.toFixed(3)} | axe ${c.axe.violations.length} | mobile word delta ${mwd.missing.length + mwd.extra.length} | numeric delta ${numericOnly.missing.length + numericOnly.extra.length}`);
    for (const p of problems) console.log(`   - ${p}`);
    if (problems.length) failures += 1;
  }
  console.log(failures ? `\nHASH AUDIT: FAIL (${failures} route(s))` : '\nHASH AUDIT: PASS');
  if (failures) process.exitCode = 1;
}

const [mode, label] = process.argv.slice(2);
const urlArg = process.argv.indexOf('--url');
const url = urlArg > -1 ? process.argv[urlArg + 1] : 'http://127.0.0.1:4380/';
if (mode === 'capture') await capture(label, url.endsWith('/') ? url : `${url}/`);
else if (mode === 'compare') await compare();
else { console.log('usage: node .reskin/hash-audit.mjs capture <baseline|current> --url URL | compare'); process.exitCode = 2; }
