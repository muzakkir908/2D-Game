// Clicks through every link in the HTML prototype and reports the result.
// Run from the project folder:  node tools/test_prototype.js
// Needs Playwright with Chromium.
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const file = 'file://' + path.resolve(__dirname, '..', '04_UI_and_Prototype', 'prototype', 'index.html');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('requestfailed', r => errors.push('failed to load ' + r.url()));
  await page.goto(file);
  await page.waitForTimeout(300);

  const results = [];
  const where = () => page.evaluate(() => location.hash);
  async function step(name, label, expected) {
    await page.click(`button[aria-label="${label}"]`);
    await page.waitForTimeout(150);
    const got = await where();
    results.push({ name, ok: got === expected, got });
  }
  results.push({ name: 'Starts on Main Menu', ok: (await where()) === '#menu', got: await where() });
  await step('Main Menu -> PLAY -> Gameplay', 'Play', '#game');
  await step('Gameplay -> door -> Victory', 'Go into the door', '#win');
  await step('Victory -> REPLAY -> Gameplay', 'Replay', '#game');
  await step('Gameplay -> moth 1 -> Game Over', 'Touch moth 1', '#lose');
  await step('Game Over -> RETRY -> Gameplay', 'Retry', '#game');
  await step('Gameplay -> moth 2 -> Game Over', 'Touch moth 2', '#lose');
  await step('Game Over -> MAIN MENU -> Main Menu', 'Main menu', '#menu');
  for (const s of ['Touch spikes 1', 'Touch spikes 2', 'Touch spikes 3']) {
    await step('Main Menu -> PLAY', 'Play', '#game');
    await step(`Gameplay -> ${s.replace('Touch ', '')} -> Game Over`, s, '#lose');
    await step('Game Over -> MAIN MENU', 'Main menu', '#menu');
  }
  await step('Main Menu -> PLAY', 'Play', '#game');
  await step('Gameplay -> door -> Victory', 'Go into the door', '#win');
  await step('Victory -> MAIN MENU -> Main Menu', 'Main menu', '#menu');
  await page.click('button[aria-label="Settings"]');
  results.push({ name: 'SETTINGS shows a message', ok: await page.isVisible('.msg') });
  await page.click('.msg button');
  await page.click('button[aria-label="Exit"]');
  results.push({ name: 'EXIT shows a message', ok: await page.isVisible('.msg') });
  await page.click('.msg button');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(150);
  results.push({ name: 'Enter key on Main Menu -> Gameplay', ok: (await where()) === '#game' });
  await page.keyboard.press('Escape');
  await page.waitForTimeout(150);
  results.push({ name: 'Esc key -> Main Menu', ok: (await where()) === '#menu' });
  const imgsOk = await page.evaluate(() => [...document.images].every(i => i.complete && i.naturalWidth > 0));
  results.push({ name: 'All images on the page loaded', ok: imgsOk });
  await page.setViewportSize({ width: 400, height: 900 });
  await page.waitForTimeout(150);
  const sw = await page.evaluate(() => document.documentElement.scrollWidth);
  results.push({ name: 'No sideways scrolling at phone width (400 px)', ok: sw <= 400, got: sw });
  results.push({ name: 'No errors in the browser console', ok: errors.length === 0, got: errors.join('; ') });

  for (const r of results) console.log((r.ok ? 'PASS  ' : 'FAIL  ') + r.name + (r.ok || r.got === undefined ? '' : `  (got ${r.got})`));
  const failed = results.filter(r => !r.ok).length;
  console.log(`\n${results.length - failed} of ${results.length} prototype checks passed.`);
  await browser.close();
  process.exit(failed ? 1 : 0);
})();
