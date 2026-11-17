# Proposals for the Commons: the data

Proposals for the Commons are long studies of how a public place could be used better, written by me, Andy Chatham. Each one says what the idea would cost, who would pay and who decides. This repo holds everything behind them: photos and scans of how places are now, the data, maps and models, and the budgets and drawings of what's proposed. Anyone can check it, and anyone can add to it, from one photo of a park to a plan for a rail line.

Every place here follows the [Reality Context Protocol](protocol/README.md): one way to write down what's there, what's proposed, who agreed and what got built, with a source for every fact. A pull request is a proposed change to a place.

## What's here

| Folder | What it holds |
| --- | --- |
| [`protocol/`](protocol) | The Reality Context Protocol: what each file means, the formats we accept, and schemas for software. |
| [`shared/`](shared) | [`caps.csv`](shared/caps.csv): 17 highway caps with a reported cost or a recent estimate. [`sources.csv`](shared/sources.csv): every source, its link and the date it was read. [`maps/`](shared/maps): outlines of caps that exist, from OpenStreetMap. |
| [`cap-i-95/`](cap-i-95) | Cap the highway: a deck over I-95 between Federal Hill and Downcity in Providence. Aerials, traffic, tax and bridge data, the trench outline, the cost and tax models, and the proposal's budget, drawings and renders. |
| [`tools/`](tools) | The number check. |

More studies move in as they're published.

## Add to it

[`CONTRIBUTING.md`](CONTRIBUTING.md) shows how, for every size of contribution: a photo, a scan, a fact, a map fix, a model, a quote or a new proposal. On GitHub, open the file and click the pencil, or **Add file**. No GitHub account? Email andy@articulate.network and I'll open the pull request.

The number check runs on every pull request. It fails when a fact has no source, a capture has no license, or a file is broken, and it lists every number on the study's page that your change would move. I read every change and approve it before it merges, and it goes in the place's `CHANGES.md` with your name.

The changes I'd most like:

- A better source for a cap's cost. Freeway Park's comes only from Wikipedia.
- Caps that aren't in `caps.csv` yet, with a cost and a source.
- A quote for any line in [`cap-i-95/proposal/budget/phase-one.csv`](cap-i-95/proposal/budget/phase-one.csv). Every line says "needs a quote".
- Photos and scans of the I-95 trench and its bridges as they are today.

## Check it yourself

You need Python 3 and nothing else.

```sh
python3 tools/check.py
```

Each model also runs on its own and prints its numbers, for example `python3 cap-i-95/models/cost.py`.

## Licenses

- **Text and data:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Use them for anything, and credit "Andy Chatham, Proposals for the Commons".
- **Maps made from OpenStreetMap** ([`shared/maps/cap-footprints.geojson`](shared/maps/cap-footprints.geojson)): [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/), © OpenStreetMap contributors. Changes to them stay open.
- **Code** (`tools/`, each place's `models/` and the scripts in `proposal/`): [MIT](LICENSE).
- **Photos, scans and renders:** each place's `captures/captures.csv` gives every capture's license, and `proposal/IMAGES.md` says how each render was made.

[`LICENSE.md`](LICENSE.md) has the details.
