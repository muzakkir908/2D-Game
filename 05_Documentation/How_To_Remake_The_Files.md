# How to Remake the Files

All the images and data files in this project are made by small Python programs in the `tools/` folder. If you change a sprite, a tile or the level, you can make all the files again with one command.

## What you need

- Python 3
- The Pillow and NumPy libraries:
  ```bash
  pip install pillow numpy
  ```

## The command

Run this from the main project folder:

```bash
python3 tools/build_all.py
```

It remakes the files in:
- `02_Pixel_Art_Assets/` (sprites, sprite sheets, tileset, palette, UI pieces, preview sheets)
- `03_Level_Design/` (maps, annotated map, section close-ups, data files)
- `04_UI_and_Prototype/` (screens, prototype images, screen flow diagram)

It does **not** change the written documents (`.md` files), the prototype page `index.html` or the Figma file.

## What each tool file does

| File | What it does |
|---|---|
| `tools/wl.py` | The art library: the colour palette, the sprites (drawn as text maps), the tiles, the pixel font and the UI pieces |
| `tools/level.py` | The level layout (as text) and the code that draws it |
| `tools/build_assets.py` | Saves the pixel art files |
| `tools/build_level.py` | Saves the level maps and level data |
| `tools/build_screens.py` | Draws and saves the UI screens |
| `tools/build_all.py` | Runs the three build files above |

## Example: changing a sprite

Sprites are drawn as text in `tools/wl.py`. Each letter is one colour from the palette, and `.` means a see-through pixel. For example, this is the ember:

```
...KK...
..KYAK..
.KYWAOK.
KAWYAOOK
KOYAORRK
.KOORRK.
..KRRK..
...KK...
```

`K` is the dark outline, `Y` is yellow, `A` is amber, `O` is orange, `R` is red and `W` is white. Change the letters, run `python3 tools/build_all.py`, and the new ember appears in every file and screen.

## Example: changing the level

The level is written as text in `tools/level.py`, one letter per tile. The list of letters is in `03_Level_Design/LEVEL_DESIGN.md`. If you change the level, also check that the jumps still follow the rules: platforms no more than 3 tiles higher, and gaps no wider than 4 tiles.
