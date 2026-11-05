# Verification Report

This report lists every requirement, how it was checked and what is still left to do.

**Status words used:**
- **Complete and verified:** the work is done and was checked.
- **Complete but not tested:** the work is done, but one test could not be done.
- **Incomplete:** the work is not finished.
- **Requires my attention:** the student must do something before submitting.

## 1. Requirements table

| Requirement | File/location | Test performed | Status | Remaining work |
|---|---|---|---|---|
| **A. Game concept and rules** | | | | |
| Title, pitch, genre, audience, story, setting | `01_Game_Concept/WICKLIGHT_Game_Design_Document.md` | Read through every section; checked against the brief | Complete and verified | – |
| Character, objective, core mechanic, controls | same file | Read through; controls checked against the main menu text | Complete and verified | – |
| Rules, collectibles, hazards, scoring | same file | Numbers checked against the level and screens (5 embers, 3 lives, 60 s, 2 moths, 3 spike groups) by `check_project.py` | Complete and verified | – |
| Win and lose conditions, gameplay loop | same file | Checked against the Victory and Game Over screens | Complete and verified | – |
| **B. Pixel art and Piskel** | | | | |
| Candle player sprite | `02_Pixel_Art_Assets/sprites/player/` | Automatic checks (transparency, palette colours, stray pixels, frame alignment) and checked by eye at 8× size | Complete and verified | – |
| Idle animation (2 frames) | `candle_idle_0–1.png`, `candle_idle_strip2.png` | Strip matches the single frames; frames line up | Complete and verified | – |
| Walk animation (4 frames) | `candle_walk_0–3.png`, `candle_walk_strip4.png` | Strip matches the frames; no duplicate frames | Complete and verified | – |
| Jump sprite | `candle_jump_0.png` | Automatic checks and checked by eye | Complete and verified | – |
| Ember collectible | `sprites/ember/` | Automatic checks and checked by eye | Complete and verified | – |
| Moth enemy | `sprites/moth/` | Automatic checks and checked by eye | Complete and verified | – |
| Spike hazard | `tiles/3_spikes.png` | Automatic checks and checked by eye | Complete and verified | – |
| Stone tiles (4 tiles) | `tiles/`, `tiles/tileset.png` | Tile size 16 × 16; tiles join up correctly on the level map | Complete and verified | – |
| Cave background | `background/cave_background.png` | Size 384 × 216; checked by eye | Complete and verified | – |
| Exit door | `sprites/door/` | Size 16 × 32; checked by eye | Complete and verified | – |
| Combined sprite sheet | `spritesheets/wicklight_spritesheet.png` | Each row matches its strip exactly | Complete and verified | – |
| Palette | `palette/wicklight.gpl` | 16 colours; every pixel in every sprite uses only these colours | Complete and verified | – |
| Transparent backgrounds | all sprite PNGs | Every sprite is RGBA, has a clear corner pixel and no half-transparent pixels | Complete and verified | – |
| Files open in Piskel | `piskel/*.piskel`, `spritesheets/*.png` | The `.piskel` files were checked against the rules in Piskel's own loading code. The Piskel website could not be reached from my computer, so the files were **not** opened in Piskel itself. | Complete but not tested | Open one `.piskel` file and one PNG strip in Piskel |
| **C. Level design** | | | | |
| Complete level map | `03_Level_Design/level_map_x3.png`, `level_map_grid.png` | Checked by eye; one screen, 24 × 12 tiles | Complete and verified | – |
| Start, exit, route, platforms, embers, enemies, hazards marked | `level_map_annotated_x3.png` | Checked by eye; legend lists every symbol | Complete and verified | – |
| Readable notes | `level_map_annotated_x3.png`, `LEVEL_DESIGN.md` | 8 numbered notes checked by eye at full size | Complete and verified | – |
| Jumps are possible | `data/jump_check_result.json` | Automatic check: every route jump is at most 3 tiles up and 4 tiles across; all 5 embers and the door can be reached | Complete and verified | – |
| Map matches the rules | level + concept document | 5 embers, 2 moths, 3 spike groups, 1 start and 1 door counted automatically | Complete and verified | – |
| **D. UI screens and prototype** | | | | |
| Main Menu (title, background, PLAY, SETTINGS, EXIT) | `04_UI_and_Prototype/screens/01_main_menu.png` | Checked by eye at full size; nothing overlaps | Complete and verified | – |
| Gameplay (player, level, embers, enemies, hazards, lives, timer, ember counter, goal) | `screens/02_gameplay.png` | Checked by eye; HUD numbers checked automatically (2/5 embers = 2 embers missing from the level) | Complete and verified | – |
| Victory (message, embers, completion, REPLAY, MAIN MENU) | `screens/03_victory.png` | Checked by eye | Complete and verified | – |
| Game Over (message, progress, RETRY, MAIN MENU) | `screens/04_game_over.png` | Checked by eye | Complete and verified | – |
| HTML prototype links | `prototype/index.html` | Automatic browser test: 27 of 27 checks passed (every link, both messages, keys, images, phone width, no errors) | Complete and verified | – |
| **Figma project with the 4 new screens** | Figma file | Not done: the Figma editing tool reached its plan limit. **The Figma file still shows the old, complicated version.** | Incomplete | Rebuild it with the steps in `04_UI_and_Prototype/UI_AND_PROTOTYPE.md` |
| Figma prototype links | Figma file | Not done (see above) | Incomplete | Add the 11 click areas from the table in `UI_AND_PROTOTYPE.md` |
| Figma tested in Present mode | Figma file | Not done | Requires my attention | Click every link in Present mode |
| Figma sharing | Figma file | Can't be checked with my tools | Requires my attention | Set sharing to "Anyone with the link can view" |
| **E. Gameplay consistency** | | | | |
| Controls, 3 lives, 60 s timer, 5 embers, win and lose rules | all documents and screens | `check_project.py` checks the numbers on every screen; documents read through | Complete and verified | – |
| **F. Repository** | | | | |
| Folders, file names, no temporary or duplicate files | whole repository | File list checked; no duplicate sprites (automatic); no cache or log files tracked | Complete and verified | – |
| Files can be made again | `tools/build_all.py` | Ran the build again; all files were made with no errors | Complete and verified | – |
| Repository link works for the teacher | GitHub link | Can't be checked with my tools | Requires my attention | Check that your teacher can open it |
| **G. Documentation** | | | | |
| Simple English, same words everywhere, no old game words | all `.md` files | Read through; automatic check for 15 words from the old version | Complete and verified | – |
| All links and images work | all `.md` files | Automatic check of every link and image | Complete and verified | – |
| **H. Submission document** | `05_Documentation/Submission_Document.md` | Read through; all links checked | Requires my attention | Fill in your name, student number, course and date |

