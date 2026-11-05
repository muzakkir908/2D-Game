# WICKLIGHT: Pixel Art Assets

![Asset overview](preview/asset_pack_overview_x4.png)

All PNG files in this folder are **real pixel art with transparent backgrounds**. They use a **16 × 16 pixel grid**. The Great Bell is the only bigger sprite, at 32 × 32.

Files with `_x4` in the name, and the files in `preview/`, are enlarged copies for showing the art. When you import into Piskel or a game engine, use the normal (1×) files.

How to import the files into Piskel, Unity, Godot and other tools: see [`05_Documentation/Import_Guide_Piskel_and_Engines.md`](../05_Documentation/Import_Guide_Piskel_and_Engines.md).

## 1. Art style

| | |
|---|---|
| **Style** | Simple pixel art. Every sprite has a 1-pixel dark outline. Each material uses one light shade and one dark shade. No smooth edges. |
| **Main idea** | Warm against cold. **Only Pip and rewards use warm colours** (fire, embers, wax, bronze). The tower and the dangers are cold (blue stone, frost, purple moths, dark water). You can understand the screen just from the colours. |
| **Colour palette** | 28 colours (see below). |
| **Lighting** | The tower is dark. Light comes from Pip, the embers and the sconces. The light fades in 4 steps with a pixel dither pattern at the edges, so it still looks like pixel art. The windows give a weak, cold moonlight. |
| **Background** | Dark brick walls with tall windows, pillars and chains. They have low contrast, so the platforms stand out. |
| **Platforms** | Mossy stone bricks (you can stand on them), wooden planks (you can jump up through them), pale cracked stone (it falls), iron spikes and dark water. |
| **Sizes** | Sprites 16 × 16, goal 32 × 32, HUD icons 5–7 pixels, font 5 × 7 pixels. |
| **Game screen** | 384 × 216 pixels (24 × 13.5 tiles), shown 5 times bigger at 1920 × 1080. |

## 2. Colour palette

The palette files are in `palette/`:
- `wicklight.gpl`: for Piskel, GIMP and Aseprite
- `wicklight.hex`: a plain list of colours (for Lospec and other tools)
- `wicklight_palette_1x.png`: one 8 × 8 square per colour
- `wicklight_palette_card.png`: a bigger card with the colour codes

![Palette](palette/wicklight_palette_card.png)

| Group | Colours | Used for |
|---|---|---|
| Outline | `#0D0B1A` | Outlines, gaps between bricks, text outline |
| Stone | `#1A1A2E` `#26324A` `#3B4D6B` `#5A7394` `#8AA2BF` | Walls, floors, UI panels |
| Water | `#14394A` `#1F6F78` `#4FB3A9` `#A8E6CF` | Water, foam |
| Moss | `#3E6B3A` `#6EA24B` | Tops of the stone you can stand on |
| Wood | `#4A2C2A` `#7A4A35` `#A8714A` | Planks, the bell's beam |
| Flame | `#B83B3B` `#F07B3F` `#FFB84D` `#FFE08A` `#FFF6D6` | Pip, embers, sconces, important UI |
| Wax | `#EFE3C8` `#C9B48F` | Pip's body, wax drops, UI text |
| Frost | `#BFE9FF` `#7FB8E0` | Moths, icicles, the Game Over screen |
| Moth | `#6B5A9E` `#3D3263` | Moth bodies, the frost UI panel |
| Bronze | `#8C6A2F` `#C9973A` | The bell, bell shards, panel corners |

## 3. What is in each folder

### `sprites/`: one PNG per frame

![Pip](preview/pip_character_sheet.png)

| Folder | File names | Frames |
|---|---|---|
| `player/` | `pip_idle_0–1`, `pip_run_0–3`, `pip_jump_0`, `pip_fall_0`, `pip_hurt_0` | 9 |
| `collectibles/` | `ember_0–3`, `wax_drop_0–1`, `bell_shard_0–3` | 10 |
| `hazards/` | `frost_moth_0–1`, `icicle_0–1` | 4 |
| `objects/` | `sconce_unlit_0`, `sconce_lit_0–1`, `great_bell_idle_0`, `great_bell_ringing_0–1` | 6 |

| Animation | Frames | Speed (frames per second) | What happens |
|---|:---:|:---:|---|
| `pip_idle` | 2 | 3 | The flame flickers |
| `pip_run` | 4 | 10 | The flame leans back and the body bobs |
| `pip_jump` | 1 | – | Eyes look up and the flame splits |
| `pip_fall` | 1 | – | The flame stretches up and the feet spread |
| `pip_hurt` | 1 | – | The flame turns blue and the eyes close |
| `ember` | 4 | 8 | A small spark moves around it |
| `wax_drop` | 2 | 3 | It moves up and down |
| `bell_shard` | 4 | 6 | A shine moves down it |
| `frost_moth` | 2 | 8 | Wings flap |
| `icicle` | 2 | 2 | A drip forms (a warning that it will fall) |
| `sconce_lit` | 2 | 6 | The flame flickers |
| `great_bell_ringing` | 2 | 8 | Sound lines appear around the bell |

### `spritesheets/`: animations in one image

- `*_stripN.png`: one row per animation. N is the number of frames. Each frame is 16 × 16 (32 × 32 for the bell), with no space between frames. **Use these for Piskel.**
- `wicklight_master_spritesheet.png`: all 16 × 16 animations in one image, one animation per row.
- `spritesheets.json`: frame size, number of frames, speed and looping for every strip, plus which row each animation is on in the master sheet.

### `tileset/`: the environment tiles

![Tileset](tileset/wicklight_tileset_x4_preview.png)

`wicklight_tileset.png` is 8 × 2 tiles (128 × 32 pixels). `tiles/` has each tile as its own file, and `tileset.json` lists the names and types.

| Number | Tile | Type |
|:---:|---|---|
| 0 | stone_top (with moss) | solid |
| 1 | stone | solid |
| 2 | stone_bg | background |
| 3 | plank | one-way platform (you can jump up through it) |
| 4 | crumble | falls after you stand on it |
| 5 | crumble_breaking | shown just before it falls |
| 6 | spikes | hazard |
| 7 | pillar | background |
| 8–9 | water_surface (2 animation frames) | water hazard |
| 10 | water_fill | water hazard |
| 11 | chain | decoration |
| 12–13 | window_top / window_bottom | background |
| 14 | icicle_mount | marks where an icicle hangs |
| 15 | sconce_unlit | marks where a sconce goes |

### `ui/`: interface pieces

- `buttons/`: PLAY, SETTINGS, EXIT, REPLAY, RETRY and MAIN MENU, each in a normal (`_idle`) and a highlighted (`_hover`) version
- `panel_stone_9slice_48.png` and `panel_frost_9slice_48.png`: frame panels with a 4-pixel border that can be stretched
- `icons/`: full and empty heart, ember, shard, empty shard, clock
- `font_belfry5x7_sheet.png`: the pixel font used on every screen. The letter order is in `font_belfry5x7_order.txt`.

### `preview/`: images for presenting

- `asset_pack_overview_x4.png`: every asset on one sheet
- `pip_character_sheet.png`: every Pip frame, enlarged with a pixel grid and the hitbox
