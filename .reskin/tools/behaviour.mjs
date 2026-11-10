/**
 * Behavioural smoke test for the reskinned shell: navigation, drawer, compose
 * editor, filters and keyboard focus must still work after the rebuild.
 */
import path from 'node:path';
import { provisionBrowser } from 'file:///C:/Users/Administrator/.dsh/skills/reskin/scripts/lib/browser.mjs';

const BASE = process.env.PREVIEW_URL || 'http://127.0.0.1:4599/';
const { playwright, executablePath } = await provisionBrowser(process.cwd(), path.resolve(process.cwd(), '.reskin'));
const browser = await playwright.chromium.launch({ executablePath, headless: true });
const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await context.newPage();
const fails = [];
const ok = (label, cond, extra = '') => {
  if (cond) console.log(`  pass  ${label}`);
  else {
    console.log(`  FAIL  ${label} ${extra}`);
    fails.push(label);
  }
};

await page.goto(`${BASE}#home`, { waitUntil: 'load' });
await page.waitForTimeout(700);

/* navigation through the orbit nodes */
await page.locator('.orb-index a[href="#treasury"]').click();
await page.waitForTimeout(400);
ok('orbit node navigates', (await page.evaluate(() => location.hash)) === '#treasury');
ok('treasury view rendered', await page.locator('.orb-canvas--treasury').isVisible());
ok('active node marked', (await page.locator('.orb-index [aria-current="page"]').innerText()).includes('Treasury'));

/* drawer */
await page.locator('.orb-dock button[aria-controls="ax-drawer"]').click();
await page.waitForTimeout(300);
ok('drawer opens', await page.locator('#ax-drawer').isVisible());
ok('drawer lists six routes', (await page.locator('#ax-drawer .orb-drawer-link').count()) === 6);
await page.locator('#ax-drawer .orb-drawer-link', { hasText: 'Guide' }).click();
await page.waitForTimeout(400);
ok('drawer navigates and closes', (await page.evaluate(() => location.hash)) === '#learn' && !(await page.locator('#ax-drawer').count()));
ok('learn view rendered', await page.locator('.orb-canvas--learn').isVisible());

/* faq accordion */
const faq = page.locator('.orb-faq-item').nth(1);
await faq.locator('summary').click();
await page.waitForTimeout(200);
ok('faq toggles open', await faq.evaluate((el) => el.open));

/* compose editor */
await page.goto(`${BASE}#governance`, { waitUntil: 'load' });
await page.waitForTimeout(500);
await page.locator('#compose-toggle').click();
await page.waitForTimeout(300);
ok('compose editor opens', await page.locator('#proposal-description').isVisible());
ok('compose focus lands in textarea', await page.evaluate(() => document.activeElement?.id === 'proposal-description'));
ok('submit disabled while short', await page.locator('form#compose-editor button[type="submit"]').isDisabled());
await page.keyboard.type('Adopt a treasury reporting window');
await page.waitForTimeout(300);
ok('submit enabled with text', !(await page.locator('form#compose-editor button[type="submit"]').isDisabled()));
await page.keyboard.press('Escape');
await page.waitForTimeout(250);
ok('escape closes editor', !(await page.locator('#proposal-description').count()));

/* quest filters */
await page.goto(`${BASE}#quests`, { waitUntil: 'load' });
await page.waitForTimeout(500);
const before = await page.locator('.orb-entry').count();
await page.locator('.orb-search-field').fill('treasury');
await page.waitForTimeout(400);
const after = await page.locator('.orb-entry').count();
ok('search filters rows', after < before || after === 0, `(${before} -> ${after})`);
await page.locator('.orb-search-field').fill('');
await page.locator('.orb-chip', { hasText: 'Open' }).click();
await page.waitForTimeout(300);
ok('status chip pressed', (await page.locator('.orb-chip[aria-pressed="true"]').innerText()).trim().toLowerCase() === 'open');

/* keyboard focus visibility on the orbit nav */
await page.goto(`${BASE}#home`, { waitUntil: 'load' });
await page.waitForTimeout(500);
let focused = null;
for (let i = 0; i < 8; i += 1) {
  await page.keyboard.press('Tab');
  focused = await page.evaluate(() => {
    const el = document.activeElement;
    if (!el || el === document.body) return null;
    const cs = getComputedStyle(el);
    return {
      tag: el.tagName,
      cls: el.className,
      outline: `${cs.outlineStyle} ${cs.outlineWidth} ${cs.outlineColor}`,
      shadow: cs.boxShadow,
    };
  });
  if (focused && focused.tag === 'A' && String(focused.cls).includes('orb-node-link')) break;
}
ok(
  'orbit node focus is visible',
  Boolean(focused && /solid/.test(focused.outline) && parseFloat(focused.outline.split(' ')[1]) > 0),
  JSON.stringify(focused),
);

await browser.close();
if (fails.length) {
  console.log(`\n${fails.length} behaviour check(s) failed`);
  process.exitCode = 1;
} else {
  console.log('\nall behaviour checks passed');
}