## 2. Tests performed

| Test | How | Result |
|---|---|---|
| Project check | `python3 tools/check_project.py` | **33 of 33 checks passed** |
| HTML prototype test | `node tools/test_prototype.js` (Playwright and Chromium) | **27 of 27 checks passed** |
| Jump check | `tools/build_level.py` | All jumps OK; all embers and the door can be reached |
| Rebuild | `python3 tools/build_all.py` | All files made with no errors |
| Visual check | Looked at every new picture at full size: asset overview, candle sheet, palette card, 3 level maps, 4 screens, screen flow | Problems found and fixed: route line covering embers, overlapping labels, a wrong arrow in the screen flow, cut-off palette names |
| Piskel format check | Part of `check_project.py`: follows Piskel's loader rules (model version 2, frame size from the layout) | Passed, but **not** tested in Piskel itself |
| Figma | Not tested | The Figma editing tool reached its limit |

**What the automatic checks do not cover:** they don't play a real game (there is no game code yet), and they don't open Piskel or Figma.

## 3. Things you must do yourself

1. Rebuild the Figma prototype with the 4 new screens (about 15 minutes; steps in `04_UI_and_Prototype/UI_AND_PROTOTYPE.md`).
2. Test every Figma link in Present mode.
3. Set Figma sharing so your teacher can open the file.
4. Open one `.piskel` file and one PNG strip in Piskel to check them.
5. Fill in your details in `Submission_Document.md`.
6. Make sure your teacher can open the repository link.
