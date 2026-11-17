"""Helpers shared by the models and the number check. Standard library only, so the check runs anywhere."""
import csv
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EARTH_R = 6378137.0
SQ_M_PER_ACRE = 4046.8564224


def path(*parts):
    return os.path.join(ROOT, *parts)


def read_csv(*parts):
    with open(path(*parts), newline="") as f:
        return list(csv.DictReader(f))


def metrics(study, name):
    """A data file shaped metric,value,unit,source_ids,note as {metric: float}."""
    return {r["metric"]: float(r["value"]) for r in read_csv(study, "data", name)}


def ring_acres(ring):
    """Area of one [lng, lat] ring on a local flat projection, which is accurate to well under 1% at city scale."""
    lat0 = math.radians(sum(p[1] for p in ring) / len(ring))
    xy = [(math.radians(p[0]) * EARTH_R * math.cos(lat0), math.radians(p[1]) * EARTH_R) for p in ring]
    a = sum(xy[i][0] * xy[i + 1][1] - xy[i + 1][0] * xy[i][1] for i in range(len(xy) - 1))
    return abs(a) / 2 / SQ_M_PER_ACRE


def feature_acres(feature):
    g = feature["geometry"]
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    # outer ring minus holes
    return sum(ring_acres(p[0]) - sum(ring_acres(h) for h in p[1:]) for p in polys)


def geojson(*parts):
    with open(path(*parts)) as f:
        return json.load(f)


def quantile(values, q):
    """Linear interpolation between closest ranks, the same rule the Commons Atlas uses."""
    a = sorted(values)
    if not a:
        return None
    i = (len(a) - 1) * q
    lo, hi = math.floor(i), math.ceil(i)
    return a[lo] + (a[hi] - a[lo]) * (i - lo)


def _round_to(v, step):
    return round(v / step) * step


def _trim(s):
    return s[:-2] if s.endswith(".0") else s


FORMATS = {
    "int": lambda v: f"{round(v):,}",
    "num1": lambda v: f"{v:.1f}",
    "pct": lambda v: f"{round(v * 100)}%",
    "usd": lambda v: f"${round(v):,}",
    "usd10": lambda v: f"${_round_to(v, 10):,.0f}",
    "usd100": lambda v: f"${_round_to(v, 100):,.0f}",
    "usd_m1": lambda v: f"${v / 1e6:.1f}M",
    "usd_m2": lambda v: f"${v / 1e6:.2f}M",
    "usd_m": lambda v: f"${v / 1e6:,.0f}M",
    "usd_m10": lambda v: f"${_round_to(v / 1e6, 10):,.0f}M",
    "usd_b": lambda v: "$" + _trim(f"{_round_to(v / 1e9, 0.5):.1f}") + "B",
    # the same amounts as the page's sentences write them
    "usd_mn": lambda v: f"${v / 1e6:,.0f} million",
    "usd_mn1": lambda v: f"${v / 1e6:,.1f} million",
    "usd_mn2": lambda v: f"${v / 1e6:,.2f} million",
    "usd_mn10": lambda v: f"${_round_to(v / 1e6, 10):,.0f} million",
    "usd_bn": lambda v: "$" + _trim(f"{_round_to(v / 1e9, 0.5):.1f}") + " billion",
}


def fmt(value, kind):
    return FORMATS[kind](value)
