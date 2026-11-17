"""Draws the two section diagrams for the Cap I-95 study into section-long.svg and section-cross.svg.

Long section: along I-95 from just north of Atwells Ave to just south of Westminster St, seen from
Federal Hill looking east. Block lengths are the plan pieces' acres over the deck's average width.
Cross section: across the trench at the park, true scale. Lanes from FHWA HPMS 2024 (6 through
lanes, 12 ft, 13 ft median between Westminster St and Broadway).
"""
import os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools"))
from commons import feature_acres, geojson  # noqa: E402

plan = {f["properties"]["block"]: feature_acres(f) for f in geojson("cap-i-95", "maps", "phase-one.geojson")["features"]}
plan["P1"] = sum(plan.values())
DECK_FT = 1700
tot = plan["A"] + plan["B"] + plan["C"]
A_FT = DECK_FT * plan["A"] / tot          # Atwells to Broadway
B_FT = DECK_FT * plan["B"] / tot          # Broadway to Washington
WIDTH_FT = round(plan["P1"] * 43560 / DECK_FT / 10) * 10

FONT = 'font-family="Archivo, Helvetica Neue, Arial, sans-serif"'
MONO = 'font-family="IBM Plex Mono, Menlo, monospace"'
INK, INK3, RULE = "#1b2124", "#566166", "#8e9897"
DECK, DECK_LINE = "#f2c230", "#9a7a12"
TUNNEL, ROAD, SOIL, WALL = "#2f3638", "#5d6567", "#d8d1c1", "#c3c8c6"
LAWN, TREE, TRUNK = "#6fae55", "#4c9a3f", "#6b5a45"
HOME, HOME_LINE, SHOP = "#dfe7f5", "#4470b8", "#f6d58b"
BLDG, BLDG_LINE = "#e3e6e4", "#a3acaa"
CARS = ["#e8ecea", "#b9c0be", "#7d8a8f", "#c25b4a", "#4f6d8f", "#d9d4c4", "#9aa4a2"]


def car(x, y, w=13, h=7, fill=None):
    return f'<rect x="{x:.1f}" y="{y - h:.1f}" width="{w}" height="{h}" rx="2" fill="{fill}"/>'


def tree(x, base, h, r):
    return (f'<line x1="{x:.1f}" y1="{base}" x2="{x:.1f}" y2="{base - h * .55:.1f}" stroke="{TRUNK}" stroke-width="2.4"/>'
            f'<circle cx="{x:.1f}" cy="{base - h + r:.1f}" r="{r}" fill="{TREE}" fill-opacity=".9"/>')


def person(x, base, s=1.0, fill=INK):
    return (f'<circle cx="{x:.1f}" cy="{base - 11 * s:.1f}" r="{2.2 * s:.1f}" fill="{fill}"/>'
            f'<line x1="{x:.1f}" y1="{base - 8.5 * s:.1f}" x2="{x:.1f}" y2="{base:.1f}" stroke="{fill}" stroke-width="{2.2 * s:.1f}" stroke-linecap="round"/>')


def text(x, y, s, size=17, weight=600, anchor="middle", fill=INK, mono=False, extra=""):
    fam = MONO if mono else FONT
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {fam}{extra}>{s}</text>'


