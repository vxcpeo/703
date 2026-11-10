/**
 * Captures the real product surfaces used by the X cards.
 * Output: website/.reskin/views/ps-*.png
 *
 * Viewport screenshots only: element screenshots of tall nodes mis-stitch under
 * the app's clip context, and a scrolled viewport is exactly what a person sees.
 */
import path from 'node:path';
import fs from 'node:fs/promises';
import { provisionBrowser } from 'file:///C:/Users/Administrator/.dsh/skills/reskin/scripts/lib/browser.mjs';

const BASE = process.env.PREVIEW_URL || 'http://127.0.0.1:4599/';
const OUT = path.resolve('.reskin', 'views');
const { playwright, executablePath } = await provisionBrowser(process.cwd(), path.resolve('.reskin'));
const browser = await playwright.chromium.launch({ executablePath, headless: true });
await fs.mkdir(OUT, { recursive: true });

async function run({ width, height, pairs }) {
  const context = await browser.newContext({
    viewport: { width, height },
    deviceScaleFactor: 2,
  });
  const page = await context.newPage();
  await page.addInitScript(() => {
    const hide = () => {
      const style = document.createElement('style');
      style.textContent = '.orb-dock{display:none !important}';
      document.head.appendChild(style);
    };
    if (document.head) hide();
    else document.addEventListener('DOMContentLoaded', hide, { once: true });
  });
  for (const [view, scrollTo, file] of pairs) {
    await page.goto(`${BASE}#${view}`, { waitUntil: 'load' });
    await page.waitForTimeout(1200);
    if (scrollTo) {
      await page.evaluate((sel) => {
        const el = document.querySelector(sel);
        if (el) window.scrollTo(0, el.getBoundingClientRect().top + window.scrollY);
      }, scrollTo);
      await page.waitForTimeout(500);
    }
    await page.screenshot({ path: path.join(OUT, file), fullPage: false });
    console.log(`captured ${file}`);
  }
  await context.close();
}

await run({
  width: 1600,
  height: 900,
  pairs: [
    ['home', null, 'ps-home.png'],
    ['treasury', '#main', 'ps-treasury-panel.png'],
  ],
});

await run({
  width: 1200,
  height: 1200,
  pairs: [['home', null, 'ps-home-square.png']],
});

await run({
  width: 760,
  height: 1400,
  pairs: [
    ['quests', '#main', 'ps-quests-panel.png'],
    ['governance', '#main', 'ps-governance-panel.png'],
    ['learn', '#main', 'ps-learn-panel.png'],
  ],
});

await run({
  width: 420,
  height: 1000,
  pairs: [
    ['quests', '#main', 'ps-quests-mobile.png'],
    ['governance', '#main', 'ps-governance-mobile.png'],
    ['learn', '#main', 'ps-learn-mobile.png'],
  ],
});

await browser.close();
