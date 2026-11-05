# WICKLIGHT – Level Design

![Annotated level map](level_map_annotated_x3.png)

## The level

| | |
|---|---|
| **Size** | 24 × 12 tiles (one screen). Each tile is 16 × 16 pixels. |
| **Start** | Bottom left |
| **Exit door** | Bottom right |
| **Embers** | 5 |
| **Spikes** | 3 groups |
| **Moths** | 2 |
| **Platforms** | 3 floating stone platforms |
| **Time** | 60 seconds |

## Files

| File | What it is |
|---|---|
| `level_map_annotated_x3.png` | The map with the player route, numbered notes and a legend |
| `level_map_x3.png` | The map without notes |
| `level_map_grid.png` | The map with a tile grid and numbers, to rebuild it in a game engine |
| `data/level.txt` | The level written as letters (one letter = one tile) |
| `data/level.tmj` | The level for the Tiled map editor |
| `data/level_tiles.csv` | The tile numbers (−1 = empty) |
| `data/jump_check_result.json` | The result of the automatic jump check |

## Map legend

| On the map | Meaning | Letter in `level.txt` |
|---|---|:---:|
| Candle | Start point | `P` |
| Glowing dot | Ember | `e` |
| Purple moth | Moth (its start spot) | `M` |
| Grey points | Spikes | `^` |
| Stone ledge | Platform | `=` |
| Stone blocks | Ground and walls | `#` |
| Wooden door | Exit door | `D` |
| Yellow dashed line | Player route | – |
| Thin purple line | Where the moth flies | – |

## How the player moves through the level

| # | Where | What happens |
|:---:|---|---|
| 1 | Start | The candle starts on the left, on flat, safe ground. You can learn to move here. |
| 2 | Ember 1 | The first ember is on the ground, right in front of you. It is easy to get. |
| 3 | First spikes | Two spikes on the floor. This is the first jump you have to make. |
| 4 | Ember 2 | Jump up onto the first platform (3 tiles up) to get the second ember. |
| 5 | Moth + Ember 3 | Jump to the high platform. A moth flies left and right across it. Wait until it moves away, then get the ember. **This is the hardest part of the level.** |
| 6 | Spike pits | There are spikes under the platforms. If you fall, you lose a life and go back to the start. |
| 7 | Ember 4 | Drop down to the third platform. From here you can see the second moth on the floor below. |
| 8 | Ember 5 + Exit | Wait until the moth flies away, drop down, take the last ember and walk into the door. |

## Beginning, middle and end

- **Beginning (notes 1–3):** flat ground, one easy ember and one small spike jump. The player learns to move and jump.
- **Middle (notes 4–6):** the platforms, the first moth and the spike pits. This is where the challenge goes up.
- **End (notes 7–8):** one last moth to wait for, the last ember and the exit door.

## Where things are and why

- **Embers:** each one is a little harder to get than the one before. Ember 1 is on the ground, ember 2 needs a jump, ember 3 is next to a moth, ember 4 is high up, and ember 5 is next to the second moth.
- **Spikes:** they are under the jumps, so a missed jump is punished.
- **Moths:** one guards the high platform (the middle of the level), and one guards the way to the door (the end).
- **Exit door:** it is at the far right, at the end of the route, so the player always knows where to go.

## Jump check

Every jump on the route is possible. The candle can jump 3 tiles up and across a 4-tile gap.

| Jump | Up | Gap | OK? |
|---|:---:|:---:|:---:|
| Over the first spikes | 0 | 2 tiles | ✅ |
| Ground → platform 1 | 3 tiles | 0 | ✅ |
| Platform 1 → high platform | 2 tiles | 1 tile | ✅ |
| High platform → platform 3 | down 2 | 1 tile | ✅ |
| Platform 3 → ground | down 3 | 1 tile | ✅ |

This was checked automatically by `tools/build_level.py` (see `data/jump_check_result.json`). The check confirms that all 5 embers and the door can be reached from the start.
