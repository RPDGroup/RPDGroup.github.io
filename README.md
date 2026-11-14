# Ren Protein Design Group website

Static site for the Ren Protein Design Group, live at <https://rpdgroup.github.io/>.
No build step: `main` is served from the repository root, and the site runs on
plain HTML, CSS, and JavaScript with no third-party runtime.

## Preview

```sh
python3 -m http.server 8766 --bind 127.0.0.1
```

Open <http://127.0.0.1:8766/>. Sections work as plain anchors, so every page
stays readable without JavaScript.

## Layout

| Path | Purpose |
| --- | --- |
| `index.html` | All page content: home, research, members, publications, activities, news, resources, analects, about, contact |
| `assets/site.css` | Global styles, responsive layout, reduced-motion support |
| `assets/site.js` | Hash navigation, mobile menu, resource search and filters |
| `assets/home-photos.js` | Homepage photo wall: rotation, pause, manual navigation |
| `assets/members.js` | Member directory filters and profile dialogs |
| `assets/activities.js` | Activity gallery filters |
| `data/members.json` | Member profiles, in display order |
| `data/activities.json` | Activity photographs and homepage selections |
| `data/publications.json` | Curated publication metadata |
| `scripts/update-members.py` | Regenerates member markup from the data |
| `scripts/update-activities.py` | Regenerates the gallery and homepage wall |
| `scripts/update-publications.py` | Regenerates the publication lists |
| `assets/README.md` | Image sources and figure provenance |

## Editing content

- **Copy and page structure** live in `index.html`.
- **Members**: edit `data/members.json`, put portraits in `assets/members/`,
  then run `python3 scripts/update-members.py`. Each entry needs a unique
  lowercase `id` and a `name`; everything else is optional. Only publish
  information approved for public display.
- **Activities**: edit `data/activities.json`, then run
  `python3 scripts/update-activities.py`. Do not infer event names, dates,
  places, or identities from a file name; keep source metadata in
  `assets/activities/*-sources.json`.
- **Publications**: edit `data/publications.json`, then run
  `python3 scripts/update-publications.py`. Keep citation text verbatim from
  the source, including original spellings, and record roles only for group
  members.

The generators also refresh the `?v=` version strings on the frontend assets,
so run them after editing CSS or JavaScript as well.

## Checks

```sh
node --check assets/site.js
node --check assets/members.js
node --check assets/activities.js
node --check assets/home-photos.js
python3 scripts/update-members.py --check
python3 scripts/update-activities.py --check
python3 scripts/update-publications.py --check
git diff --check
```

Then open every route in a desktop and a narrow window, and check search,
filters, photo previews, and profile dialogs (they should close with Escape and
restore keyboard focus).

## Publishing

Automatic deployment is intentionally disabled: the Pages source is set to
GitHub Actions without a push-triggered workflow, so a push alone does not
update the live site. To release, switch the repository Pages source to
*Deploy from a branch* (`main`, `/`), wait for the deployment to succeed, and
then restore the source to *GitHub Actions*.
