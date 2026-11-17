# Reality Context Protocol, draft 0.1

The Reality Context Protocol is a plain way to write down a place: what's there now, what someone wants to change, who agreed to it and what got built, with a source for every fact. People and software read and write the same files. A pull request is a proposed change to a place, and a reviewed merge is its approval.

It's the format behind Proposals for the Commons, and the public tier of the Record that Articulate's products work on: the shared, versioned record of places, people and work behind ZenHome and ZenLink. The same files describe a private home, a rental unit or a job. There, only the place's members can read them.

## Five things

| Thing | What it is | In a place folder | Articulate's word | Lines up with |
| --- | --- | --- | --- | --- |
| **Place** | Where: a park, a highway trench, a rail corridor, a building, a home, a room | `place.json` and a GeoJSON outline | Jurisdiction, Parcel, Building, Property, Unit, Area | GeoJSON, OpenStreetMap and Overture, IFC Site and Space |
| **Capture** | What exists, recorded: a photo, a scan, a video, an aerial | the file, or a link to it, and a row in `captures/captures.csv` | Capture | STAC Item, EXIF, E57, glTF |
| **Fact** | Something known about a place, with its source | a row in `data/*.csv` with `source_ids` that point into `shared/sources.csv` | Fact | W3C PROV |
| **Proposal** | A change someone wants, from a new bench to a rail tunnel | `proposal/proposal.json` with its budget, drawings, models and renders | Project, Design model, Option | IFC Project, OpenUSD variants |
| **Approval** | Someone agreeing to an exact version | a reviewed merge, and each official decision in the proposal's `history` | Revision, Approval | git commits, ISO 19650, PROV |

## The life of a change

A proposal's `state` is one of these, in order. Each change of state goes in its `history` with the date, who decided it and, for an official decision, its source.

| State | Means | The Record's word |
| --- | --- | --- |
| `proposed` | Written down, with what it would cost and who decides | Proposed |
| `agreed` | The people who decide approved an exact version, like a council vote or a signed grant | Agreed |
| `underway` | Being built | Do |
| `built` | Finished | Finish |
| `verified` | Checked against what was proposed, with captures of the result | Verified |
| `dropped` | Nobody is pursuing it. It stays in the record, so the next person can see why | |

What exists now never changes state. A capture is what someone saw on a date; a newer capture sits beside it.

## A pull request for reality

1. **Propose.** Anyone opens a pull request that adds a capture, fixes a fact, or changes a proposal.
2. **Check.** The number check runs. It fails when a fact has no source, a capture has no license, or a file is broken, and it lists every number on the study's page that would move.
3. **Review.** The place's maintainers, named in `.github/CODEOWNERS`, read it.
4. **Merge.** The merge is the place's next revision. Git keeps every earlier one, and the study's `CHANGES.md` says what changed and who did it.

## A place folder

```
cap-i-95/
  place.json              the place: name, level, tier, outline, who owns it
  captures/               what exists: photos, scans, aerials
    captures.csv          one row per file: where, when, who, license
  data/                   facts, each row with source_ids
  maps/                   outlines as GeoJSON
  models/                 the math, as code anyone can rerun
  proposal/
    proposal.json         the change: summary, state, phases, who decides, history
    budget/               the budget, line by line
    drawings/  renders/   what it would look like, with the prompts for any AI image
  numbers.csv             every number the study's page shows, and where it comes from
  CHANGES.md
```

A place with no proposal yet is just `place.json` and `captures/`. That's enough to start.

## Captures

Each row of `captures.csv` names one file:

| Column | Required | What goes in it |
| --- | --- | --- |
| `file` or `url` | one of them | The file's name in this folder, or a stable link to it |
| `sha256` | yes | The file's SHA-256, so anyone can confirm they have the same file |
| `bytes` | yes | Its size |
| `kind` | yes | One of the kinds in [`formats.csv`](formats.csv): `photo`, `scan`, `mesh`, `splat`, `video`, `map` and so on |
| `format` | yes | Its format, like `jpeg`, `e57` or `glb` |
| `taken` | yes | When it was captured: `2026-11-16`, `2026-11`, `2026`, or a range like `1951/1952` |
| `lat`, `lng` or `bbox` | yes | Where: a point, or west,south,east,north for an aerial |
| `by` | yes | Who made it |
| `license` | yes | `CC-BY-4.0`, `CC0-1.0`, `CC-BY-SA-4.0`, `ODbL-1.0`, `public-domain`, or `credit:<who>` for an agency that asks only for credit |
| `source_ids` | no | Where it came from, when someone else published it |
| `note` | no | Anything else: what it shows, which way it faces |

Any format is welcome. [`formats.csv`](formats.csv) lists what we can show and the open format we'd suggest for each kind, but a file in any other format is kept as it is.

Files bigger than 25 MB, like most scans and videos, stay out of git. Put them anywhere with a stable public link, and give the link, its SHA-256 and its size in the row. An upload page for logged-in ZenHome and ZenLink users, which stores and serves them, is next.

## Tiers

| Tier | Who can read it | Examples |
| --- | --- | --- |
| `commons` | Anyone | Parks, streets, highways, bridges, public buildings, codes, permits, public prices |
| `private` | The place's members | A home, a unit, a job, a company's records |

This repo is only the `commons` tier. A private place uses the same files inside ZenHome or ZenLink, where its members can read it and nobody else can.

## From a bench to a national project

The files are the same at every size. A bigger proposal has more places, more facts and more phases.

| Size | Example | What it takes |
| --- | --- | --- |
| A small fix | A new bench in a park, a broken fountain | One capture of how it is, one proposal, maybe a quote |
| A site | A splash pad, a playground | Captures, a scan, a budget |
| A corridor | Cap I-95 in Providence | An outline in blocks, facts from public records, a cost model, a budget |
| A network | A rail link between two stations, a greenway | A place with `parts`, one per segment, each with its own captures |
| A national program | High-speed rail between cities | Places in several states, each with its own `jurisdictions` and decision-makers |

## Not settled yet

- **Shared ids.** How a place points at the same thing in OpenStreetMap, Overture, a state parcel layer or a city's bridge list.
- **A scan's frame.** A scan measures in its own frame, in meters from where it started. Tying that frame to map coordinates is open.
- **An API.** Today the protocol is files in git. Next come an HTTP API and a tool for AI assistants that read and propose changes the same way, with a person approving each one.

Changes to the protocol itself go through pull requests too.
