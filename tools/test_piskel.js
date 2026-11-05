// Opens every .piskel file in the real Piskel editor, checks it, edits it,
// exports a PNG from Piskel and compares that PNG with the original strip.
//
// Run from the project folder (Piskel must be running at PISKEL_URL):
//   PISKEL_URL=http://127.0.0.1:8765/wicklight_test_index.html node tools/test_piskel.js
// Needs Playwright with Chromium. Evidence is saved in 05_Documentation/piskel_test_evidence/.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const URL = process.env.PISKEL_URL || 'http://127.0.0.1:8765/wicklight_test_index.html';
const OUT = path.join(ROOT, '05_Documentation', 'piskel_test_evidence');
const META = JSON.parse(fs.readFileSync(path.join(ROOT, '02_Pixel_Art_Assets', 'spritesheets', 'spritesheets.json')));
const PALETTE = fs.readFileSync(path.join(ROOT, '02_Pixel_Art_Assets', 'palette', 'wicklight.hex'), 'utf8')
  .trim().split('\n').map(h => h.trim().toLowerCase());
fs.mkdirSync(OUT, { recursive: true });

const results = [];
const rec = (file, name, ok, info) => results.push({ file, name, ok, info });

async function openEditor(page) {
  await page.goto(URL);
  await page.waitForSelector('#drawing-canvas-container canvas', { state: 'attached', timeout: 30000 });
  await page.waitForTimeout(300);
}

async function importPiskel(page, file) {
  await page.click('[data-setting="import"]');
  await page.waitForSelector('.settings-section-import', { state: 'attached' });
  const chooserPromise = page.waitForEvent('filechooser');
  await page.click('.open-piskel-button');
  (await chooserPromise).setFiles(file);
  await page.waitForSelector('.current-step .import-mode', { state: 'attached', timeout: 10000 });
  page.once('dialog', d => d.accept());
  await page.click('.import-mode-replace-button');
  await page.waitForSelector('#dialog-container-wrapper:not(.show)', { state: 'attached', timeout: 10000 });
  await page.waitForTimeout(500);
}

async function exportPng(page, columns, saveAs) {
  await page.click('[data-setting="export"]');
  await page.waitForSelector('.settings-section-export', { state: 'attached' });
  await page.click('[data-test-id="export-tab-png"]');
  await page.waitForSelector('.export-panel-png', { state: 'attached' });
  if (columns > 1) {            // Piskel hides the columns box when there is only 1 frame
    await page.fill('[data-test-id="png-columns-input"]', String(columns));
  }
  const dl = page.waitForEvent('download');
  await page.click('[data-test-id="png-download-button"]');
  const download = await dl;
  await download.saveAs(saveAs);
  await page.click('[data-setting="export"]');   // close the panel
  await page.waitForTimeout(300);
}

