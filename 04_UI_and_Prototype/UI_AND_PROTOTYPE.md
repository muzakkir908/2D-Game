# WICKLIGHT · Game UI and Interactive Prototype

![Screen flow](screen_flow_diagram.png)

## 1. How to run the prototype

Open **`prototype/index.html`** in any browser (double-click it; no server needed).

* Click the buttons on each screen just as you would in the game. Buttons switch to their in-game hover state when the mouse is over them.
* Clicking empty space flashes every clickable area, like Figma's prototype hotspot hints. You can also tick **Show hotspots**.
* Keyboard: **Enter** = main action, **Esc** = back to menu, **W / L** on the gameplay screen = win / lose.
* Every screen animates (4 frames: flames, moth wings, water), using the real in-game frames.

| From | Action | To |
|---|---|---|
| Main Menu | PLAY | Gameplay |
| Main Menu | SETTINGS | Settings → BACK → Main Menu |
| Main Menu | EXIT | "Thanks for playing" message (a browser can't close the game) |
| Gameplay | Click the area to the right / the Bell Shard route (or W) | **Victory** |
| Gameplay | Click the frost moth or the spikes (or L) | **Game Over** |
| Gameplay | Esc | Main Menu |
| Victory | REPLAY | Gameplay |
| Victory | MAIN MENU | Main Menu |
| Game Over | RETRY | Gameplay |
| Game Over | MAIN MENU | Main Menu |

## 2. Screens

All screens are drawn at the game's native **384 × 216** and exported at **×5 = 1920 × 1080**, using only the 28-colour palette, the Belfry 5×7 font and the same panel and button components.

| File | Size |
|---|---|
| `screens/01_main_menu_1920x1080.png` | 1920 × 1080 |
| `screens/02_gameplay_1920x1080.png` | 1920 × 1080 |
| `screens/03_victory_1920x1080.png` | 1920 × 1080 |
| `screens/04_game_over_1920x1080.png` | 1920 × 1080 |
| `screens/05_settings_bonus_1920x1080.png` | 1920 × 1080 (bonus) |
| `screens/native_384x216/*.png` | 1× originals for engines |
| `screens/*_animated.gif` | 4-frame animated previews |

### Screen 1: Main Menu
![](screens/01_main_menu_1920x1080.png)
* **Logo:** "WICKLIGHT" in the Belfry font at ×4, two-band flame gradient (yellow over orange with a white-hot top line), with **Pip's flame dotting the I**.
* **Background:** the belfry interior: arched moonlit windows with light shafts, Pip idling beside a lit sconce on a mossy ledge, black water, a dark Great Bell looming top-right (the goal is visible from the first screen), drifting embers and a distant moth.
* **Buttons:** PLAY (selected, flame-orange), SETTINGS, EXIT, with a flame cursor either side of the selection.
* **Footer:** best score (bottom-left) and the theme tag and version (bottom-right).

### Screen 2: Gameplay (HUD)
![](screens/02_gameplay_1920x1080.png)

| HUD zone | Shows | Why there |
|---|---|---|
| Top-left panel | **Lives** (3 hearts) and **wax timer** (melting candle bar + 1:42) | Survival info grouped together |
| Top-centre banner | **Objective: "RING THE GREAT BELL"** + 4 section pips (progress) | Always-visible goal |
| Top-right panel | **Score** (banked), **embers 10/24**, **bell shards** (0/3 icons) | Reward info grouped together |
| Bottom-left panel | **GLOW ×3** (5 flame pips) + **AT RISK 60** + "BANK IT!" | The core risk/reward decision, next to Pip's feet where the eye already is |
| Bottom-right | Control hints | Fades out after the first section in the final game |
| In-world | Moth **"!" alert**, dotted **detection ring** around Pip (grows with glow), **+40** pickup popup | Feedback where the action is |

### Screen 3: Victory
![](screens/03_victory_1920x1080.png)
Score breakdown (embers banked, shards with icons, wax bonus, hits), **final score**, **rank** (BLAZE, 4 of 5 flames), a "NEW BEST!" flag, a hint about the missed shard (gives a reason to replay), and **REPLAY** / **MAIN MENU**. The ringing bell is visible behind the panel.

### Screen 4: Game Over
![](screens/04_game_over_1920x1080.png)
The whole screen is re-graded **frost blue**: warm colours are gone because Pip's flame went out. Shows the cause of death, **progress to the bell** (62% bar with section ticks and Pip's marker), banked score, embers lost (a reminder that unbanked glow is lost), shards, the section reached, a **tip**, and **RETRY** / **MAIN MENU**.

