// Tests the Figma plugin (04_UI_and_Prototype/figma_plugin/code.js) outside Figma.
// It runs the plugin code with a pretend "figma" object that records what the plugin
// creates, then checks the frames, images, buttons, links and starting screen.
// IMPORTANT: this tests the plugin's logic only. It is NOT the same as running it in Figma.
// Run:  node tools/test_figma_plugin.js
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const CODE = fs.readFileSync(path.join(ROOT, '04_UI_and_Prototype', 'figma_plugin', 'code.js'), 'utf8');

function makeFigma(command, startPages) {
  let nextId = 1;
  const images = {};
  const node = (type) => ({
    id: `1:${nextId++}`, type, name: '', x: 0, y: 0, width: 100, height: 100, children: [],
    fills: [], reactions: [], locked: false, parent: null,
    resize(w, h) { this.width = w; this.height = h; },
    appendChild(c) { c.parent = this; this.children.push(c); },
    async setReactionsAsync(r) { this.reactions = r; },
    remove() { const a = this.parent.children; a.splice(a.indexOf(this), 1); },
  });
  // insertChild MOVES a node (like Figma): take it out of its old place first.
  const root = { children: [], insertChild(i, p) {
    const old = this.children.indexOf(p); if (old >= 0) this.children.splice(old, 1);
    p.parent = root; this.children.splice(i, 0, p); } };
  for (const name of startPages) { const p = node('PAGE'); p.name = name; p.parent = root; root.children.push(p); }
  let closed = null;
  const figma = {
    command, root, currentPage: root.children[0],
    createPage() { const p = node('PAGE'); p.parent = root; root.children.push(p); p.flowStartingPoints = []; return p; },
    createFrame() { return node('FRAME'); },
    createRectangle() { return node('RECTANGLE'); },
    createImage(bytes) { const hash = 'h' + Object.keys(images).length; images[hash] = Buffer.from(bytes); return { hash }; },
    base64Decode(s) { return new Uint8Array(Buffer.from(s, 'base64')); },
    async setCurrentPageAsync(p) { figma.currentPage = p; },
    viewport: { scrollAndZoomIntoView() {} },
    closePlugin(msg) { closed = msg; },
  };
  return { figma, images, getClosed: () => closed };
}

async function run(command, pages) {
  const env = makeFigma(command, pages);
  vm.runInNewContext(CODE, { figma: env.figma, console });
  for (let i = 0; i < 50 && env.getClosed() === null; i++) await new Promise(r => setTimeout(r, 10));
  return env;
}

function pngSize(buf) { return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) }; }

