# Figma Rebuild Guide

The old Figma file I made is in a different Figma account, and it shows the old game. **Do not use it.** Make a new, empty Design file in your own Figma account and use the plugin below. (If you prefer to do it by hand, the manual way is further down.)

## ⭐ Quick way: run the WICKLIGHT plugin (about 3 minutes)

The folder `04_UI_and_Prototype/figma_plugin/` has a small Figma plugin. It builds everything for you: the 4 frames with the screen PNGs, all the buttons, the click areas, the 11 links and the starting screen. It does **not** delete anything by itself. It renames the old pages to "OLD VERSION" so you keep a backup.

You need the **Figma desktop app**, because Figma only allows your own plugins in the desktop app. Download it from figma.com/downloads.

1. Download the project from GitHub (green **Code** button → **Download ZIP**) and unzip it.
2. Open the Figma desktop app. On the home screen, click **Design** (top right) to make a new empty Design file. Click the file name at the top and rename it **WICKLIGHT - The Little Candle**.
3. In the top menu, choose **Plugins → Development → Import plugin from manifest…**
4. Choose the file `04_UI_and_Prototype/figma_plugin/manifest.json`.
5. Choose **Plugins → Development → WICKLIGHT Prototype Builder → Build WICKLIGHT prototype**.
6. Wait a few seconds. A message at the bottom says **"Done: 4 screens and 11 links."**
7. Press **Present (▶)** and test every link with the list in Step 7 below.
8. If everything works, you can remove the old pages with **Plugins → Development → WICKLIGHT Prototype Builder → Delete OLD VERSION pages**.
9. Share the file (Step 8 below).

If the plugin shows an error, use the manual way below.

---

## Manual way (about 15–20 minutes)

**You need these 4 files** (from `04_UI_and_Prototype/screens/`):

| Screen | PNG file | Size |
|---|---|---|
| Main Menu | `01_main_menu.png` | 1920 × 1080 |
| Gameplay | `02_gameplay.png` | 1920 × 1080 |
| Victory | `03_victory.png` | 1920 × 1080 |
| Game Over | `04_game_over.png` | 1920 × 1080 |

---

## Step 1: Clear the old design

1. Open the Figma file.
2. On every page, select everything (**Ctrl + A**, or **Cmd + A** on Mac) and press **Delete**.
3. To delete an extra page, right-click it in the left panel and choose **Delete page**. Keep only one page, and rename it **Prototype**.
4. If there are old colour variables, open the **Local variables** panel and delete the old collection.

## Step 2: Make 4 frames

Press **F** (Frame tool). Draw a frame, then type the exact numbers in the right panel.

| Frame name | X | Y | W | H |
|---|---:|---:|---:|---:|
| Main Menu | 0 | 0 | 1920 | 1080 |
| Gameplay | 2120 | 0 | 1920 | 1080 |
| Victory | 0 | 1280 | 1920 | 1080 |
| Game Over | 2120 | 1280 | 1920 | 1080 |

To rename a frame, double-click its name in the left panel.

## Step 3: Put the screens in the frames

For each frame:
1. Drag the matching PNG file from your computer into the frame.
2. With the picture selected, set **X 0, Y 0, W 1920, H 1080** in the right panel. These numbers are inside the frame.
3. Rename the picture layer **Screen art**.
4. Lock it (click the lock icon next to the layer name), so you don't move it by mistake.

Do not stretch the pictures. They are already the right size, so they stay sharp.

## Step 4: Draw the click areas

Press **R** (Rectangle tool) and draw a rectangle inside the frame. Then type the exact numbers below. They are inside the frame, from its top-left corner.

To make each rectangle invisible but still clickable: in **Fill**, set the opacity to **0%**. Give each rectangle the name in the table.

