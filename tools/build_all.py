"""Makes every WICKLIGHT image and data file again.  Run:  python3 tools/build_all.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import build_assets  # noqa: E402
import build_level  # noqa: E402
import build_screens  # noqa: E402
import build_figma_plugin  # noqa: E402

if __name__ == "__main__":
    build_assets.main()
    print("assets  -> 02_Pixel_Art_Assets/")
    build_level.main()
    print("level   -> 03_Level_Design/")
    build_screens.main()
    print("screens -> 04_UI_and_Prototype/")
    build_figma_plugin.main()
    print("figma   -> 04_UI_and_Prototype/figma_plugin/")
