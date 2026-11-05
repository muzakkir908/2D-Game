# WICKLIGHT: The Drowned Belfry

![Main menu](04_UI_and_Prototype/screens/01_main_menu_1920x1080.png)

**A 2D pixel-art push-your-luck platformer: complete pre-production package.**
Assignment theme: **No Risk? No Reward!**

> You are Pip, the last living candle in a flooded bell tower. Every ember you swallow makes you
> brighter, worth more and easier to hunt. Bank your glow at a sconce to keep it safe, or keep
> burning and hope the frost moths don't find you first.

![Gameplay](04_UI_and_Prototype/screens/02_gameplay_1920x1080.png)

## Deliverables

| Section | Folder | Start here |
|---|---|---|
| **A. Game concept and rules** | [`01_Game_Concept/`](01_Game_Concept) | [`WICKLIGHT_Game_Design_Document.md`](01_Game_Concept/WICKLIGHT_Game_Design_Document.md) |
| **B. Pixel art asset pack** | [`02_Pixel_Art_Assets/`](02_Pixel_Art_Assets) | [`README.md`](02_Pixel_Art_Assets/README.md) (style guide + Piskel/Unity/Godot import) |
| **C. Level design** | [`03_Level_Design/`](03_Level_Design) | [`LEVEL_DESIGN.md`](03_Level_Design/LEVEL_DESIGN.md) + [`level_01_annotated_design_x2.png`](03_Level_Design/level_01_annotated_design_x2.png) |
| **D. Game UI and prototype** | [`04_UI_and_Prototype/`](04_UI_and_Prototype) | Open [`prototype/index.html`](04_UI_and_Prototype/prototype/index.html) in a browser · [`UI_AND_PROTOTYPE.md`](04_UI_and_Prototype/UI_AND_PROTOTYPE.md) |
| Source / generators | [`tools/`](tools) | `python3 tools/build_all.py` regenerates every image |

## At a glance

| | |
|---|---|
| Genre | 2D precision platformer + risk/reward scoring |
| Core mechanic | **GLOW**: each ember raises your multiplier (×1–×5), moth detection range and wax burn rate. Bank at sconces or lose it all when hit. |
| Controls | Move (A/D, ←/→) + Jump (Space). That's it. |
| Win / lose | Ring the Great Bell / run out of lives or wax |
| Art | 28-colour palette, 16 × 16 grid, 384 × 216 native (×5 = 1080p) |
| Level 1 | 96 × 14 tiles, 4 sections (Teach → Choose → Pressure → Exam), 24 embers, 3 shards, 4 moths, 4 icicles, 3 checkpoints |
| Assets | 1 player (9 frames), 2 enemies, 3 collectibles, 3 objects, 16-tile tileset, UI kit, bitmap font |
| Screens | Main Menu · Gameplay · Victory · Game Over (+ Settings) and a working click-through prototype |

![Annotated level](03_Level_Design/level_01_annotated_design_x2.png)

## Folder map

```
01_Game_Concept/       Game design document (story, mechanics, rules, scoring, loop)
02_Pixel_Art_Assets/
  sprites/             1x transparent PNGs per frame (player, collectibles, hazards, objects)
  spritesheets/        Horizontal animation strips + master sheet + spritesheets.json
  tileset/             16x16 tileset (+ every tile separately, tileset.json)
  palette/             .gpl / .hex palette + palette card
  ui/                  Buttons, 9-slice panels, icons, bitmap font sheet
  preview/             Presentation sheets (asset overview, Pip character sheet)
03_Level_Design/       Annotated map, clean map, grid map, section close-ups
  data/                Tiled .tmj, CSV layers, entity JSON, ASCII source
04_UI_and_Prototype/
  screens/             1920x1080 screens, native 384x216 versions, animated GIFs
  prototype/           index.html interactive prototype (open in browser)
  screen_flow_diagram.png
tools/                 Python (Pillow + NumPy) generators for every asset
```