def long_section():
    W, H = 1000, 400
    k = 940 / 2200                     # px per foot along the road
    X = lambda ft: 30 + (ft + 250) * k
    Y0, V = 250, 2.0                   # street level, px per foot of height
    under, road = Y0 + 10, Y0 + 24 * V
    streets = [("Atwells Ave", 0, 60), ("Broadway", A_FT, A_FT + 60),
               ("Washington St", A_FT + B_FT, A_FT + B_FT + 60), ("Westminster St", DECK_FT - 60, DECK_FT)]
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Long section along I-95 from just north of Atwells Ave to just south of Westminster St. North of Atwells and south of Westminster the highway is an open trench. Between them a deck about 1,700 feet long sits at street level over the highway, which keeps running underneath in a tunnel. On the deck: apartment buildings from Atwells Ave to Broadway, then a park to Westminster St, with Broadway and Washington St crossing at street level and emergency stairs from the tunnel up to those two streets.">']
    # ground under the road, road, open-trench far walls, tunnel
    o.append(f'<rect x="{X(-250)}" y="{road}" width="{X(1950) - X(-250)}" height="16" fill="{SOIL}"/>')
    for a, b in [(-250, 0), (DECK_FT, 1950)]:
        o.append(f'<rect x="{X(a):.1f}" y="{Y0}" width="{X(b) - X(a):.1f}" height="{road - Y0}" fill="{WALL}"/>')
        o.append(f'<line x1="{X(a):.1f}" y1="{Y0}" x2="{X(b):.1f}" y2="{Y0}" stroke="{RULE}" stroke-width="2"/>')
        o.append(text((X(a) + X(b)) / 2, road - 18, "Open trench", 14, 600, fill=INK))
    o.append(f'<rect x="{X(0):.1f}" y="{under}" width="{X(DECK_FT) - X(0):.1f}" height="{road - under}" fill="{TUNNEL}"/>')
    for ft in range(25, DECK_FT, 70):
        o.append(f'<circle cx="{X(ft):.1f}" cy="{under + 3}" r="1.6" fill="#ffd34d"/>')
    o.append(f'<rect x="{X(-250)}" y="{road}" width="{X(1950) - X(-250)}" height="3" fill="{ROAD}"/>')
    # traffic, both ends and the tunnel
    rnd = random.Random(7)
    ft = -235
    while ft < 1930:
        truck = rnd.random() < .16
        o.append(car(X(ft), road, 26 if truck else 13, 13 if truck else 7, rnd.choice(CARS[:3]) if truck else rnd.choice(CARS)))
        ft += rnd.uniform(55, 110)
    o.append(text(X(A_FT + 30 + B_FT / 2), road - 15, "I-95 keeps running underneath, in a tunnel", 15, 650, fill="#ffffff"))
    # exit stairs at the two middle cross streets
    for _, a, b in streets[1:3]:
        cx = X((a + b) / 2)
        o.append(f'<rect x="{cx - 5:.1f}" y="{under}" width="10" height="{road - under}" fill="#8e9897"/>')
        for i in range(5):
            yy = road - 4 - i * 6.5
            o.append(f'<line x1="{cx - 4:.1f}" y1="{yy:.1f}" x2="{cx + 4:.1f}" y2="{yy - 4:.1f}" stroke="{INK}" stroke-width="1.2"/>')
    # the deck
    o.append(f'<rect x="{X(0):.1f}" y="{Y0}" width="{X(DECK_FT) - X(0):.1f}" height="{under - Y0}" fill="{DECK}" stroke="{DECK_LINE}" stroke-width="1.2"/>')
    # homes, Atwells to Broadway
    blocks = [(64, 172), (184, 292), (304, A_FT - 4)]
    for a, b in blocks:
        x0, x1, top = X(a), X(b), Y0 - 68 * V
        o.append(f'<rect x="{x0:.1f}" y="{top:.1f}" width="{x1 - x0:.1f}" height="{Y0 - top:.1f}" fill="{HOME}" stroke="{HOME_LINE}" stroke-width="1.4"/>')
        o.append(f'<rect x="{x0 + 2:.1f}" y="{Y0 - 14:.1f}" width="{x1 - x0 - 4:.1f}" height="11" fill="{SHOP}"/>')
        for f in range(1, 6):
            yy = Y0 - 14 - f * 21.5 + 6
            xx = x0 + 6
            while xx + 6 < x1 - 3:
                o.append(f'<rect x="{xx:.1f}" y="{yy:.1f}" width="6" height="9" fill="#9fb4dc"/>')
                xx += 12
    o.append(text((X(64) + X(A_FT - 4)) / 2, Y0 - 68 * V - 12, "Homes and shops", 17, 700, fill=HOME_LINE))
    # park, Broadway to Westminster
    for a, b in [(A_FT + 60, A_FT + B_FT), (A_FT + B_FT + 60, DECK_FT - 60)]:
        o.append(f'<rect x="{X(a):.1f}" y="{Y0 - 4}" width="{X(b) - X(a):.1f}" height="4" fill="{LAWN}"/>')
        t = a + 30
        while t < b - 25:
            o.append(tree(X(t), Y0 - 4, 30 * V, 13))
            t += rnd.uniform(55, 80)
        for p in range(int((b - a) / 140)):
            o.append(person(X(a + 60 + p * 140 + rnd.uniform(0, 40)), Y0 - 4))
    o.append(text(X(A_FT + 60 + (B_FT - 60) / 2), Y0 - 30 * V - 16, "Park", 19, 700, fill="#2f6b27"))
    # cross streets on the deck, labelled up top
    for name, a, b in streets:
        cx = X((a + b) / 2)
        o.append(f'<rect x="{X(a):.1f}" y="{Y0 - 4}" width="{X(b) - X(a):.1f}" height="4" fill="#6b7375"/>')
        o.append(f'<line x1="{cx:.1f}" y1="44" x2="{cx:.1f}" y2="{Y0 - 6}" stroke="{RULE}" stroke-width="1.2" stroke-dasharray="3 4"/>')
        o.append(text(cx, 34, name, 15, 650))
    # labels under the road
    lab_y = road + 34
    for s, ft in [("Tunnel opening", 0), ("Exit stairs", A_FT + 30), ("Exit stairs", A_FT + B_FT + 30), ("Tunnel opening", DECK_FT)]:
        o.append(f'<line x1="{X(ft):.1f}" y1="{road + 18}" x2="{X(ft):.1f}" y2="{lab_y - 13}" stroke="{INK3}" stroke-width="1.2"/>')
        o.append(text(X(ft), lab_y, s, 13, 500, fill=INK3, mono=True))
    # length of the deck and compass
    dy = H - 22
    o.append(f'<line x1="{X(0):.1f}" y1="{dy}" x2="{X(DECK_FT):.1f}" y2="{dy}" stroke="{INK}" stroke-width="1.6"/>')
    for ft in (0, DECK_FT):
        o.append(f'<line x1="{X(ft):.1f}" y1="{dy - 7}" x2="{X(ft):.1f}" y2="{dy + 7}" stroke="{INK}" stroke-width="1.6"/>')
    mid = X(DECK_FT / 2)
    o.append(f'<rect x="{mid - 92:.1f}" y="{dy - 12}" width="184" height="24" fill="var(--card, #f9faf9)"/>')
    o.append(text(mid, dy + 5, "Deck: about 1,700 feet", 15, 650))
    o.append(text(X(-250), dy + 5, "← North", 13, 500, "start", INK3, True))
    o.append(text(X(1950), dy + 5, "South →", 13, 500, "end", INK3, True))
    o.append("</svg>")
    return "\n".join(o)


