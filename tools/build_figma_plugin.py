"""Makes a small Figma plugin that builds the WICKLIGHT prototype inside Figma.

Output: 04_UI_and_Prototype/figma_plugin/ (manifest.json + code.js).
The plugin contains the 4 screen PNGs. When you run it in the Figma desktop app it:
  - makes a new page with 4 frames (1920 x 1080) using the screen PNGs,
  - adds every button as its own image layer (cut from the same screen, so it looks the same),
  - adds see-through click areas for the door, the moths and the spikes,
  - links everything (On click -> Navigate to, Dissolve 150 ms),
  - sets Main Menu as the starting screen,
  - renames the old pages to "OLD VERSION" (they are not deleted).
"""
import base64
import io
import json
import os
from PIL import Image
import build_screens as bs

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "04_UI_and_Prototype", "figma_plugin")
S = bs.SCALE  # 5

FRAMES = [  # key, frame name, png file, x, y on the Figma canvas
    ("menu", "Main Menu", "01_main_menu", 0, 0),
    ("game", "Gameplay", "02_gameplay", 2120, 0),
    ("win", "Victory", "03_victory", 0, 1280),
    ("lose", "Game Over", "04_game_over", 2120, 1280),
]
# Level design frames: name, file in 03_Level_Design/, x, y (placed below the 4 screens)
LEVELS = [
    ("Level Map - Annotated", "level_map_annotated_x3.png", 0, 2600),
    ("Level Map", "level_map_x3.png", 1352, 2600),
    ("Level Map - Grid", "level_map_grid.png", 1352, 3376),
]
BUTTON_NAMES = {"play": "PLAY", "settings": "SETTINGS", "exit": "EXIT", "replay": "REPLAY",
                "retry": "RETRY", "main_menu": "MAIN MENU"}


def b64_png(img):
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


def level_data():
    out = []
    for name, png, x, y in LEVELS:
        path = os.path.join(ROOT, "03_Level_Design", png)
        w, h = Image.open(path).size
        with open(path, "rb") as f:
            out.append({"name": name, "x": x, "y": y, "w": w, "h": h,
                        "png": base64.b64encode(f.read()).decode()})
    return out


def plugin_data():
    hs = bs.hotspots()
    screens = []
    for key, name, png, fx, fy in FRAMES:
        full = Image.open(os.path.join(ROOT, "04_UI_and_Prototype", "screens", png + ".png")).convert("RGBA")
        items = []
        for h in hs[key]["hots"]:
            x, y, w, hh = h["r"]
            if h.get("btn"):
                hh += 2                                 # include the button shadow
                box = (x * S, y * S, (x + w) * S, (y + hh) * S)
                items.append({"name": "Button: " + BUTTON_NAMES[h["btn"]], "x": box[0], "y": box[1],
                              "w": box[2] - box[0], "h": box[3] - box[1],
                              "png": b64_png(full.crop(box)), "go": h.get("go")})
            else:
                items.append({"name": "Click area: " + h["label"].replace("Touch ", "").replace("Go into the door", "Exit door"),
                              "x": x * S, "y": y * S, "w": w * S, "h": hh * S, "png": None, "go": h["go"]})
        with open(os.path.join(ROOT, "04_UI_and_Prototype", "screens", png + ".png"), "rb") as f:
            full_b64 = base64.b64encode(f.read()).decode()
        screens.append({"key": key, "name": name, "x": fx, "y": fy, "png": full_b64, "items": items})
    return screens


