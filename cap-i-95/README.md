# Cap the highway: Cap I-95

The study: [ajchatham.com/commons/cap-i-95](https://ajchatham.com/commons/cap-i-95/).

**The plan.** I-95 stays in its trench, with its lanes and its traffic. A deck at street level covers it from Atwells Ave to Westminster St, about 1,700 feet and 8.6 acres, built when RIDOT rebuilds the bridges over the trench. About 150 homes go on the block from Atwells Ave to Broadway, and a park covers the rest. Broadway and Washington St cross the deck as ordinary streets, and I-95 runs underneath in a tunnel.

## Files

| File | What it is |
| --- | --- |
| [`place.json`](place.json) | The place: the I-95 trench, in the commons tier, owned by RIDOT |
| [`captures/`](captures) | What exists: the 2023 and 1951–52 aerials, listed in `captures.csv` with where, when, who and license |
| [`data/traffic.csv`](data/traffic.csv) | Traffic and lanes between Westminster St and Broadway, from FHWA's 2024 highway data |
| [`data/bridges.csv`](data/bridges.csv) | The four bridges over the trench, their condition, and which two are in RIDOT's Connect Four project |
| [`data/connect-four.csv`](data/connect-four.csv) | Connect Four's planning grant and the state plan's money for the bridges |
| [`data/tax-near-trench.csv`](data/tax-near-trench.csv) | What every lot within 250 meters of the trench was billed in 2025 |
| [`data/apartment-buildings.csv`](data/apartment-buildings.csv) | The four buildings of 20 or more homes in that circle, which set the homes estimate |
| [`data/tax-rates.csv`](data/tax-rates.csv) | Providence's FY2027 tax rates |
| [`data/washington-bridge.csv`](data/washington-bridge.csv) | RIDOT's budgets for the Washington Bridge, which the study compares the cost to |
| [`maps/trench.geojson`](maps/trench.geojson) | The trench outline: phase one to Westminster St, phase two to Point St |
| [`maps/phase-one.geojson`](maps/phase-one.geojson) | Phase one in three blocks, split at the Broadway and Washington St bridges |
| [`models/area.py`](models/area.py) | Acres and lengths, from the maps |
| [`models/cost.py`](models/cost.py) | Cost per acre of caps that exist, and what phase one and the whole trench would cost at those rates |
| [`models/tax.py`](models/tax.py) | What the land near the trench pays, and what homes on the deck could pay |
| [`proposal/proposal.json`](proposal/proposal.json) | The change: what would be built, its phases, who decides, the next decision and where it stands |
| [`proposal/budget/phase-one.csv`](proposal/budget/phase-one.csv) | Phase one's budget lines. None has an amount yet; each needs a quote |
| [`numbers.csv`](numbers.csv) | Every number on the page that comes from this folder, written as the page shows it, and which file or model it comes from |
| [`charts/cost-per-acre.svg`](charts/cost-per-acre.svg) | The cost chart, drawn by `models/cost.py` |
| [`proposal/`](proposal) | Section drawings, concept renders and the prompts that made them, explained in [`IMAGES.md`](proposal/IMAGES.md) |
| [`CHANGES.md`](CHANGES.md) | Every change, dated, with who made it |

## What isn't here yet

- **The lot-by-lot tax join.** The tax totals come from joining the 2025 tax roll to the assessor's parcel layer for every lot within 250 meters of the outline. The totals are here; the join itself isn't yet.
- **The trench's depth.** The drawings put the road about 24 feet below the street. Nobody has measured it for this study.
- **Any engineering.** The cost is a range from other cities' caps, and the budget lines have no amounts. A structural engineer's correction to either is the most useful change this folder could get.
