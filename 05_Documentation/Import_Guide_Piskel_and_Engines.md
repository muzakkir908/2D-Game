# Import Guide: Piskel and Game Engines

This guide explains how to open the WICKLIGHT pixel art in Piskel and in common game engines.

**Important:** always use the normal size (1×) files from `02_Pixel_Art_Assets/sprites/`, `spritesheets/` and `tileset/`. Files with `_x4` in the name and the files in `preview/` are only enlarged pictures.

## Piskel (piskelapp.com)

### Open one sprite
1. Open Piskel and click **Import** on the right side.
2. Click **Browse images** and choose a file, for example `sprites/player/pip_idle_0.png`.
3. Keep the size at **16 × 16** and click **Import**.

### Open a whole animation
1. Click **Import** → **Browse images**.
2. Choose a strip file, for example `spritesheets/pip_run_strip4.png`.
3. Select **Import as spritesheet**.
4. Set frame width to **16** and frame height to **16**. For the bell, use **32 × 32**.
5. Click **Import**. Piskel splits the strip into frames.
6. Set the speed (FPS) using the table in `02_Pixel_Art_Assets/README.md`. For example, `pip_run` uses 10 FPS.

### Add the colour palette
1. Click **Palettes** on the right side.
2. Click **Import** and choose `palette/wicklight.gpl`.
3. Use only these 28 colours when you draw new art, so it matches the rest of the game.

### Save your work
Use **Export → PNG → Spritesheet** and choose a horizontal layout. This gives the same kind of strip as the files in `spritesheets/`.

## Unity (2D)

1. Copy the `02_Pixel_Art_Assets` folder into your Unity `Assets` folder.
2. Select all the PNG files and set:
   - **Texture Type:** Sprite (2D and UI)
   - **Pixels Per Unit:** 16
   - **Filter Mode:** Point (no filter)
   - **Compression:** None
3. For strip files, set **Sprite Mode** to **Multiple**, open the **Sprite Editor**, and use **Slice → Grid By Cell Size → 16 × 16**.
4. Slice `tileset/wicklight_tileset.png` the same way. Then open **Window → 2D → Tile Palette** and drag the tiles in.
5. For the camera, use the **Pixel Perfect Camera** with a reference resolution of **384 × 216**.

## Godot 4

1. Copy the folder into your project.
2. In **Project Settings → Rendering → Textures**, set **Default Texture Filter** to **Nearest**.
3. In **Project Settings → Display → Window**, set the size to **384 × 216**, **Stretch Mode** to **canvas_items** and **Scale Mode** to **integer**.
4. For animations, add an `AnimatedSprite2D`, open **SpriteFrames** and click **Add frames from sprite sheet**. Choose a strip and set the right number of columns (for example 4 × 1 for `pip_run_strip4.png`).
5. For the level, add a `TileMapLayer` with a new TileSet (tile size 16 × 16) and add `wicklight_tileset.png`. Add collision to tiles 0 and 1 (solid), tile 3 (one-way) and tiles 4–5 (crumbling).

## Phaser, GameMaker and Construct

The strip files (`*_stripN.png`) work directly. Each frame is 16 × 16 pixels with no space between frames.

Phaser example:
```js
this.load.spritesheet('pip_run', 'pip_run_strip4.png', { frameWidth: 16, frameHeight: 16 });
```

## Tiled (map editor)

Open `03_Level_Design/data/level_01.tmj` in Tiled. It already links to `wicklight_tileset.png`, so the level shows up straight away. From Tiled you can export the level to most game engines.