// Compare two PNG files pixel by pixel, inside the browser (canvas).
async function comparePngs(page, a, b) {
  const da = 'data:image/png;base64,' + fs.readFileSync(a).toString('base64');
  const db = 'data:image/png;base64,' + fs.readFileSync(b).toString('base64');
  return page.evaluate(async ({ da, db }) => {
    const load = src => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.src = src; });
    const [ia, ib] = await Promise.all([load(da), load(db)]);
    const px = img => { const c = document.createElement('canvas'); c.width = img.width; c.height = img.height;
      const g = c.getContext('2d'); g.drawImage(img, 0, 0); return g.getImageData(0, 0, img.width, img.height).data; };
    if (ia.width !== ib.width || ia.height !== ib.height) {
      return { same: false, why: `size ${ia.width}x${ia.height} vs ${ib.width}x${ib.height}` };
    }
    const pa = px(ia), pb = px(ib); let diff = 0;
    for (let i = 0; i < pa.length; i += 4) {
      const ta = pa[i + 3] === 0, tb = pb[i + 3] === 0;
      if (ta && tb) continue;
      if (pa[i] !== pb[i] || pa[i + 1] !== pb[i + 1] || pa[i + 2] !== pb[i + 2] || pa[i + 3] !== pb[i + 3]) diff++;
    }
    return { same: diff === 0, why: diff + ' different pixels', size: ia.width + 'x' + ia.height };
  }, { da, db });
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1400, height: 900 }, acceptDownloads: true });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));

  const files = fs.readdirSync(path.join(ROOT, '02_Pixel_Art_Assets', 'piskel')).filter(f => f.endsWith('.piskel')).sort();
  for (const f of files) {
    const name = f.replace('.piskel', '');
    const m = META.animations[name];
    await openEditor(page);
    try {
      await importPiskel(page, path.join(ROOT, '02_Pixel_Art_Assets', 'piskel', f));
      rec(f, 'Opens in Piskel', true);
    } catch (e) { rec(f, 'Opens in Piskel', false, e.message); continue; }

    const info = await page.evaluate(() => {
      const pc = window.pskl.app.piskelController, p = pc.getPiskel();
      const colours = new Set(); let transparent = 0;
      for (let fi = 0; fi < pc.getFrameCount(); fi++) {
        const fr = p.getLayerAt(0).getFrameAt(fi);
        for (let y = 0; y < p.getHeight(); y++) for (let x = 0; x < p.getWidth(); x++) {
          const c = fr.getPixel(x, y);
          if (c === 0) { transparent++; continue; }
          const v = c >>> 0; // ABGR int
          const r = v & 255, g = (v >>> 8) & 255, b = (v >>> 16) & 255;
          colours.add([r, g, b].map(n => n.toString(16).padStart(2, '0')).join(''));
        }
      }
      return { w: p.getWidth(), h: p.getHeight(), frames: pc.getFrameCount(), fps: pc.getFPS(),
               layers: p.getLayers().length, colours: [...colours], transparent };
    });
    rec(f, `Size ${m.frame_width}x${m.frame_height}`, info.w === m.frame_width && info.h === m.frame_height, `${info.w}x${info.h}`);
    rec(f, `${m.frames} frames`, info.frames === m.frames, info.frames);
    rec(f, `Speed ${m.fps} FPS`, info.fps === m.fps, info.fps);
    rec(f, 'Only palette colours', info.colours.every(c => PALETTE.includes(c)), info.colours.filter(c => !PALETTE.includes(c)).join(',') || `${info.colours.length} colours`);
    rec(f, 'Has see-through pixels', info.transparent > 0, info.transparent);
    if (name === 'candle_walk') {
      await page.screenshot({ path: path.join(OUT, 'piskel_candle_walk_loaded.png') });
    }

    // Export from Piskel, then compare with the original strip (frame order + pixels)
    const exported = path.join(OUT, `${name}_exported_from_piskel.png`);
    await exportPng(page, m.frames, exported);
    const cmp = await comparePngs(page, exported, path.join(ROOT, '02_Pixel_Art_Assets', 'spritesheets', m.file));
    rec(f, 'Exported PNG matches the original strip (same size, frame order and pixels)', cmp.same, cmp.size ? `${cmp.size}, ${cmp.why}` : cmp.why);

    // Edit test: draw one pixel with the real Pen tool, check it, then undo
    const before = await page.evaluate(() => window.pskl.app.piskelController.getCurrentFrame().getPixel(0, 0));
    await page.evaluate(() => { $.publish(Events.SELECT_PRIMARY_COLOR, ['#c2403a']); });
    await page.click('[data-tool-id="tool-pen"]');
    await page.waitForTimeout(400);
    const xy = await page.evaluate(() => window.pskl.app.drawingController.getScreenCoordinates(0, 0));
    await page.mouse.move(xy.x, xy.y);
    await page.waitForTimeout(400);
    await page.mouse.click(xy.x, xy.y);
    await page.waitForTimeout(300);
    const after = await page.evaluate(() => window.pskl.app.piskelController.getCurrentFrame().getPixel(0, 0));
    if (name === 'candle_walk') {
      await page.screenshot({ path: path.join(OUT, 'piskel_candle_walk_edited.png') });
    }
    await page.keyboard.press('Control+z');
    await page.waitForTimeout(300);
    const undone = await page.evaluate(() => window.pskl.app.piskelController.getCurrentFrame().getPixel(0, 0));
    rec(f, 'Can be edited with the Pen tool (and undone)', before === 0 && after !== 0 && undone === 0,
        `before ${before}, after ${after >>> 0}, after undo ${undone}`);
  }
  rec('-', 'No errors in the Piskel page', errors.length === 0, errors.slice(0, 3).join(' | '));
  await browser.close();

  for (const r of results) console.log((r.ok ? 'PASS  ' : 'FAIL  ') + r.file.padEnd(20) + r.name + (r.info !== undefined ? `  (${r.info})` : ''));
  const failed = results.filter(r => !r.ok).length;
  console.log(`\n${results.length - failed} of ${results.length} Piskel checks passed.`);
  fs.writeFileSync(path.join(OUT, 'piskel_test_results.txt'),
    results.map(r => (r.ok ? 'PASS  ' : 'FAIL  ') + r.file.padEnd(20) + r.name + (r.info !== undefined ? `  (${r.info})` : '')).join('\n')
    + `\n\n${results.length - failed} of ${results.length} Piskel checks passed.\n`);
  process.exit(failed ? 1 : 0);
})();
