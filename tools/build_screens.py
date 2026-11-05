"""Makes the 4 UI screens, the screen flow picture and the HTML prototype.

Screens are drawn at 384 x 216 pixels and saved 5 times bigger (1920 x 1080).
"""
import json
import os
import math
from PIL import Image, ImageDraw
import art
import level as L

OUT = os.path.join(os.path.dirname(__file__), "..", "04_UI_and_Prototype")
SW, SH, SCALE = 384, 216, 5
HUD_H = 24

# Button positions (x, y, width) - used for drawing AND for the prototype click areas.
MENU_BUTTONS = [("PLAY", 142, 86, 100), ("SETTINGS", 142, 110, 100), ("EXIT", 142, 134, 100)]
END_BUTTONS = [(102, 160, 86), (196, 160, 86)]      # left button, right button

# The game state shown on the screens (all numbers must match the rules).
START_LIVES = 3
START_TIME = 60
GAMEPLAY = {"lives": 3, "time": 41, "embers": 2}
VICTORY = {"lives": 2, "time": 18, "embers": 5}
GAME_OVER = {"lives": 0, "time": 26, "embers": 3, "reason": "NO LIVES LEFT"}


def mmss(sec):
    return "%d:%02d" % (sec // 60, sec % 60)


def candle(frame=0):
    return art.candle_frames()["candle_idle"][frame % 2]


def ground_strip(img, y):
    top = art.from_map(art.GROUND_TOP, 16, 16)
    for x in range(0, SW, 16):
        img.alpha_composite(top, (x, y))


def buttons_end(img, left, right):
    for (label, (x, y, w), sel) in ((left, END_BUTTONS[0], True), (right, END_BUTTONS[1], False)):
        img.alpha_composite(art.button(label, w=w, selected=sel), (x, y))


# ---------------------------------------------------------------- screens
def screen_menu(frame=0):
    img = art.background()
    ground_strip(img, 200)
    art.draw_text(img, "WICKLIGHT", SW // 2, 22, color='Y', sc=4, anchor='c')
    art.draw_text(img, "THE LITTLE CANDLE", SW // 2, 60, color='C', anchor='c')
    for (label, x, y, w) in MENU_BUTTONS:
        img.alpha_composite(art.button(label, w=w, selected=(label == "PLAY")), (x, y))
    img.alpha_composite(art.scale(candle(frame), 2), (40, 168))
    ember = art.from_map(art.EMBER_A if frame % 2 == 0 else art.EMBER_B, 16, 16)
    for (x, y) in [(300, 120), (330, 96), (80, 110)]:
        img.alpha_composite(ember, (x, y))
    moth = art.from_map(art.MOTH_UP if frame % 2 == 0 else art.MOTH_DOWN, 16, 16)
    img.alpha_composite(moth, (300, 150))
    art.draw_text(img, "ARROW KEYS = MOVE    SPACE = JUMP", SW // 2, 186, color='L', anchor='c')
    return img


def hud(img, lives, time, embers):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, SW - 1, HUD_H - 1], fill=art.rgba('K'))
    d.rectangle([0, 0, SW - 1, HUD_H - 3], fill=art.rgba('N'))
    for i in range(START_LIVES):
        img.alpha_composite(art.from_map(art.HEART if i < lives else art.HEART_EMPTY), (6 + i * 9, 8))
    img.alpha_composite(art.from_map(art.ICON_EMBER), (42, 8))
    art.draw_text(img, "%d/5" % embers, 50, 8, color='Y')
    img.alpha_composite(art.from_map(art.ICON_CLOCK), (80, 9))
    art.draw_text(img, mmss(time), 88, 8, color='C')
    art.draw_text(img, "GET 5 EMBERS, THEN GO TO THE DOOR", SW - 6, 8, color='L', anchor='r')


def moth_positions(frame):
    """Moth 1 is flying over the high platform, moth 2 is on the floor."""
    f = frame % 2
    return [(15 * 16 - 4 * f, 4 * 16, f), (18 * 16 + 4 * f, 9 * 16, 1 - f)]


def screen_gameplay(frame=0):
    img = Image.new("RGBA", (SW, SH), art.rgba('N'))
    taken = [(4, 9), (10, 6)]          # ember 1 (ground) and ember 2 (first platform)
    lvl = L.render(ember_taken=taken, moths=moth_positions(frame),
                   player=(candle(frame), 11 * 16, 6 * 16))
    img.alpha_composite(lvl, (0, HUD_H))
    hud(img, **GAMEPLAY)
    return img


def end_panel(img, title, title_col, line):
    img.alpha_composite(art.panel(200, 160), (92, 26))
    art.draw_text(img, title, SW // 2, 36, color=title_col, sc=2, anchor='c')
    art.draw_text(img, line, SW // 2, 58, color='C', anchor='c')


def ember_row(img, n, y):
    art.draw_text(img, "EMBERS", 108, y, color='L')
    for i in range(5):
        img.alpha_composite(art.from_map(art.ICON_EMBER if i < n else art.ICON_EMBER_EMPTY),
                            (200 + i * 8, y))
    art.draw_text(img, "%d/5" % n, 276, y, color='Y', anchor='r')


def screen_victory(frame=0):
    img = art.background()
    ground_strip(img, 200)
    img.alpha_composite(art.scale(art.from_map(art.door_rows(True)), 2), (340, 136))
    img.alpha_composite(art.scale(candle(frame), 2), (300, 168))
    end_panel(img, "YOU MADE IT!", 'Y', "THE CANDLE FOUND THE WAY OUT.")
    ember_row(img, VICTORY["embers"], 80)
    art.draw_text(img, "TIME LEFT", 108, 98, color='L')
    art.draw_text(img, mmss(VICTORY["time"]), 276, 98, color='C', anchor='r')
    art.draw_text(img, "LIVES LEFT", 108, 116, color='L')
    for i in range(START_LIVES):
        img.alpha_composite(art.from_map(art.HEART if i < VICTORY["lives"] else art.HEART_EMPTY),
                            (252 + i * 9, 116))
    art.draw_text(img, "LEVEL COMPLETE", SW // 2, 138, color='Y', anchor='c')
    buttons_end(img, "REPLAY", "MAIN MENU")
    return img


def screen_game_over(frame=0):
    img = art.background()
    ground_strip(img, 200)
    img.alpha_composite(Image.new("RGBA", (SW, SH), art.rgba('K', 90)))
    moth = art.from_map(art.MOTH_UP if frame % 2 == 0 else art.MOTH_DOWN, 16, 16)
    img.alpha_composite(art.scale(moth, 2), (318, 90))
    img.alpha_composite(art.scale(moth, 2), (34, 120))
    end_panel(img, "GAME OVER", 'R', "YOUR FLAME WENT OUT.")
    ember_row(img, GAME_OVER["embers"], 80)
    art.draw_text(img, "REASON", 108, 98, color='L')
    art.draw_text(img, GAME_OVER["reason"], 276, 98, color='C', anchor='r')
    art.draw_text(img, "TIME LEFT", 108, 116, color='L')
    art.draw_text(img, mmss(GAME_OVER["time"]), 276, 116, color='C', anchor='r')
    art.draw_text(img, "TRY AGAIN!", SW // 2, 138, color='Y', anchor='c')
    buttons_end(img, "RETRY", "MAIN MENU")
    return img


SCREENS = [("01_main_menu", screen_menu), ("02_gameplay", screen_gameplay),
           ("03_victory", screen_victory), ("04_game_over", screen_game_over)]


# ---------------------------------------------------------------- click areas (prototype)
def hotspots():
    def b(x, y, w):
        return [x, y, w, 17]
    return {
        "menu": {"img": "01_main_menu", "hint": "Click PLAY to start the game.", "hots": [
            {"r": b(142, 86, 100), "go": "game", "label": "Play", "btn": "play", "main": True},
            {"r": b(142, 110, 100), "msg": "Settings are not part of this prototype.", "label": "Settings", "btn": "settings"},
            {"r": b(142, 134, 100), "msg": "Thanks for playing! In the real game, this closes the game.",
             "label": "Exit", "btn": "exit"}]},
        "game": {"img": "02_gameplay",
                 "hint": "Click the DOOR to win. Click a MOTH or the SPIKES to lose your last life.",
                 "hots": [
                     {"r": [348, 150, 24, 36], "go": "win", "label": "Go into the door", "main": True},
                     {"r": [228, 84, 32, 24], "go": "lose", "label": "Touch moth 1"},
                     {"r": [280, 164, 32, 24], "go": "lose", "label": "Touch moth 2"},
                     {"r": [96, 170, 32, 14], "go": "lose", "label": "Touch spikes 1"},
                     {"r": [192, 170, 48, 14], "go": "lose", "label": "Touch spikes 2"},
                     {"r": [256, 170, 16, 14], "go": "lose", "label": "Touch spikes 3"}]},
        "win": {"img": "03_victory", "hint": "REPLAY plays the level again. MAIN MENU goes back.", "hots": [
            {"r": b(*END_BUTTONS[0]), "go": "game", "label": "Replay", "btn": "replay", "main": True},
            {"r": b(*END_BUTTONS[1]), "go": "menu", "label": "Main menu", "btn": "main_menu"}]},
        "lose": {"img": "04_game_over", "hint": "RETRY plays the level again. MAIN MENU goes back.", "hots": [
            {"r": b(*END_BUTTONS[0]), "go": "game", "label": "Retry", "btn": "retry", "main": True},
            {"r": b(*END_BUTTONS[1]), "go": "menu", "label": "Main menu", "btn": "main_menu"}]},
    }


def flow_diagram():
    th = {n: f(0).resize((192, 108), Image.NEAREST) for n, f in SCREENS}
    W, H = 640, 350
    im = Image.new("RGBA", (W, H), art.rgba('N'))
    art.draw_text(im, "HOW THE SCREENS CONNECT", W // 2, 8, color='Y', sc=2, anchor='c')
    pos = {"01_main_menu": (30, 50), "02_gameplay": (418, 50), "03_victory": (30, 200),
           "04_game_over": (418, 200)}
    names = {"01_main_menu": "MAIN MENU", "02_gameplay": "GAMEPLAY", "03_victory": "VICTORY",
             "04_game_over": "GAME OVER"}
    d = ImageDraw.Draw(im)
    for n, (x, y) in pos.items():
        d.rectangle([x - 2, y - 2, x + 193, y + 109], fill=art.rgba('L'))
        im.alpha_composite(th[n], (x, y))
        art.draw_text(im, names[n], x + 96, y + 113, color='C', anchor='c')

    def arrow(a, b, label=None, lp=None):
        d.line([a, b], fill=art.rgba('K'), width=4)
        d.line([a, b], fill=art.rgba('Y'), width=2)
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        p1 = (b[0] - 7 * math.cos(ang - 0.5), b[1] - 7 * math.sin(ang - 0.5))
        p2 = (b[0] - 7 * math.cos(ang + 0.5), b[1] - 7 * math.sin(ang + 0.5))
        d.polygon([b, p1, p2], fill=art.rgba('Y'))
        if label:
            art.draw_text(im, label, lp[0], lp[1], color='W', anchor='c')
    arrow((226, 90), (414, 90), "PLAY", (320, 78))
    arrow((418, 140), (226, 220), "REACH THE DOOR", (300, 160))
    arrow((226, 250), (430, 162))
    art.draw_text(im, "REPLAY", 350, 214, color='W', anchor='c')
    arrow((470, 168), (470, 196))
    art.draw_text(im, "NO LIVES OR", 462, 174, color='W', anchor='r')
    art.draw_text(im, "NO TIME", 462, 184, color='W', anchor='r')
    arrow((600, 196), (600, 168))
    art.draw_text(im, "RETRY", 592, 178, color='W', anchor='r')
    arrow((126, 196), (126, 172))
    art.draw_text(im, "MAIN MENU", 66, 180, color='W', anchor='c')
    # game over -> main menu: along the bottom and up the left side
    path = [(514, 331), (514, 342), (12, 342), (12, 100)]
    d.line(path, fill=art.rgba('K'), width=4)
    d.line(path, fill=art.rgba('Y'), width=2)
    arrow((12, 100), (26, 100))
    art.draw_text(im, "MAIN MENU", 300, 330, color='W', anchor='c')
    art.scale(im, 2).save(os.path.join(OUT, "screen_flow.png"))


def write_prototype_html():
    tpl = open(os.path.join(os.path.dirname(__file__), "prototype_template.html")).read()
    html = tpl.replace("/*SCREENS_JSON*/", json.dumps(hotspots(), indent=1))
    with open(os.path.join(OUT, "prototype", "index.html"), "w") as f:
        f.write(html)


def main():
    os.makedirs(os.path.join(OUT, "screens"), exist_ok=True)
    pimg = os.path.join(OUT, "prototype", "img")
    os.makedirs(pimg, exist_ok=True)
    for name, fn in SCREENS:
        art.scale(fn(0), SCALE).save(os.path.join(OUT, "screens", f"{name}.png"))
        for i in range(2):
            fn(i).save(os.path.join(pimg, f"{name}_f{i}.png"))
    for lbl, w in (("PLAY", 100), ("SETTINGS", 100), ("EXIT", 100), ("REPLAY", 86),
                   ("RETRY", 86), ("MAIN MENU", 86)):
        art.button(lbl, w=w, selected=True).save(
            os.path.join(pimg, f"button_{lbl.lower().replace(' ', '_')}.png"))
    flow_diagram()
    write_prototype_html()


if __name__ == "__main__":
    main()
