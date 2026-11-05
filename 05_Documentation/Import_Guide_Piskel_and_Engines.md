# How to Open the Art in Piskel (and Game Engines)

Use the normal size files. The files in `preview/` and files with `_x3` or `_x4` in the name are only big copies for showing the art.

## Piskel

### Way 1: open a `.piskel` file (easiest)
1. Open Piskel (piskelapp.com).
2. Click the **folder icon (Open)** on the right.
3. Click **Browse .piskel files** and choose a file from `02_Pixel_Art_Assets/piskel/`, for example `candle_walk.piskel`.
4. All the frames and the animation speed load in one step.

### Way 2: import a PNG sprite sheet
1. Click **Import** on the right, then **Browse images**.
2. Choose a strip from `02_Pixel_Art_Assets/spritesheets/`, for example `candle_walk_strip4.png`.
3. Select **Import as spritesheet**.
4. Set the frame size to **16 × 16**. For the door, use **16 × 32**.
5. Click **Import**. Piskel splits the strip into frames.

### Way 3: open one frame
Click **Import → Browse images** and choose one PNG from `02_Pixel_Art_Assets/sprites/`.

### Add the colour palette
1. Click **Palettes**, then **Import**.
2. Choose `02_Pixel_Art_Assets/palette/wicklight.gpl`.
3. Use only these 16 colours when you change the art, so it still matches.

### Save your work
Use **Save** to get a `.piskel` file, or **Export → PNG → Spritesheet** to get a PNG strip.

## Game engines (for the next assignment)

### Unity
- Set **Texture Type** to Sprite (2D and UI), **Pixels Per Unit** to 16, **Filter Mode** to Point (no filter) and **Compression** to None.
- For strips: set **Sprite Mode** to Multiple, open the **Sprite Editor**, and slice with **Grid By Cell Size** at 16 × 16.

### Godot 4
- In **Project Settings → Rendering → Textures**, set **Default Texture Filter** to **Nearest**.
- Use `AnimatedSprite2D` → **Add frames from sprite sheet** for the strips.
- Use a `TileMapLayer` with `tiles/tileset.png` (16 × 16 tiles).

### Tiled
Open `03_Level_Design/data/level.tmj`. It already uses `tiles/tileset.png`.
