"""Areas and lengths of the deck, from the outlines in ../maps.

The page states each phase's area rounded down to a tenth of an acre, so it never overstates the
land: 8.67 acres reads as 8.6. Block lengths are each block's area over the deck's average width.
"""
import math
import _setup  # noqa: F401
from commons import feature_acres, geojson

STUDY = "cap-i-95"
DECK_FT = 1700          # phase one's length along the trench, measured on the outline
SQ_FT_PER_ACRE = 43560


def floor_tenth(v):
    return math.floor(v * 10 + 1e-9) / 10


def numbers():
    trench = {f["properties"]["phase"]: feature_acres(f) for f in geojson(STUDY, "maps", "trench.geojson")["features"]}
    blocks = {f["properties"]["block"]: feature_acres(f) for f in geojson(STUDY, "maps", "phase-one.geojson")["features"]}
    p1, p2 = floor_tenth(trench[1]), floor_tenth(trench[2])
    deck = sum(blocks.values())
    width = round(trench[1] * SQ_FT_PER_ACRE / DECK_FT / 10) * 10
    return {
        "phase_one_acres": p1,
        "phase_two_acres": p2,
        "trench_acres": p1 + p2,
        "homes_block_acres": blocks["A"],
        "park_acres": blocks["B"] + blocks["C"],
        "deck_width_ft": width,
        "block_a_ft": DECK_FT * blocks["A"] / deck,
        "block_b_ft": DECK_FT * blocks["B"] / deck,
    }


if __name__ == "__main__":
    for k, v in numbers().items():
        print(f"{k:22} {v:,.2f}")