def cross_section():
    W, H = 1000, 350
    k = 2.3                              # px per foot, both ways
    Y0 = 186
    under, road = Y0 + 5 * k, Y0 + 24 * k
    L, R = 500 - WIDTH_FT * k / 2, 500 + WIDTH_FT * k / 2
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Cross section across the trench at the park, drawn to scale: Federal Hill on the left, Downcity on the right, both at street level. The deck spans the trench, about {WIDTH_FT} feet, at street level, with lawn, trees and people on it. Underneath, in a tunnel, I-95 keeps its three lanes each way and its ramps, with supports between the lanes.">']
    # neighbourhoods
    o.append(f'<rect x="0" y="{Y0}" width="{L:.1f}" height="{H - 40 - Y0}" fill="{SOIL}"/>')
    o.append(f'<rect x="{R:.1f}" y="{Y0}" width="{W - R:.1f}" height="{H - 40 - Y0}" fill="{SOIL}"/>')
    o.append(f'<rect x="{L:.1f}" y="{road:.1f}" width="{R - L:.1f}" height="{H - 40 - road:.1f}" fill="{SOIL}"/>')
    for x0, w, h in [(18, 64, 34), (92, 64, 38), (166, 58, 32)]:
        top = Y0 - h * k
        o.append(f'<path d="M{x0} {Y0} V{top:.1f} L{x0 + w / 2:.1f} {top - 22:.1f} L{x0 + w} {top:.1f} V{Y0} Z" fill="{BLDG}" stroke="{BLDG_LINE}" stroke-width="1.2"/>')
    for x0, w, h in [(R + 14, 84, 62), (R + 108, 120, 74)]:
        o.append(f'<rect x="{x0:.1f}" y="{Y0 - h * k:.1f}" width="{w}" height="{h * k:.1f}" fill="{BLDG}" stroke="{BLDG_LINE}" stroke-width="1.2"/>')
    o.append(person(L - 30, Y0) + person(R + 40, Y0))
    # tunnel, lanes, supports, traffic
    o.append(f'<rect x="{L:.1f}" y="{under:.1f}" width="{R - L:.1f}" height="{road - under:.1f}" fill="{TUNNEL}"/>')
    o.append(f'<rect x="{L:.1f}" y="{road:.1f}" width="{R - L:.1f}" height="3" fill="{ROAD}"/>')
    med = 13 * k / 2
    inner, lane, outer = 3 * k, 12 * k, 10 * k
    lanes = []
    for side in (-1, 1):
        start = 500 + side * (med + inner)
        for i in range(3):
            lanes.append(start + side * (lane * i + lane / 2))
    edge_l, edge_r = 500 - med - inner - 3 * lane - outer, 500 + med + inner + 3 * lane + outer
    for x in (500, edge_l, edge_r):
        o.append(f'<rect x="{x - 5:.1f}" y="{under:.1f}" width="10" height="{road - under:.1f}" fill="#8e9897"/>')
    o.append(f'<rect x="{500 - med:.1f}" y="{road - 8:.1f}" width="{2 * med:.1f}" height="8" fill="#9aa4a2"/>')
    ramps = [(L + edge_l) / 2, (edge_r + R) / 2]
    rnd = random.Random(3)
    for i, x in enumerate(lanes):
        if i in (1, 4):
            continue
        o.append(car(x - 7, road, 14, 12, rnd.choice(CARS)))
    o.append(car(ramps[1] - 10, road, 20, 31, CARS[1]))
    o.append(car(ramps[0] - 7, road, 14, 12, CARS[5]))
    for x in range(int(L) + 18, int(R), 46):
        o.append(f'<circle cx="{x}" cy="{under + 3:.1f}" r="1.6" fill="#ffd34d"/>')
    # deck and park
    o.append(f'<rect x="{L:.1f}" y="{Y0}" width="{R - L:.1f}" height="{under - Y0:.1f}" fill="{DECK}" stroke="{DECK_LINE}" stroke-width="1.2"/>')
    o.append(f'<rect x="{L:.1f}" y="{Y0 - 4}" width="{R - L:.1f}" height="4" fill="{LAWN}"/>')
    for x in (L + 40, L + 125, R - 125, R - 40):
        o.append(tree(x, Y0 - 4, 30 * k, 16))
    for x in (L + 200, L + 232, R - 210, R - 180):
        o.append(person(x, Y0 - 4, 1.15))
    o.append(text(500, Y0 - 34 * k, "Park, at street level", 17, 700, fill="#2f6b27"))
    # callouts
    o.append(f'<line x1="{R - 2:.1f}" y1="{(Y0 + under) / 2:.1f}" x2="{R + 22:.1f}" y2="{under + 18:.1f}" stroke="{INK3}" stroke-width="1.2"/>')
    o.append(text(R + 26, under + 23, "Deck", 14, 650, "start"))
    o.append(text(500, road + 21, "I-95: three lanes each way and ramps, with supports between them", 12.5, 500, fill=INK, mono=True))
    o.append(text(L / 2, road + 21, "Federal Hill", 16, 700, fill=INK))
    o.append(text((R + W) / 2, road + 21, "Downcity", 16, 700, fill=INK))
    dy = H - 22
    o.append(f'<line x1="{L:.1f}" y1="{dy}" x2="{R:.1f}" y2="{dy}" stroke="{INK}" stroke-width="1.6"/>')
    for x in (L, R):
        o.append(f'<line x1="{x:.1f}" y1="{dy - 7}" x2="{x:.1f}" y2="{dy + 7}" stroke="{INK}" stroke-width="1.6"/>')
    o.append(f'<rect x="{500 - 74}" y="{dy - 12}" width="148" height="24" fill="var(--card, #f9faf9)"/>')
    o.append(text(500, dy + 5, f"about {WIDTH_FT} feet", 15, 650))
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    open(os.path.join(HERE, "section-long.svg"), "w").write(long_section())
    open(os.path.join(HERE, "section-cross.svg"), "w").write(cross_section())
    print("A", round(A_FT), "B", round(B_FT), "width", WIDTH_FT)
