"""What phase one and the full trench would cost, priced per acre against caps that exist.

Each cap's cost is brought to 2026 dollars at 4% a year and divided by its acres. Built caps give
the low end (lower quartile) and the middle (median); estimates published since 2020 give the
high end (median). Those per-acre figures times the trench's acres are the ranges on the page.
Running this file also redraws ../charts/cost-per-acre.svg.
"""
import os
import _setup  # noqa: F401
from commons import fmt, path, quantile, read_csv
import area

NOW_YEAR = 2026
ESCALATION = 0.04
CHART_PLACES = {"freeway-park": "Seattle", "i-579-cap-frankie-pace-park": "I-579 cap, Pittsburgh",
                "klyde-warren-park": "Dallas", "margaret-t-hance-park-deck-park-tunnel": "Phoenix",
                "the-cap-at-union-station": "Columbus"}


def per_acre():
    rows = []
    for c in read_csv("shared", "caps.csv"):
        usd, year, acres = float(c["cost_usd"]), int(c["cost_year"]), float(c["acres"])
        rows.append({**c, "per_acre": usd * (1 + ESCALATION) ** (NOW_YEAR - year) / acres})
    return rows


def numbers():
    rows = per_acre()
    built = [r["per_acre"] for r in rows if r["set"] == "built"]
    recent = [r["per_acre"] for r in rows if r["set"] == "recent"]
    low, mid, high = quantile(built, 0.25), quantile(built, 0.5), quantile(recent, 0.5)
    a = area.numbers()
    out = {
        "built_caps": len(built),
        "recent_estimates": len(recent),
        "built_min_per_acre": min(built),
        "built_max_per_acre": max(built),
        "built_p25_per_acre": low,
        "built_median_per_acre": mid,
        "recent_median_per_acre": high,
        "phase_one_low": a["phase_one_acres"] * low,
        "phase_one_mid": a["phase_one_acres"] * mid,
        "phase_one_high": a["phase_one_acres"] * high,
        "trench_low": a["trench_acres"] * low,
        "trench_mid": a["trench_acres"] * mid,
        "trench_high": a["trench_acres"] * high,
    }
    for r in rows:
        if r["set"] == "built":
            out[f"per_acre:{r['id']}"] = r["per_acre"]
    return out


def chart():
    """The page's bar chart: each built cap per acre, then the median of recent estimates."""
    rows = sorted((r for r in per_acre() if r["set"] == "built"), key=lambda r: r["per_acre"])
    n = numbers()
    bars = [(f"{r['short_name']}, {CHART_PLACES.get(r['id'], r['place'])} ({r['cost_year']})", r["per_acre"], "#3f6b33") for r in rows]
    bars.append((f"Estimates published since 2020, median of {n['recent_estimates']}", n["recent_median_per_acre"], "#a3261b"))
    top = max(v for _, v, _ in bars)
    w, label_w, bar_w, row_h = 720, 330, 300, 34
    h = row_h * len(bars) + 16
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Cost per acre of highway caps in 2026 dollars">',
           '<style>text{font:14px "Source Serif 4",Georgia,serif;fill:#1a2321}.v{font:600 13px "IBM Plex Mono",Menlo,monospace}</style>']
    for i, (label, v, color) in enumerate(bars):
        y = 8 + i * row_h
        bw = bar_w * v / top
        out.append(f'<text x="0" y="{y + 18}">{label}</text>')
        out.append(f'<rect x="{label_w}" y="{y + 6}" width="{bw:.1f}" height="16" rx="2" fill="{color}"/>')
        out.append(f'<text class="v" x="{label_w + bw + 8:.1f}" y="{y + 19}">{fmt(v, "usd_m1")}</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


CHARTS = {"cap-i-95/charts/cost-per-acre.svg": chart}

if __name__ == "__main__":
    for k, v in numbers().items():
        print(f"{k:58} {v:,.0f}" if v > 100 else f"{k:58} {v}")
    with open(path("cap-i-95", "charts", "cost-per-acre.svg"), "w") as f:
        f.write(chart())
