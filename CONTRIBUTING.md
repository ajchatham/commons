# How to add to the commons

Anything that makes a public place better understood is welcome, from one photo to a whole study. Pick the size that fits what you have.

| You have | Example | Add | Where |
| --- | --- | --- | --- |
| **A photo** | A new bench in Lippitt Park, a cracked sidewalk on a bridge | The photo, with where and when you took it | The place's `captures/` folder and one row in `captures/captures.csv` |
| **A scan or video** | A phone scan of a playground, a walk across the Atwells Ave bridge | The file, or a link to it if it's over 25 MB | The same: `captures/` and `captures.csv` |
| **A fact** | A cap's real cost, a bridge's condition rating, a traffic count | The number, and where it comes from | A row in the place's `data/` file, and the source in [`shared/sources.csv`](shared/sources.csv) |
| **A fix to a map** | An outline that's off by a lane | The corrected GeoJSON | The place's `maps/` |
| **A model or a quote** | A better way to estimate deck cost, or an engineer's price for a budget line | The code, or the amount and who quoted it | The place's `models/` or `proposal/budget/` |
| **A proposal** | Shade trees on a plaza, a cap over a highway, a rail link | A new folder with `place.json`, `captures/` and `proposal/proposal.json` | A new folder at the top of the repo |

The [Reality Context Protocol](protocol/README.md) explains each file, and [`protocol/formats.csv`](protocol/formats.csv) lists the formats we can show. Any format is accepted.

## On GitHub

1. Open the folder or file on GitHub. To change a file, click the pencil. To add one, click **Add file**, then **Upload files**. GitHub makes your own copy, so you don't need to ask first.
2. Fill in the row that goes with it: where, when, who, the license, and a source for any number.
3. Click **Propose changes** and say what it is in a sentence or two.

The number check runs on every pull request. It fails when a fact has no source, a capture has no license, or a file is broken, and it lists every number on the study's page that your change would move. Andy reads every change and approves it before it merges. When it merges, it goes in the place's `CHANGES.md` with your name.

## No GitHub account?

Email andy@articulate.network with the file or the number, where and when it's from, and how you'd like to be credited. Andy will open the pull request.

## What you agree to

- You made the file or found the number yourself, or you're allowed to share it.
- What you add is licensed CC BY 4.0, unless its row names another open license.
- Maps traced from OpenStreetMap stay under the ODbL, in their own file.

## Please leave out

- Faces you can recognize and license plates. Blur them or crop them out.
- The inside of anyone's home, or anything else private. This repo is only for public places.
- Anything you couldn't show the people in it.
