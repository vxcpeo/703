/**
 * Visual capture loop for the reskin: all six hash views, desktop + mobile.
 * Usage: node .reskin/tools/shots.mjs [label]
 * Expects a preview server on http://127.0.0.1:4317/
 */
import path from 'node:path';
import fs from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { provisionBrowser } from 'file:///C:/Users/Administrator/.dsh/skills/reskin/scripts/lib/browser.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const PROJECT = path.resolve(HERE, '..', '..');
const OUT = path.resolve(PROJECT, '.reskin', 'views');
const label = process.argv[2] || 'now';
const BASE = process.env.PREVIEW_URL || 'http://127.0.0.1:4317/';

const VIEWS = ['home', 'quests', 'governance', 'treasury', 'stake', 'learn'];
const VIEWPORTS = [
  { id: 'desktop', width: 1440, height: 900 },
  { id: 'mobile', width: 390, height: 844 },
];

const { playwright, executablePath } = await provisionBrowser(PROJECT, path.resolve(PROJECT, '.reskin'));
const browser = await playwright.chromium.launch({ executablePath, headless: true });
await fs.mkdir(OUT, { recursive: true });

const errors = [];
for (const viewport of VIEWPORTS) {
  const context = await browser.newContext({
    viewport: { width: viewport.width, height: viewport.height },
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();
  page.on('console', (msg) => {
    if (msg.type() === 'error') errors.push(`${viewport.id} console: ${msg.text()}`);
  });
  page.on('pageerror', (err) => errors.push(`${viewport.id} pageerror: ${err.message}`));
  for (const view of VIEWS) {
    await page.goto(`${BASE}#${view}`, { waitUntil: 'load' });
    await page.waitForTimeout(900);
    const overflow = await page.evaluate(() => ({
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
    }));
    if (overflow.scrollWidth > overflow.clientWidth + 1) {
      errors.push(`${viewport.id} ${view}: horizontal overflow ${overflow.scrollWidth} > ${overflow.clientWidth}`);
    }
    await page.screenshot({
      path: path.join(OUT, `${label}-${view}-${viewport.id}.png`),
      fullPage: true,
    });
  }
  await context.close();
}
await browser.close();
console.log(`captured ${VIEWS.length * VIEWPORTS.length} shots into .reskin/views/`);
console.log(errors.length ? `PROBLEMS:\n${errors.join('\n')}` : 'no console errors, no horizontal overflow');
