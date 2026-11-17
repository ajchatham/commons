# Proposals for the Commons: the data

Proposals for the Commons are long studies of how a public place could be used better, written by me, Andy Chatham. Each one says what the idea would cost, who would pay and who decides. This repo holds everything the numbers come from: the data, maps, models, budgets and images. Anyone can check them, and anyone can propose a change.

## What's here

| Folder | What it holds |
| --- | --- |
| [`shared/`](shared) | [`caps.csv`](shared/caps.csv): 17 highway caps with a reported cost or a recent estimate. [`sources.csv`](shared/sources.csv): every source, its link and the date it was read. [`maps/`](shared/maps): outlines of caps that exist, from OpenStreetMap. |
| [`cap-i-95/`](cap-i-95) | Cap the highway: a deck over I-95 between Federal Hill and Downcity in Providence. |
| [`tools/`](tools) | The number check. |

More studies move in as they're published.

## Propose a change

1. Open the file on GitHub and click the pencil. GitHub makes your own copy, so you don't need to ask first.
2. Change the number. Add where it comes from to [`shared/sources.csv`](shared/sources.csv): an id, a title, the link and the date you read it. Put that id in the row's `source_ids`.
3. Click "Propose changes" and say why in a sentence or two.

The number check runs on every pull request. It fails when a number has no source, and it lists every number on the study's page that your change would move, so we can both see what it does. I read every change and approve it before it merges. When it merges, it goes in the study's `CHANGES.md` with your name, and I update the page.

The changes I'd most like:

- A better source for a cap's cost. Freeway Park's comes only from Wikipedia.
- Caps that aren't in `caps.csv` yet, with a cost and a source.
- A quote for any line in [`cap-i-95/budget/phase-one.csv`](cap-i-95/budget/phase-one.csv). Every line says "needs a quote".
- Fixes to the maps.

## No GitHub account?

Email me at ADDRESS-TO-CONFIRM with the number, what it should be and where it comes from. I'll open the pull request and credit you.

## Check it yourself

You need Python 3 and nothing else.

```sh
python3 tools/check.py
```

Each model also runs on its own and prints its numbers, for example `python3 cap-i-95/models/cost.py`.

## Licenses

- **Text and data:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Use them for anything, and credit "Andy Chatham, Proposals for the Commons".
- **Maps made from OpenStreetMap** ([`shared/maps/cap-footprints.geojson`](shared/maps/cap-footprints.geojson)): [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/), © OpenStreetMap contributors. Changes to them stay open.
- **Code** (`tools/`, each study's `models/` and the scripts in `assets/`): [MIT](LICENSE).
- **Photos and renders:** each study's `assets/README.md` says where every image comes from.

[`LICENSE.md`](LICENSE.md) has the details.
