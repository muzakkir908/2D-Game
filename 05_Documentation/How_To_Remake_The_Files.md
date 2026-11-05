# How to Remake the Files

All the pictures and data files are made by small Python programs in `tools/`. If you change a sprite or the level, run one command and every file is made again.

## What you need

```bash
pip install pillow numpy
```

## Make all the files again

From the main project folder, run:

```bash
python3 tools/build_all.py
```

## Check the whole project

```bash
python3 tools/check_project.py
```

This checks the PNG files, sprite sheets, Piskel files, the level, the screens and the documents, and prints PASS or FAIL for each check.

## The tool files

| File | What it does |
|---|---|
| `tools/art.py` | The colours, sprites, tiles, background and UI pieces |
| `tools/font.py` | The pixel letters |
| `tools/level.py` | The level layout |
| `tools/build_assets.py` | Saves the pixel art, sprite sheets and Piskel files |
| `tools/build_level.py` | Saves the level maps and checks every jump |
| `tools/build_screens.py` | Saves the 4 screens, the screen flow picture and the HTML prototype |
| `tools/prototype_template.html` | The page design used for the HTML prototype |
| `tools/build_all.py` | Runs the three build files |
| `tools/check_project.py` | Checks the whole project |

## Example: change a sprite

Sprites are written as text in `tools/art.py`. One letter is one pixel and `.` is a see-through pixel. This is the ember:

```
.......KK.......
......KYYK......
.....KYWWYK.....
....KOYWWYOK....
....KOYYYYOK....
.....KOOOOK.....
......KRRK......
.......KK.......
```

`K` = outline, `Y` = yellow, `W` = white, `O` = orange, `R` = red. Change the letters and run `python3 tools/build_all.py`.

## Example: change the level

The level is written as text in `tools/level.py` (`#` ground, `=` platform, `^` spikes, `e` ember, `M` moth, `P` start, `D` door). After a change, run the build again. It checks that every ember and the door can still be reached.
