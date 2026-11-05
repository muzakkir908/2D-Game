# Verification Report

*This report was written by the AI assistant that helped make this project (see `AI_Use_Note.md`). In this report, "I" and "me" mean the AI assistant.*

This report shows what was checked, how it was checked, and what is still left to do.

**Status words:**
- **Complete and verified:** the work is done and it was checked.
- **Complete but not tested:** the work is done, but one important test could not be done.
- **Incomplete:** the work is not finished.
- **Requires my attention:** the student must do something.

**Two kinds of checks are used:**
- **Automatic checks:** `tools/check_project.py`, `tools/test_prototype.js`, `tools/test_figma_plugin.js` and `tools/test_piskel.js`.
- **Checked by eye:** the pictures were opened and looked at, at full size.

## 1. Final assignment checklist

| Assignment requirement | Result | Evidence or file | Remaining work |
|---|---|---|---|
| Game concept and rules | Complete and verified | `01_Game_Concept/WICKLIGHT_Game_Design_Document.md`. All 17 sections read through. Its numbers (3 lives, 60 s, 5 embers, 2 moths, 3 spike groups) match the level and screens (automatic check). | – |
| Original player sprite | Complete and verified | `02_Pixel_Art_Assets/sprites/player/`: idle (2 frames), walk (4), jump (1), all 16 × 16. Automatic: frames line up, no stray pixels, no duplicates. Checked by eye. | – |
| Environment tiles | Complete and verified | `tiles/`: ground top, ground, platform, spikes, plus `tileset.png` (64 × 16). `background/cave_background.png`. Tiles join correctly on the level map (checked by eye). | – |
| Collectibles | Complete and verified | `sprites/ember/` (2 frames). Checked by eye. | – |
| Hazards and enemies | Complete and verified | `sprites/moth/` (2 frames), `tiles/3_spikes.png`. Checked by eye. | – |
| Sprite sheet | Complete and verified | `spritesheets/wicklight_spritesheet.png` and 6 strips. Automatic: every row matches its strip, and every strip matches the single PNGs pixel for pixel. | – |
| PNG exports | Complete and verified | Automatic: all sprite PNGs are RGBA with see-through backgrounds, no half-transparent pixels, only the 16 palette colours, sizes are multiples of 16. Palette: `palette/wicklight.gpl`. | – |
| Piskel compatibility | Complete and verified | All 6 `.piskel` files were opened in the **real Piskel editor** (Piskel's open-source code, run in a browser on my work computer, because the piskelapp.com website is blocked there). Opened through Piskel's own Import panel; size, frame count, frame order, speed, palette colours and transparency checked; one pixel drawn with the Pen tool and undone; a PNG exported from Piskel and compared pixel by pixel with the original strip: **49 of 49 checks passed**. Evidence: `05_Documentation/piskel_test_evidence/`. | – (optional: open one file on piskelapp.com yourself) |
| Complete level map | Complete and verified | `03_Level_Design/level_map_x3.png`, `level_map_grid.png`, `data/level.txt`, `data/level.tmj`. One screen, 24 × 12 tiles. Checked by eye. | – |
| Annotated player route | Complete and verified | `level_map_annotated_x3.png`: route, 8 numbered notes, legend, moth paths. Checked by eye at full size. | – |
| Challenge design | Complete and verified | `LEVEL_DESIGN.md`. Automatic jump check: every route jump is at most 3 tiles up and 4 tiles across, and all 5 embers and the door can be reached (`data/jump_check_result.json`). Clear beginning, middle and end. | – |
| Main menu | Complete and verified | `04_UI_and_Prototype/screens/01_main_menu.png` (1920 × 1080): title, background, PLAY, SETTINGS, EXIT. Checked by eye: nothing overlaps. | – |
| Gameplay screen | Complete and verified | `screens/02_gameplay.png`: candle, cave, 3 platforms, all 5 embers, 2 moths, 3 spike groups, door, 3 hearts, timer 0:58, ember counter 0/5, goal text. Checked by eye; numbers checked automatically. | – |
| Victory screen | Complete and verified | `screens/03_victory.png`: message, 5/5 embers, time left, lives left, "LEVEL COMPLETE", REPLAY, MAIN MENU. Checked by eye. | – |
| Game-over screen | Complete and verified | `screens/04_game_over.png`: message, 3/5 embers, reason, time left, RETRY, MAIN MENU. Checked by eye. | – |
| Interactive Figma prototype | Requires my attention | The Figma file still shows the old game: the Figma editing tool is still at the Starter plan's limit (checked again). Instead, I made a **Figma plugin** (`04_UI_and_Prototype/figma_plugin/`) that builds the 4 frames, 7 buttons, click areas, 11 links and the starting screen in one click. Its logic passed 36 of 36 checks in a test outside Figma (`tools/test_figma_plugin.js`). It has **not** been run inside Figma yet. The HTML prototype has the same links and passed 27 of 27 checks. | Run the plugin in the Figma desktop app (3 minutes), test in Present mode, set sharing |
| Submission document | Requires my attention | `05_Documentation/Submission_Document.md`: description, links and all project files. All links work (automatic). | Fill in your name, student number, course, assignment title, date, Figma link and GitHub link |
| Repository organisation | Complete and verified | Folders 01–05 plus `tools/`. Automatic: all document links and images work, no old-version words in documents or code, no duplicate sprites. Rebuilding twice gives the same files. | Check that your teacher can open the GitHub link |

## 2. Tests performed in this session

| Test | How | Result |
|---|---|---|
| Rebuild from source | `python3 tools/build_all.py` | Worked, no errors |
| Rebuild gives the same files | Ran the build twice and compared | No differences |
| Project checks | `python3 tools/check_project.py` | **37 of 37 passed** |
| HTML prototype | `node tools/test_prototype.js` (Chromium browser) | **27 of 27 passed**: starts on the Main Menu, all 11 links, Settings and Exit messages, Enter and Esc keys, all images load, no sideways scroll at phone width, no errors |
| Level jump check | Part of the build | Passed: 5 embers, 2 moths, 3 spike groups, everything reachable |
| Figma guide matches the prototype | Part of the project checks | All 11 click areas match exactly |
| Checked by eye | The 4 screens, the asset overview, the annotated level map | No overlaps, readable text, the same style everywhere |
| Figma editing | One read-only call | **Failed:** plan limit reached. No edits were made. |
| Figma plugin (logic) | `node tools/test_figma_plugin.js`: runs the plugin code with a pretend Figma | **36 of 36 passed**: 4 frames at 1920 × 1080, exact screen PNGs, 7 buttons, 11 correct links, Main Menu as start, old pages kept as backup |
| Figma plugin (in Figma) | – | **Not done:** Figma editing is blocked for me |
| Figma Present mode | – | **Not done** (Figma not available to me) |
| Piskel website | Tried to connect | **Failed:** blocked by the network rules of my work environment |
| Piskel editor (real app) | `tools/test_piskel.js`: Piskel's own source code, run in Chromium | **49 of 49 passed** for all 6 files: open, check, edit with the Pen tool, undo, export PNG, compare. Screenshots checked by eye. |

**What the automatic checks do not prove:** there is no game code yet, so nothing was actually played. The Figma plugin was tested outside Figma only. Piskel was tested with the real Piskel editor code, but on my work computer, not on piskelapp.com.

## 3. Fixes made in this session

| Problem | Fix |
|---|---|
| The Gameplay screen showed only 3 of the 5 embers (2 already collected) and 0:41 on the timer. The Figma brief asks for five embers and a 60-second timer. | The Gameplay screen now shows the start of the run: all 5 embers, 0/5, 0:58 and 3 full hearts. The candle is hopping towards the first ember (this also shows the jump sprite). |
| The code still called the font "Belfry" (a name from the old version). | Renamed it to "WICKLIGHT pixel font". |
| There was no full Figma rebuild guide. | Added `04_UI_and_Prototype/Figma_Rebuild_Guide.md` with exact sizes, positions, click areas, links, starting screen, a test list and sharing steps. |
| The AI use note had been deleted, but it is a required document. | Added it again, without naming a product. It has spaces for you to fill in what your college asks for. |
| The submission document had no assignment title field and no blank fields for the links. | Added them. |
| The Piskel guide had no steps for checking a file. | Added a short checklist. |
| The checks did not cover the required documents, the Figma guide numbers or old words in the code. | Added 4 new automatic checks (33 → 37). |
| Figma could not be edited by me. | Made a one-click Figma plugin (`04_UI_and_Prototype/figma_plugin/`) and a test for it. Added a "Quick way" to the Figma guide. |
| The `.piskel` files had never been opened in Piskel. | Ran the real Piskel editor (its open-source code) in a browser and tested all 6 files. Saved the results, screenshots and exported PNGs in `piskel_test_evidence/`. |

## 4. The 125 files removed in the redesign

Each group of removed files was checked against the new version. No required work is missing.

| Removed (old version) | Why it was removed | Replaced by (new version) |
|---|---|---|
| Old player sprites and strips (9 frames, 5 animations) | Old character | Candle: idle, walk, jump (7 frames, 3 strips) |
| Old collectibles (ember, wax drop, bell shard) | Wax and shards were removed from the game | Ember (2 frames) |
| Old hazards (frost moth, icicle) | Icicles were removed from the game | Moth (2 frames) and spikes tile |
| Old objects (sconce, Great Bell) | Checkpoints and the bell were removed | Exit door (closed and open) |
| Old 16-tile tileset and tile files | Too many tiles for a beginner project | 4 tiles + `tileset.png` + cave background |
| Old UI buttons, icons, panels, font sheet | Old style and colours | New buttons, icons, panel, font sheet |
| Old palette files (28 colours) | Old colours | New 16-colour palette |
| Old preview sheets | Old art | `asset_overview_x4.png`, `candle_sheet_x8.png` |
| Old level maps and 4 section close-ups, old level data | 96-tile, 4-section level | One-screen level: 3 maps + 4 data files |
| Old 5 screens (including Settings) and flow diagram | Old game; only 4 screens needed | 4 new screens + `screen_flow.png` |
| Old prototype images | Old screens | New prototype images |
| `tools/wl.py` | Old art library | `tools/art.py` and `tools/font.py` |

## 5. What you must do before submitting

1. **Build the Figma prototype:** run the plugin in the Figma desktop app (Quick way in `04_UI_and_Prototype/Figma_Rebuild_Guide.md`).
2. **Test it in Present mode:** tick the list in Step 7 of the guide.
3. **Share it:** set "Anyone with the link can view" and copy the link.
4. **Fill in `Submission_Document.md`:** name, student number, course, assignment title, date, Figma link and GitHub link.
5. **Fill in `AI_Use_Note.md`:** add your own work, and check the note against your college's rules.
6. **Check the GitHub link:** make sure your teacher can open it. If the repository is private, add your teacher or upload a ZIP of the project to Moodle.
7. **Delete the old branch `ccr-d1b522b6-hxi5qm`** on GitHub (Branches page → trash icon). It holds only an old empty commit.
