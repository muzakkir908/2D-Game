# Level 1: The Drowned Belfry · Level Design

![Annotated level layout](level_01_annotated_design_x2.png)

| | |
|---|---|
| **Size** | 96 × 14 tiles (1536 × 224 px), 16 px tiles |
| **Structure** | 4 sections × 24 tiles. Each section is exactly one screen wide at 384 × 216, so the camera only ever shows one "room's worth" of ideas. |
| **Contents** | 24 embers · 3 wax drops · 3 bell shards · 4 frost moths · 4 icicles · 3 sconces · 1 Great Bell |
| **Par time** | about 2:30 for a safe run, 3:00+ for a full-collection run (wax starts at 3:00) |
| **Design rules** | Max climb **3 tiles**, max gap **4 tiles** (matches Pip's jump: 3.3 tiles high, 4.3 tiles long). Every jump in the level is within those limits. |

**Files**

| File | What it is |
|---|---|
| `level_01_annotated_design_x2.png` | Full map + main route (amber) + risk routes (red) + 19 numbered callouts + difficulty curve |
| `level_01_map_clean_x3.png` | Clean art-only map |
| `level_01_map_grid_coords.png` | Map with tile grid and X/Y coordinates for rebuilding in an engine |
| `section_1…4_*_x3.png` | Close-ups of each section with annotations |
| `data/level_01.tmj` | **Tiled** map (Background + Terrain tile layers, Entities object layer) |
| `data/level_01_terrain.csv`, `data/level_01_background.csv` | Tile index grids (−1 = empty), for engines without a Tiled importer |
| `data/level_01_entities.json` | Every object with pixel and tile position |
| `data/level_01.txt` | The ASCII source the level is built from (easy to read and edit) |

### Legend (ASCII source)

```
#  stone (auto top/fill)     =  wooden plank (one-way)   %  crumbling stone
^  iron spikes (hazard)      ~  water surface (hazard)   w  deep water
c  hanging chain (decor)     P  player start             e  ember
d  wax drop                  b  bell shard               M  frost moth
I  icicle (ceiling hazard)   S  sconce checkpoint        G  great bell (2x2)
```

---

## Overall structure: beginning, middle, end

```
Difficulty
 10 |                                                         ___
    |                                              __/‾‾‾‾‾‾‾‾   |  ← peak: final exam
    |                          /‾‾‾‾\        /‾‾‾‾                |
    |            /‾‾‾\        /      \      /                     |
    |  __/‾‾\___/     \_____/        \____/                      |
  1 |_/  TEACH    ↑   CHOOSE    ↑   PRESSURE   ↑     EXAM         |
     0          sconce 1      sconce 2      sconce 3            bell (96)
```

Each section **introduces → combines → tests**, and every section ends at a sconce. After each spike in difficulty the player gets a "breath" and a chance to bank, so the decision to bank or push on comes up three times, with higher stakes each time.

---

## Section 1: The Wick-Room (tiles 0–23) · TEACH

![](section_1_the_wick_room_x3.png)

| # | Where | What and why |
|---|---|---|
| **1 START** | (3,10) | Flat, enclosed runway with a wall behind the player. Nothing can hurt you here, so the first 2 seconds are just "learn to move". |
| **2 FIRST EMBER** | (5,10) | Sits directly in the walking path, so it's impossible to miss. On pickup the GLOW meter fills to ×2 and the light radius grows. That teaches the core mechanic with zero words. |
| **3 FIRST GAP** | cols 6–7 | A 2-tile gap over water. Two embers float in an **arc over the gap**, so following the embers *is* the jump. This teaches that jumping is needed and that water hurts. |
| **4 WIDER GAP** | cols 13–15 | 3 tiles: the same lesson with less margin. One ember marks the apex. |
| **5 OPTIONAL SHELF** | planks at cols 16–20 | The first optional reward: 3 embers on a shelf you need a full-height jump to reach. **No enemy here**, so the first taste of greed is safe practice. |
| **6 SCONCE 1** | (22,10) | Placed right after the shelf, so the player reaches it carrying 5–8 embers at high glow. Touching it shows the BANK animation: score jumps, glow resets. **This teaches banking at the moment it matters most.** |

**How you can fail here:** only by falling into water (−1 life, respawn at start). Low stakes on purpose.

---

## Section 2: Moth Gallery (tiles 24–47) · CHOOSE

![](section_2_moth_gallery_x3.png)

| # | Where | What and why |
|---|---|---|
| **7 THE FORK** | plank at (27–29, 8) | The level splits. **Low road:** walk the floor, 3 embers, a wax drop, one spike pit. **High road:** jump up the planks, 5 embers + a bell shard, but a moth patrols it. Both routes are visible at once, so the choice is informed. |
| **8 FIRST MOTH** | (38,3) | Hovers just above the high road's ember line. At glow ×1 its detection radius (3.5 tiles) barely reaches the planks. At ×4–5 it covers the whole plank. Players who arrive greedy from section 1 (they skipped the sconce) get chased; players who banked can slip past. **The sconce lesson is tested right away.** |
| **9 SPIKE PIT** | cols 34–36 | The low road isn't free: one 3-tile spike jump. It also punishes falling off the high road. |
| **10 BELL SHARD 1** | (44,4) | At the end of the high road, across a 2-tile hop. It's banked instantly, so the high road pays out even if the moth hits you afterwards. |

**Where rewards are placed:** the riskier route has roughly double the points (5 embers at climbing glow + 250) versus the low road (3 embers + wax). The wax drop on the low road is a quiet hint that it's the "steady" route.

**How you can fail here:** moth contact (lose AT RISK pool), spikes (life + respawn at sconce 1).

---

## Section 3: The Flooded Nave (tiles 48–71) · PRESSURE

![](section_3_flooded_nave_x3.png)

| # | Where | What and why |
|---|---|---|
| **11 SCONCE 2** | (50,10) | Placed *before* the hard part so a failure here doesn't send you back through section 2. |
| **12 PILLAR + WAX** | (55–56, 10) | A safe stepping stone with a wax drop: refuel before the most time-sensitive stretch. |
| **13 CRUMBLE + ICE** | crumbles at (59–60, 9) and (63–64, 9) | The only footholds over 11 tiles of water **fall 0.6 s after landing**, and **icicles hang above them**. The player can't wait, and can't stand still to line up a jump. **Bell Shard 2** sits 2 tiles above the first crumble, so you have to jump *up* from a collapsing tile: a clear greed test with a short timer. |
| **14 MOTH OVER WATER** | (67,5) | Guards the landing. Getting hit here causes knockback, which can push you into the water: one mistake can cost twice. A high-glow player gets noticed from the crumbles. |

**Difficulty increase:** the first section where standing still is punished (crumbles, wax) and where enemy contact can chain into an environmental death.

---

## Section 4: Bell Climb (tiles 72–95) · EXAM

![](section_4_bell_climb_x3.png)

| # | Where | What and why |
|---|---|---|
| **15 SCONCE 3** | (73,10) | The last bank. Everything after this is a vertical climb over a spike floor, so smart players cash in here. The design hint is that the floor ahead is 11 tiles of spikes. |
| **16 THE CLIMB** | ledges (77–79, 8) → (81–83, 5) → plank (86–88, 5) | Each step is exactly 3 tiles up, Pip's maximum jump. Missing any step drops you onto the spikes. The jump rules from section 1 now have to be executed perfectly. |
| **17 MOTH + ICICLE** | moth (84,3), icicle (87,2), moth (89,7) | The first time both threat types share a screen. The moth above the gap and the icicle over the plank force the player to time the jump *between* threats. |
| **18 BELL SHARD 3** | (88,3) | Floats directly in the moth's airspace above the plank. One hop up to grab it, at the worst possible moment. The ultimate risk/reward test. |
| **19 THE GREAT BELL** | (92–93, 4–5) on the tower ledge | Touch to ring it: auto-banks everything and ends the level. A 2-tile gap from the plank, so the final jump is easy. The level ends on a satisfying moment, not a frustrating one. |

---

## Player route summary

* **Main (amber) route:** floor → gap jumps → sconce 1 → low road → spike jump → sconce 2 → pillar → crumbles → sconce 3 → three-step climb → bell. Uses only 2–3 tile jumps. A first-time player can finish with about 15 embers.
* **Risk (red) routes:** the section 1 shelf and the section 2 high road, plus the shard jumps in sections 3 and 4. Taking all of them is needed for rank **Sun**.

## How the level teaches (without text)

| Lesson | Taught by | Tested by |
|---|---|---|
| Embers = glow | Ember 2 in your path | Section 2 fork |
| Jumping | Ember arc over gap 1 | Bell Climb steps |
| Banking | Sconce right after the bonus shelf | Moth that punishes high glow straight after |
| Water/spikes hurt | Shallow 2-tile water gap | 11-tile spike floor in the climb |
| Moths chase brightness | Single moth with a clear "!" tell | Moth + icicle combo |
| Keep moving | Wax timer | Crumbling stones |

## Success and failure states

* **Succeed:** reach the bell with ≥1 life and >0:00 wax. Score = banked points + shards + wax bonus (+ no-hit bonus).
* **Fail:** lose 3 lives (hazards respawn you at the last sconce, enemies knock you back), or let the wax run out. Lost AT RISK points are gone for good, so even a successful run can be "poor" if the player was greedy at the wrong moment.
