# Cap I-95: drawings and renders

How each drawing and render on the study page was made. The aerial photos are captures of what exists, so they're in [`../captures/`](../captures), with their sources in `captures.csv`.

## Drawings

| File | What it is |
| --- | --- |
| [`drawings/section-long.svg`](drawings/section-long.svg) | Along I-95 from Atwells Ave to Westminster St, seen from Federal Hill. Heights are drawn about five times their true scale against length. |
| [`drawings/section-cross.svg`](drawings/section-cross.svg) | Across the trench at the park, to scale. Lanes from FHWA's 2024 highway data. |
| [`drawings/footprints.svg`](drawings/footprints.svg) | The trench beside caps that exist, at one scale. The other outlines come from OpenStreetMap. |

`python3 drawings/section.py` redraws both sections from [`../maps/phase-one.geojson`](../maps/phase-one.geojson).

## Concept renders

These are illustrations, not designs. Google's Gemini image model made them with the prompts in [`prompts/`](prompts), using [`render.mjs`](render.mjs). To run it, set `GOOGLE_API_KEY` in your environment and pass a name, an aspect ratio, a size and a prompt file.

| File | Prompt | Notes |
| --- | --- | --- |
| [`renders/aerial-concept.jpg`](renders/aerial-concept.jpg) | `p-tight.txt` | Rendered from a tight crop of the 2023 aerial with the deck painted in, then pasted back inside the phase-one outline so nothing outside it changes. The real Atwells Ave bridge was pasted back over the deck's north edge. |
| [`renders/render-portal.jpg`](renders/render-portal.jpg) | `p-portal.txt` | Looking north toward Westminster St, where I-95 goes under the park. |
| [`renders/render-park.jpg`](renders/render-park.jpg) | `p-park.txt` | The park at street level, looking south to Washington St. |
| [`renders/render-broadway.jpg`](renders/render-broadway.jpg) | `p-broadway.txt`, then `p-broadway-signs.txt` | Broadway crossing the deck. The second prompt blanked the made-up lettering on the signs. |
| [`renders/share-card.jpg`](renders/share-card.jpg) | | The link preview: the 2023 aerial with the outline and three numbers. |

The aerial concept starts from [`../captures/aerial-2023.jpg`](../captures/aerial-2023.jpg).

[`prompts/dropped/`](prompts/dropped) holds two prompts whose renders were wrong and aren't used. The Atwells Ave view put the open highway beside the street instead of under it. The bird's-eye view was tried three times and kept moving the homes beside the park and leaving an open gap behind Atwells Ave.
