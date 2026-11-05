# WICKLIGHT – Pixel Art Asset Pack

![Asset overview](preview/asset_overview_x4.png)

All the art is simple pixel art on a **16 × 16 pixel grid**. Every PNG has a **see-through (transparent) background**, except the cave background picture. The art uses **16 colours**.

The pictures in `preview/` and files with `_x3` or `_x4` in the name are only bigger copies for showing the art. Use the normal size files in Piskel or a game engine.

How to open the files in Piskel: see [`05_Documentation/Import_Guide_Piskel_and_Engines.md`](../05_Documentation/Import_Guide_Piskel_and_Engines.md).

## Art style

- Simple shapes with a dark outline.
- Each object uses only a few colours.
- Warm colours (yellow, orange and red) are for the candle, the embers and the open door.
- Cool colours (purple and grey) are for the cave, the stone and the moths.

## Colour palette (16 colours)

![Palette](palette/palette_card_x3.png)

Files in `palette/`:
- `wicklight.gpl`: the palette for Piskel (and GIMP and Aseprite)
- `wicklight.hex`: a list of the colour codes
- `palette.png`: one small square for each colour

## Assets

| Required asset | File | Size | Frames |
|---|---|---|---|
| Candle (player) – idle | `sprites/player/candle_idle_0.png`, `_1.png` | 16 × 16 | 2 |
| Candle – walk | `sprites/player/candle_walk_0.png` to `_3.png` | 16 × 16 | 4 |
| Candle – jump | `sprites/player/candle_jump_0.png` | 16 × 16 | 1 |
| Ember (collectible) | `sprites/ember/ember_0.png`, `_1.png` | 16 × 16 | 2 |
| Moth (enemy) | `sprites/moth/moth_0.png`, `_1.png` | 16 × 16 | 2 |
| Exit door | `sprites/door/door_closed.png`, `door_open.png` | 16 × 32 | 2 |
| Spikes (hazard) | `tiles/3_spikes.png` | 16 × 16 | 1 |
| Stone tiles | `tiles/0_ground_top.png`, `1_ground.png`, `2_platform.png` | 16 × 16 | 1 each |
| Tileset (all 4 tiles) | `tiles/tileset.png` | 64 × 16 | – |
| Cave background | `background/cave_background.png` | 384 × 216 | – |

### The 4 tiles

| Number | Tile | Use |
|:---:|---|---|
| 0 | ground_top | Ground you can stand on (top row) |
| 1 | ground | Ground under the top row, and the cave walls |
| 2 | platform | A floating stone platform |
| 3 | spikes | A hazard on the floor |

## Sprite sheets (`spritesheets/`)

- `candle_idle_strip2.png`, `candle_walk_strip4.png`, `candle_jump_strip1.png`, `ember_strip2.png`, `moth_strip2.png`, `door_strip2.png`: one row per animation. Every frame is 16 pixels wide, and there are no gaps between frames.
- `wicklight_spritesheet.png`: all the animations in one picture, one animation per row.
- `spritesheets.json`: the frame size, number of frames and speed for each animation.

| Animation | Frames | Speed (frames per second) |
|---|:---:|:---:|
| candle_idle | 2 | 3 |
| candle_walk | 4 | 8 |
| candle_jump | 1 | – |
| ember | 2 | 4 |
| moth | 2 | 6 |
| door (closed, open) | 2 | – (it changes when you have 5 embers) |

## Piskel files (`piskel/`)

Each animation is also saved as a `.piskel` file. You can open these straight in Piskel with **Open** (the folder icon), and all the frames and the speed are already set.

## UI pieces (`ui/`)

- `buttons/`: PLAY, SETTINGS, EXIT, REPLAY, RETRY and MAIN MENU, each as normal and selected
- `icons/`: full heart, empty heart, ember, empty ember, clock
- `panel.png`: a dark panel with a border
- `font_sheet.png`: the pixel letters used on the screens

## Preview pictures (`preview/`)

- `asset_overview_x4.png`: all assets on one sheet
- `candle_sheet_x8.png`: every candle frame, made bigger, with a pixel grid