| Frame | Rectangle name | X | Y | W | H | Goes to |
|---|---|---:|---:|---:|---:|---|
| Main Menu | Click: PLAY | 710 | 430 | 500 | 95 | Gameplay |
| Gameplay | Click: Exit door | 1740 | 750 | 120 | 180 | Victory |
| Gameplay | Click: Moth 1 | 1140 | 420 | 160 | 120 | Game Over |
| Gameplay | Click: Moth 2 | 1400 | 820 | 160 | 120 | Game Over |
| Gameplay | Click: Spikes 1 | 480 | 850 | 160 | 70 | Game Over |
| Gameplay | Click: Spikes 2 | 960 | 850 | 240 | 70 | Game Over |
| Gameplay | Click: Spikes 3 | 1280 | 850 | 80 | 70 | Game Over |
| Victory | Click: REPLAY | 510 | 800 | 430 | 95 | Gameplay |
| Victory | Click: MAIN MENU | 980 | 800 | 430 | 95 | Main Menu |
| Game Over | Click: RETRY | 510 | 800 | 430 | 95 | Gameplay |
| Game Over | Click: MAIN MENU | 980 | 800 | 430 | 95 | Main Menu |

**Where the buttons are on the pictures** (so you can see that the click areas line up):

| Frame | Button | X | Y | W | H |
|---|---|---:|---:|---:|---:|
| Main Menu | PLAY | 710 | 430 | 500 | 85 |
| Main Menu | SETTINGS | 710 | 550 | 500 | 85 |
| Main Menu | EXIT | 710 | 670 | 500 | 85 |
| Victory | REPLAY | 510 | 800 | 430 | 85 |
| Victory | MAIN MENU | 980 | 800 | 430 | 85 |
| Game Over | RETRY | 510 | 800 | 430 | 85 |
| Game Over | MAIN MENU | 980 | 800 | 430 | 85 |

Each click area is 10 pixels taller than its button, so the dark shadow under the button is clickable too.

SETTINGS and EXIT have no link, because there is no settings screen in this assignment.

## Step 5: Add the links

1. Click the **Prototype** tab (top of the right panel).
2. Select a click rectangle. A small **+** circle appears on its right edge.
3. Drag the **+** onto the frame in the "Goes to" column.
4. In the pop-up, check that it says **On click → Navigate to → (frame name)**. Set **Animation** to **Dissolve**, **150 ms**.
5. Do this for all 11 rectangles.

## Step 6: Set the starting screen

1. Still in the **Prototype** tab, click on an empty part of the canvas.
2. Under **Flow starting point**, click **+** and choose **Main Menu**.
3. Name the flow **WICKLIGHT prototype**.

## Step 7: Test it in Present mode

Press **Present (▶)** at the top right. Then click through this list and tick each line:

- [ ] The prototype starts on the **Main Menu**.
- [ ] PLAY → Gameplay
- [ ] Exit door → Victory
- [ ] Victory REPLAY → Gameplay
- [ ] Moth 1 → Game Over
- [ ] Game Over RETRY → Gameplay
- [ ] Moth 2 → Game Over
- [ ] Game Over MAIN MENU → Main Menu
- [ ] PLAY → Gameplay → Spikes 1 → Game Over
- [ ] (Retry) → Spikes 2 → Game Over
- [ ] (Retry) → Spikes 3 → Game Over
- [ ] (Retry) → Exit door → Victory → MAIN MENU → Main Menu

Use the mouse, not the keyboard: in Present mode, Figma uses the arrow keys and spacebar to jump to the next screen. SETTINGS and EXIT are placeholders and do nothing.

Tip: in Present mode, clicking anywhere that is not clickable makes the click areas flash blue. This helps you check they are in the right place.

## Step 8: Share the file

1. Click **Share** (top right).
2. Under **Who has access**, choose **Anyone with the link**, and set it to **can view**.
3. Click **Copy link**.
4. Paste this link into `05_Documentation/Submission_Document.md` and into Moodle.
5. Open the link in a private browser window (not logged in). If you can see the file, your teacher can too.

## Optional: make the text editable

The screens are pictures. To show editable text in Figma, you can add text layers on top. For example, add a text layer "0/5" over the ember counter. This is optional and not needed for the links to work.