(async () => {
  const results = [];
  const check = (name, ok, info) => results.push({ name, ok, info });
  const { figma, images, getClosed } = await run('build', ['Prototype']);
  const page = figma.root.children[0];

  check('Plugin finishes without an error', getClosed() && !getClosed().startsWith('Error'), getClosed());
  check('New page is first and named correctly', page.name === 'WICKLIGHT - The Little Candle', page.name);
  check('Old page renamed (kept as backup, not deleted)',
        figma.root.children.length === 2 && figma.root.children[1].name.startsWith('OLD VERSION'), figma.root.children[1].name);

  const frames = page.children.filter(n => n.type === 'FRAME');
  const want = { 'Main Menu': ['01_main_menu', 0, 0], 'Gameplay': ['02_gameplay', 2120, 0],
                 'Victory': ['03_victory', 0, 1280], 'Game Over': ['04_game_over', 2120, 1280] };
  check('Exactly 4 frames', frames.length === 4, frames.map(f => f.name).join(', '));
  for (const f of frames) {
    const [png, x, y] = want[f.name] || [];
    check(`${f.name}: 1920 x 1080 at (${x}, ${y})`, f.width === 1920 && f.height === 1080 && f.x === x && f.y === y,
          `${f.width}x${f.height} at (${f.x}, ${f.y})`);
    const art = f.children[0];
    const bytes = images[art.fills[0].imageHash];
    const file = fs.readFileSync(path.join(ROOT, '04_UI_and_Prototype', 'screens', png + '.png'));
    check(`${f.name}: screen art is the exact file ${png}.png (not stretched)`,
          art.name === 'Screen art' && bytes.equals(file) && art.width === 1920 && art.height === 1080 && art.locked);
  }
  const byName = Object.fromEntries(frames.map(f => [f.name, f]));
  const buttons = frames.flatMap(f => f.children.filter(c => c.name.startsWith('Button: ')).map(c => [f.name, c]));
  check('7 buttons exist (PLAY, SETTINGS, EXIT, REPLAY, MAIN MENU, RETRY, MAIN MENU)', buttons.length === 7,
        buttons.map(([f, c]) => `${f}/${c.name}`).join(', '));
  for (const [f, b] of buttons) {
    const s = pngSize(images[b.fills[0].imageHash]);
    check(`${f} ${b.name}: button image has the same size as its layer`, s.w === b.width && s.h === b.height, `${s.w}x${s.h}`);
  }
  const linkOf = (frame, name) => {
    const n = byName[frame].children.find(c => c.name === name);
    if (!n || !n.reactions.length) return null;
    const a = n.reactions[0].actions[0];
    const dest = frames.find(fr => fr.id === a.destinationId);
    return n.reactions[0].trigger.type === 'ON_CLICK' && a.navigation === 'NAVIGATE' ? dest && dest.name : null;
  };
  const LINKS = [
    ['Main Menu', 'Button: PLAY', 'Gameplay'],
    ['Gameplay', 'Click area: Exit door', 'Victory'],
    ['Gameplay', 'Click area: moth 1', 'Game Over'],
    ['Gameplay', 'Click area: moth 2', 'Game Over'],
    ['Gameplay', 'Click area: spikes 1', 'Game Over'],
    ['Gameplay', 'Click area: spikes 2', 'Game Over'],
    ['Gameplay', 'Click area: spikes 3', 'Game Over'],
    ['Victory', 'Button: REPLAY', 'Gameplay'],
    ['Victory', 'Button: MAIN MENU', 'Main Menu'],
    ['Game Over', 'Button: RETRY', 'Gameplay'],
    ['Game Over', 'Button: MAIN MENU', 'Main Menu'],
  ];
  for (const [f, n, dest] of LINKS) check(`Link: ${f} / ${n} -> ${dest}`, linkOf(f, n) === dest, linkOf(f, n));
  const total = frames.reduce((s, f) => s + f.children.filter(c => c.reactions.length).length, 0);
  check('Exactly 11 links in total', total === 11, total);
  check('SETTINGS and EXIT have no link', !linkOf('Main Menu', 'Button: SETTINGS') && !linkOf('Main Menu', 'Button: EXIT'));
  const fsp = page.flowStartingPoints || [];
  check('Starting screen is Main Menu', fsp.length === 1 && fsp[0].nodeId === byName['Main Menu'].id);

  // second command: delete the old pages
  const env2 = makeFigma('build', ['Prototype']);
  vm.runInNewContext(CODE, { figma: env2.figma, console });
  for (let i = 0; i < 50 && env2.getClosed() === null; i++) await new Promise(r => setTimeout(r, 10));
  env2.figma.command = 'delete-old';
  let closed2 = null; env2.figma.closePlugin = m => { closed2 = m; };
  vm.runInNewContext(CODE, { figma: env2.figma, console });
  for (let i = 0; i < 50 && closed2 === null; i++) await new Promise(r => setTimeout(r, 10));
  check('"Delete OLD VERSION pages" removes only the old pages',
        env2.figma.root.children.length === 1 && env2.figma.root.children[0].name === 'WICKLIGHT - The Little Candle', closed2);

  // running it twice should stop, not make a second copy
  const env3 = makeFigma('build', ['WICKLIGHT - The Little Candle']);
  vm.runInNewContext(CODE, { figma: env3.figma, console });
  for (let i = 0; i < 50 && env3.getClosed() === null; i++) await new Promise(r => setTimeout(r, 10));
  check('Running it twice stops with a clear message', (env3.getClosed() || '').startsWith('Error: A page called'), env3.getClosed());

  // "Add level design": run it in the file that already has the 4 screens
  let closedL = null; figma.command = 'add-level'; figma.closePlugin = m => { closedL = m; };
  vm.runInNewContext(CODE, { figma, console });
  for (let i = 0; i < 50 && closedL === null; i++) await new Promise(r => setTimeout(r, 10));
  check('"Add level design" finishes without an error', closedL && !closedL.startsWith('Error'), closedL);
  const lv = page.children.filter(n => n.name.indexOf('Level Map') === 0);
  const LV = { 'Level Map - Annotated': 'level_map_annotated_x3.png', 'Level Map': 'level_map_x3.png',
               'Level Map - Grid': 'level_map_grid.png' };
  check('3 level frames on the same page as the screens', lv.length === 3, lv.map(f => f.name).join(', '));
  for (const f of lv) {
    const file = fs.readFileSync(path.join(ROOT, '03_Level_Design', LV[f.name]));
    const art = f.children[0];
    const sz = pngSize(file);
    check(`${f.name}: exact image ${LV[f.name]}, same size (${sz.w} x ${sz.h}), not stretched`,
          images[art.fills[0].imageHash].equals(file) && f.width === sz.w && f.height === sz.h
          && art.width === sz.w && art.height === sz.h && art.locked);
  }
  const overlap = (a, b) => a.x < b.x + b.width && b.x < a.x + a.width && a.y < b.y + b.height && b.y < a.y + a.height;
  const all = [...frames, ...lv];
  check('No frames overlap', all.every((a, i) => all.every((b, j) => i === j || !overlap(a, b))));
  check('The 11 screen links are unchanged', frames.reduce((n, f) => n + f.children.filter(c => c.reactions.length).length, 0) === 11);
  let closedL2 = null; figma.closePlugin = m => { closedL2 = m; };
  vm.runInNewContext(CODE, { figma, console });
  for (let i = 0; i < 50 && closedL2 === null; i++) await new Promise(r => setTimeout(r, 10));
  check('Running "Add level design" twice stops with a clear message, no copies',
        (closedL2 || '').startsWith('Error: The level design is already') &&
        page.children.filter(n => n.name.indexOf('Level Map') === 0).length === 3, closedL2);

  for (const r of results) console.log((r.ok ? 'PASS  ' : 'FAIL  ') + r.name + (r.ok || r.info === undefined ? '' : `  (${r.info})`));
  const failed = results.filter(r => !r.ok).length;
  console.log(`\n${results.length - failed} of ${results.length} Figma plugin checks passed (logic test, not run inside Figma).`);
  process.exit(failed ? 1 : 0);
})();