CODE = r"""// WICKLIGHT - The Little Candle: Figma prototype builder.
// Made by tools/build_figma_plugin.py. Do not edit by hand.
const SCREENS = __DATA__;
const LEVELS = __LEVELS__;
const PAGE_NAME = "WICKLIGHT - The Little Candle";

function imageFill(b64) {
  const img = figma.createImage(figma.base64Decode(b64));
  return [{ type: "IMAGE", imageHash: img.hash, scaleMode: "FILL" }];
}

async function build() {
  if (figma.root.children.some(p => p.name === PAGE_NAME)) {
    throw new Error('A page called "' + PAGE_NAME + '" already exists. Delete it first, then run the plugin again.');
  }
  // Keep the old pages as a backup: rename them, do not delete them.
  for (const p of figma.root.children) {
    if (p.name.indexOf("OLD VERSION") !== 0) {
      p.name = "OLD VERSION (not used) - " + p.name;
    }
  }
  const page = figma.createPage();
  page.name = PAGE_NAME;
  figma.root.insertChild(0, page);
  await figma.setCurrentPageAsync(page);

  const frames = {};
  for (const s of SCREENS) {
    const f = figma.createFrame();
    f.name = s.name;
    f.resize(1920, 1080);
    f.x = s.x;
    f.y = s.y;
    f.clipsContent = true;
    f.fills = [];
    page.appendChild(f);
    const art = figma.createRectangle();
    art.name = "Screen art";
    art.resize(1920, 1080);
    art.fills = imageFill(s.png);
    f.appendChild(art);
    art.locked = true;
    frames[s.key] = f;
  }

  let links = 0;
  for (const s of SCREENS) {
    for (const it of s.items) {
      const r = figma.createRectangle();
      r.name = it.name;
      r.resize(it.w, it.h);
      r.x = it.x;
      r.y = it.y;
      r.fills = it.png ? imageFill(it.png)
                       : [{ type: "SOLID", color: { r: 1, g: 0.83, b: 0.36 }, opacity: 0 }];
      frames[s.key].appendChild(r);
      if (it.go) {
        await r.setReactionsAsync([{
          trigger: { type: "ON_CLICK" },
          actions: [{
            type: "NODE", destinationId: frames[it.go].id, navigation: "NAVIGATE",
            transition: { type: "DISSOLVE", easing: { type: "EASE_OUT" }, duration: 0.15 },
            preserveScrollPosition: false
          }]
        }]);
        links++;
      }
    }
  }
  page.flowStartingPoints = [{ nodeId: frames.menu.id, name: "WICKLIGHT prototype" }];
  figma.viewport.scrollAndZoomIntoView(Object.keys(frames).map(k => frames[k]));
  return links;
}

async function addLevel() {
  const page = figma.root.children.find(p => p.name === PAGE_NAME) || figma.currentPage;
  await figma.setCurrentPageAsync(page);
  if (page.children.some(n => n.name.indexOf("Level Map") === 0)) {
    throw new Error("The level design is already on this page.");
  }
  const made = [];
  for (const l of LEVELS) {
    const f = figma.createFrame();
    f.name = l.name;
    f.resize(l.w, l.h);
    f.x = l.x;
    f.y = l.y;
    f.clipsContent = true;
    f.fills = [];
    page.appendChild(f);
    const art = figma.createRectangle();
    art.name = "Level art";
    art.resize(l.w, l.h);
    art.fills = imageFill(l.png);
    f.appendChild(art);
    art.locked = true;
    made.push(f);
  }
  figma.viewport.scrollAndZoomIntoView(made);
  return made.length;
}

async function deleteOld() {
  const old = figma.root.children.filter(p => p.name.indexOf("OLD VERSION") === 0);
  const keep = figma.root.children.find(p => p.name === PAGE_NAME);
  if (!keep) throw new Error("Run 'Build WICKLIGHT prototype' first.");
  await figma.setCurrentPageAsync(keep);
  for (const p of old) p.remove();
  return old.length;
}

(async () => {
  try {
    if (figma.command === "add-level") {
      const n = await addLevel();
      figma.closePlugin("Done: added " + n + " level design frames below the screens.");
    } else if (figma.command === "delete-old") {
      const n = await deleteOld();
      figma.closePlugin("Deleted " + n + " old page(s).");
    } else {
      const links = await build();
      figma.closePlugin("Done: 4 screens and " + links + " links. Main Menu is the starting screen. Press Present to test.");
    }
  } catch (e) {
    figma.closePlugin("Error: " + e.message);
  }
})();
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    data = plugin_data()
    with open(os.path.join(OUT, "code.js"), "w") as f:
        f.write(CODE.replace("__DATA__", json.dumps(data)).replace("__LEVELS__", json.dumps(level_data())))
    manifest = {
        "name": "WICKLIGHT Prototype Builder",
        "id": "wicklight-prototype-builder",
        "api": "1.0.0",
        "main": "code.js",
        "editorType": ["figma"],
        "documentAccess": "dynamic-page",
        "networkAccess": {"allowedDomains": ["none"]},
        "menu": [
            {"name": "Build WICKLIGHT prototype", "command": "build"},
            {"name": "Add level design", "command": "add-level"},
            {"name": "Delete OLD VERSION pages", "command": "delete-old"},
        ],
    }
    with open(os.path.join(OUT, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)


if __name__ == "__main__":
    main()
