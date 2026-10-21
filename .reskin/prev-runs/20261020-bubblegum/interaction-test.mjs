#!/usr/bin/env node
/** Functional click-through for the reskinned shell (supplementary evidence). */
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const OUT = path.dirname(fileURLToPath(import.meta.url));
const req = createRequire(path.join(OUT, 'tools', 'package.json'));
const { chromium } = req('playwright-core');
const CHROME = 'C:\\Users\\Administrator\\AppData\\Local\\ms-playwright\\chromium-1247\\chrome-win64\\chrome.exe';
const BASE = process.argv[2] || 'http://127.0.0.1:4380/';

const results = [];
function check(name, ok, detail = '') {
  results.push({ name, ok, detail });
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? ` — ${detail}` : ''}`);
}

const browser = await chromium.launch({ headless: true, executablePath: CHROME, args: ['--no-sandbox', '--hide-scrollbars'] });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
const errors = [];
page.on('pageerror', (e) => errors.push(String(e.message || e)));
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });

try {
  await page.goto(`${BASE}#home`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(700);

  // Rail navigation via real anchors
  await page.click('a.ax-rail-item[href="#quests"]');
  await page.waitForTimeout(500);
  check('rail link navigates to quests', await page.locator('h1', { hasText: 'Find your' }).count() === 1);
  check('hash updated to #quests', new URL(page.url()).hash === '#quests', page.url());

  // Search filter
  const input = page.locator('input[type="search"]');
  await input.fill('zzz');
  await page.waitForTimeout(200);
  check('search filters to empty state', await page.locator('.ax-empty-title').innerText().then((t) => t.includes('No matching quests')));
  const clearBtn = page.locator('button:has-text("Clear filters")');
  check('empty state offers clear filters', await clearBtn.count() === 1);
  await clearBtn.first().click();
  await page.waitForTimeout(400);
  const pressed = await page.$$eval('.ax-chip', (els) => els.map((e) => ({ t: e.textContent.trim(), p: e.getAttribute('aria-pressed') })));
  check('clear filters restores the full filter', pressed.find((p) => p.p === 'true')?.t === 'all', JSON.stringify(pressed));

  // Filter chips
  const chips = page.locator('.ax-chip');
  const chipCount = await chips.count();
  check('filter chips render', chipCount >= 1, `${chipCount} chips`);
  if (chipCount > 1) {
    await chips.nth(1).click();
    await page.waitForTimeout(200);
    check('chip toggles aria-pressed', await chips.nth(1).getAttribute('aria-pressed') === 'true');
  }

  // Governance: compose disclosure
  await page.click('a.ax-rail-item[href="#governance"]');
  await page.waitForTimeout(500);
  const toggle = page.locator('#compose-toggle');
  await toggle.click();
  await page.waitForTimeout(300);
  check('compose editor opens', await page.locator('#compose-editor').count() === 1);
  const area = page.locator('#proposal-description');
  await area.fill('A proposal about the seasonal research budget.');
  await page.waitForTimeout(250);
  check('proposal counter updates', await page.locator('.ax-form-note').first().innerText().then((t) => t.includes('46') || t.includes('45') || t.includes('47')));
  await page.click('button:has-text("Clear")');
  await page.waitForTimeout(250);
  check('clear shows undo', await page.locator('button:has-text("Undo clear")').count() === 1);
  await page.click('button:has-text("Undo clear")');
  await page.waitForTimeout(250);
  check('undo restores draft', (await area.inputValue()).includes('seasonal research'));
  await page.click('button:has-text("Keep draft")');
  await page.waitForTimeout(300);
  const notes = await page.$$eval('.ax-sheet-note', (els) => els.map((e) => e.textContent.replace(/\s+/g, ' ').trim()));
  check('draft saved indicator', notes[0] === 'draft saved', JSON.stringify(notes));
  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);
  check('escape closes editor', await page.locator('#compose-editor').count() === 0);

  // Drawer
  await page.click('button[aria-controls="ax-drawer"]');
  await page.waitForTimeout(400);
  check('drawer opens', await page.locator('#ax-drawer').count() === 1);
  check('drawer lists sections', await page.locator('#ax-drawer .ax-drawer-link').count() === 6);
  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);
  check('escape closes drawer', await page.locator('#ax-drawer').count() === 0);

  // Wallet connect: no extension in this browser, so the app must answer with
  // its own sheet, an injected wallet modal, or a status toast.
  await page.click('.ax-command-inner button.ax-btn');
  await page.waitForTimeout(1200);
  const surfaced = (await page.locator('.ax-toast').count()) + (await page.locator('.ax-wallets').count()) + (await page.locator('mm-install-modal').count());
  check('wallet action opens a wallet surface', surfaced > 0, `surfaces=${surfaced}`);
  await page.evaluate(() => document.querySelectorAll('mm-install-modal').forEach((el) => el.remove()));
  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);
  const dismiss = page.locator('.ax-toast-close');
  if (await dismiss.count()) {
    await dismiss.click();
    await page.waitForTimeout(300);
    check('toast dismisses', await page.locator('.ax-toast').count() === 0);
  } else {
    check('wallet surface closes', await page.locator('.ax-wallets').count() === 0);
  }

  // FAQ disclosure
  await page.click('a.ax-rail-item[href="#learn"]');
  await page.waitForTimeout(500);
  const second = page.locator('.ax-faq-item').nth(1);
  const summary = second.locator('summary');
  await summary.click();
  await page.waitForTimeout(250);
  check('faq item opens', await second.evaluate((el) => el.open === true));
  await summary.click();
  await page.waitForTimeout(250);
  check('faq item closes', await second.evaluate((el) => el.open === false));

  // Footer navigation
  await page.click('.ax-status-links button:has-text("Treasury")');
  await page.waitForTimeout(500);
  check('footer link navigates', await page.locator('h1', { hasText: 'Nothing hidden' }).count() === 1);

  // Mobile: rail strip reachable + drawer
  await page.setViewportSize({ width: 390, height: 844 });
  await page.waitForTimeout(400);
  const railLinks = await page.$$eval('a.ax-rail-item', (els) => els.filter((el) => {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden';
  }).length);
  check('mobile rail exposes all routes', railLinks === 6, `${railLinks} visible`);
  await page.locator('a.ax-rail-item[href="#stake"]').scrollIntoViewIfNeeded();
  await page.click('a.ax-rail-item[href="#stake"]');
  await page.waitForTimeout(500);
  check('mobile rail navigates', await page.locator('h1', { hasText: 'No token is' }).count() === 1);
  await page.click('button[aria-controls="ax-drawer"]');
  await page.waitForTimeout(400);
  check('mobile drawer opens', await page.locator('#ax-drawer').count() === 1);
  await page.keyboard.press('Escape');

  check('no console/page errors during clicks', errors.filter((e) => !/favicon|Vue Devtools/i.test(e)).length === 0, errors.slice(0, 3).join(' | '));
} finally {
  await browser.close().catch(() => {});
}

const failed = results.filter((r) => !r.ok);
console.log(`\n${failed.length ? 'FUNCTIONAL TEST: FAIL' : 'FUNCTIONAL TEST: PASS'} (${results.length - failed.length}/${results.length})`);
if (failed.length) process.exitCode = 1;
