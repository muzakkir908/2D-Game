# WICKLIGHT – UI Screens and Prototype

![How the screens connect](screen_flow.png)

There are 4 screens: **Main Menu**, **Gameplay**, **Victory** and **Game Over**. All screens use the same 16 colours, the same pixel font, the same buttons and the same dark panel.

| File | Size |
|---|---|
| `screens/01_main_menu.png` | 1920 × 1080 |
| `screens/02_gameplay.png` | 1920 × 1080 |
| `screens/03_victory.png` | 1920 × 1080 |
| `screens/04_game_over.png` | 1920 × 1080 |
| `screen_flow.png` | How the screens connect |
| `prototype/index.html` | Clickable HTML prototype |

The screens are drawn at 384 × 216 pixels and saved 5 times bigger, so the pixels stay sharp.

## Screen 1: Main Menu
![](screens/01_main_menu.png)
- Game title "WICKLIGHT" and "THE LITTLE CANDLE"
- A simple cave background with the candle, embers and a moth
- PLAY, SETTINGS and EXIT buttons
- The controls at the bottom: arrow keys to move, space to jump

## Screen 2: Gameplay
![](screens/02_gameplay.png)
The whole level fits on the screen. The bar at the top shows:
- **Lives:** 3 hearts
- **Embers:** 2/5 (the candle already has embers 1 and 2)
- **Timer:** 0:41 (the timer started at 1:00)
- **Goal:** "GET 5 EMBERS, THEN GO TO THE DOOR"

In the level you can see the candle on the first platform, the 3 embers still left, 2 moths, 3 spike groups and the exit door.

## Screen 3: Victory
![](screens/03_victory.png)
- "YOU MADE IT!" and "THE CANDLE FOUND THE WAY OUT."
- Embers 5/5, time left 0:18, lives left 2 of 3
- "LEVEL COMPLETE"
- REPLAY and MAIN MENU buttons

## Screen 4: Game Over
![](screens/04_game_over.png)
- "GAME OVER" and "YOUR FLAME WENT OUT."
- Progress: embers 3/5, the reason (no lives left) and the time left (0:26)
- RETRY and MAIN MENU buttons

## Screen links

| From | Click | Goes to |
|---|---|---|
| Main Menu | PLAY | Gameplay |
| Gameplay | The exit door | Victory |
| Gameplay | A moth or spikes | Game Over |
| Victory | REPLAY | Gameplay |
| Victory | MAIN MENU | Main Menu |
| Game Over | RETRY | Gameplay |
| Game Over | MAIN MENU | Main Menu |

SETTINGS and EXIT are on the menu, but settings are not part of this assignment. In the HTML prototype they show a short message.

## HTML prototype

Open `prototype/index.html` in a web browser by double-clicking it.
- Click the buttons and the door, moths or spikes on the gameplay screen.
- Buttons light up when your mouse is over them.
- Tick **Show click areas** to see everything you can click.
- **Enter** presses the main button. **Esc** goes back to the main menu.

## Figma prototype

**Figma file:** https://www.figma.com/design/E1gSy4J9rj3xGSCBafzJrX

> ⚠️ **This Figma file still shows the OLD, complicated version of the game.** It has to be rebuilt with the 4 new screens before you submit. The tool I used to edit Figma reached its usage limit before I could update the file. Follow the steps below. It takes about 15 minutes.

### How to build the Figma prototype

1. Open the Figma file and delete the old frames (or start a new Design file).
2. Make 4 frames of **1920 × 1080** and name them **Main Menu**, **Gameplay**, **Victory** and **Game Over**.
3. Drag each screen PNG from `screens/` into its frame and place it at **X 0, Y 0**. Do not resize it.
4. Draw a rectangle for each click area in the table below. Set its fill opacity to 0%, so it can't be seen.
5. Click the **Prototype** tab. For each rectangle, add **On click → Navigate to →** the screen in the last column. Use the **Dissolve** animation (150 ms).
6. Select the Main Menu frame and add a **flow starting point** (the ▶ icon in the Prototype tab).
7. Press **Present (▶)** and click through every link once.
8. Click **Share** and set the link to **"Anyone with the link can view"**, or invite your teacher.

### Click areas (in 1920 × 1080 frame coordinates)

| Frame | Click area | X | Y | W | H | Navigate to |
|---|---|---:|---:|---:|---:|---|
| Main Menu | PLAY | 710 | 430 | 500 | 95 | Gameplay |
| Gameplay | Exit door | 1740 | 750 | 120 | 180 | Victory |
| Gameplay | Moth 1 | 1140 | 420 | 160 | 120 | Game Over |
| Gameplay | Moth 2 | 1400 | 820 | 160 | 120 | Game Over |
| Gameplay | Spikes 1 | 480 | 850 | 160 | 70 | Game Over |
| Gameplay | Spikes 2 | 960 | 850 | 240 | 70 | Game Over |
| Gameplay | Spikes 3 | 1280 | 850 | 80 | 70 | Game Over |
| Victory | REPLAY | 510 | 800 | 430 | 95 | Gameplay |
| Victory | MAIN MENU | 980 | 800 | 430 | 95 | Main Menu |
| Game Over | RETRY | 510 | 800 | 430 | 95 | Gameplay |
| Game Over | MAIN MENU | 980 | 800 | 430 | 95 | Main Menu |

These are the same click areas as in the HTML prototype, made 5 times bigger.