### Bonus: Settings
Volume bars, toggles (fullscreen, pixel-perfect, an accessibility "slow wax" assist) and controls.

## 3. UI style rules

* **Font:** Belfry 5×7 (custom bitmap, in `02_Pixel_Art_Assets/ui/`). ×1 for body, ×2 for screen titles, ×4 for the logo. Text always has a 1 px soot outline + drop shadow so it reads over any background.
* **Colour meaning:** amber/yellow = reward or primary action · frost blue = checkpoints, info, game over · red = risk (AT RISK points) · green = positive news (NEW BEST, ON).
* **Components:** stone 9-slice panel (4 px bevel, bronze rivets) for neutral UI, frost panel for failure, 17 px buttons (selected = flame gradient with dark text, idle = stone with light text).
* **Grid:** 4 px margins on the 384 × 216 canvas (20 px at 1080p). HUD panels sit in the four corners so the centre of the playfield stays clear.

## 4. Figma prototype (built)

**Figma file:** https://www.figma.com/design/E1gSy4J9rj3xGSCBafzJrX

This is a real Figma Design file built for this project, not just instructions. Open it and press **Present (▶)**. The flow starts at *Main Menu*.

| Page | Contents |
|---|---|
| **🔥 Prototype** | 5 frames at 1920 × 1080: *1 · Main Menu*, *2 · Gameplay*, *3 · Victory*, *4 · Game Over*, *5 · Settings*, with every navigation link wired |
| **Components (pixel art + UI)** | Every tile (stone, mossy top, background brick, window, pillar, plank, crumble, spikes, water) and sprite (Pip ×4 poses, ember, wax drop, bell shard, frost moth, icicle, sconce lit/unlit, Great Bell) rebuilt **pixel-for-pixel as Figma components** from the same pixel maps as `tools/wl.py`, plus a `UI/Button` variant set (Default / Selected, editable **Label** property) and resizable `UI/Panel Stone` / `UI/Panel Frost` components |
| **Art Assets** | HUD icons (hearts, clock, ember, shard, glow flames, bell) |
| Local variables | **Wicklight Palette**: all 28 colours as colour variables |

Everything is editable. Each scene is a **tilemap of component instances** in layers (*background → veil → terrain → entities → lighting → FX → HUD*), so editing a tile component updates every screen. All text is live Silkscreen text.

**Interactions:** PLAY → Gameplay · SETTINGS → Settings → BACK → Menu · on Gameplay, click the **moth** or **spikes** → Game Over, and click the **shard route on the right** → Victory · REPLAY/RETRY → Gameplay · MAIN MENU → Menu. Keyboard: Enter, Esc, and W/L on gameplay, the same as the HTML prototype. Transitions use Dissolve, 150 ms.

### Rebuilding it by hand (alternative)
If you'd rather assemble your own Figma file from the PNGs:
1. Make 5 frames of **1920 × 1080** and drop each `screens/*_1920x1080.png` in at (0,0). They're pre-scaled with nearest-neighbour, so they stay crisp. `figma_assets/bg_*.png` are the same scenes **without UI** if you want to rebuild the UI as layers.
2. Add transparent hotspot rectangles at these frame coordinates and set **On click → Navigate to**, Dissolve 150 ms:

| Frame | Hotspot | X | Y | W | H | Navigate to |
|---|---|---:|---:|---:|---:|---|
| Main Menu | PLAY | 700 | 420 | 520 | 95 | Gameplay |
| Main Menu | SETTINGS | 700 | 540 | 520 | 95 | Settings |
| Settings | BACK | 760 | 840 | 400 | 95 | Main Menu |
| Gameplay | Frost moth | 1020 | 180 | 200 | 150 | Game Over |
| Gameplay | Spikes | 790 | 740 | 260 | 80 | Game Over |
| Gameplay | Right route / shard | 1500 | 220 | 420 | 260 | Victory |
| Victory | REPLAY | 430 | 850 | 500 | 95 | Gameplay |
| Victory | MAIN MENU | 990 | 850 | 500 | 95 | Main Menu |
| Game Over | RETRY | 430 | 860 | 500 | 95 | Gameplay |
| Game Over | MAIN MENU | 990 | 860 | 500 | 95 | Main Menu |

3. Set *Main Menu* as the flow starting point and press ▶.
