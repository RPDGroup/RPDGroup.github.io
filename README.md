# Ren Protein Design Group website

A buildless GitHub Pages website. The `main` branch is published from the
repository root at <https://rpdgroup.github.io/>. No npm install, framework, or
third-party runtime is required.

The layout takes cues from Baker Lab's photo-led homepage: a blue-purple
masthead, compact navigation, a rotating photo collage, and simple research
entries. Branding, photographs, project descriptions, and scientific figures
belong to RPDGroup. Home, News, About, and Contact are grouped under Info; the
logo also links home. Research, People, Publications, and Resources remain
direct navigation links. Activities has its own navigation entry and a
three-photo preview on the homepage.

## Preview

From the repository root:

```sh
python3 -m http.server 8766 --bind 127.0.0.1
```

Open <http://127.0.0.1:8766/>. Check the homepage, the nine navigation destinations,
the `#research/dynamics` deep link, resource search and category filters, the
Info dropdown, and the mobile menu. JavaScript enhances routing and search; without it, all sections
remain readable and navigation uses native anchors.

## Edit

- `index.html`: research, people, publication, news, contact, and resource content.
- `assets/site.css`: responsive styles and reduced-motion support.
- `assets/site.js`: hash navigation, accessible mobile disclosure, resource search.
- `assets/home-photos.js`: homepage photo rotation, pause, and manual navigation.
- `data/members.json`: public member profiles, in display order.
- `scripts/update-members.py`: generate static member HTML after editing the data.
- `assets/members.js`: member search, category filters, and profile dialogs.
- `data/activities.json`: activity photographs, categories, homepage previews, and photo focal points.
- `scripts/update-activities.py`: render the photo journal and refresh frontend asset versions.
- `assets/activities.js`: activity category filtering.
- `assets/activities/`: web encodings and source metadata for the activity journal.
- `assets/photos/`: selected photographs from the supplied presentation, with source metadata.
- `assets/README.md`: image sources and scientific illustration provenance.

Keep project descriptions and publication metadata grounded in their owning
repositories. Home project cards and resource cards are static HTML; update both
when adding or changing a project. Search indexes the resource cards themselves.

## Member profiles

The People page follows the circular portrait directory and profile overlays of
<https://wglab.org/members.html>. The roster starts empty because individual
photographs and biographies will be supplied later. The public empty state
does not imply that the group has no members.

Add confirmed profiles to the `members` list in `data/members.json`, and place
their web photographs inside `assets/members/`. Each entry requires a unique
lowercase `id` and a `name`. Optional fields are `name_local`, `role`, `status`
(`current`, `previous`, or `future`; defaults to `current`), `photo` (a local
asset path), `period`, `bio`, `contact` (list of text entries), `education`
(list of text entries), `research`, and `links` (list of `label` / HTTP(S) `url`
objects). Only include information approved for public display. Missing photos
use initials; missing fields are omitted. Entry order is preserved.

Run `python3 scripts/update-members.py` after updating the data and commit the
generated `index.html` with it. Profiles are static HTML and remain available
as native expandable entries without JavaScript. JavaScript adds category and
keyword filtering and a larger profile dialog. The generator escapes text and
validates image paths and external links before changing the page.

## Activity photographs

The Activities page uses 81 photographs: 47 from the supplied presentation,
13 graduation photographs selected by the user from Photos, and 21 directly
supplied photographs of academic exchanges and group activities. They are
organized as Lab life, Academic exchange, and Group moments. Below the rotating
wall, the homepage shows three selections. The gallery preserves complete image proportions;
homepage previews may crop a frame. Opening a photograph shows the complete
web image. Previous/Next buttons and the left/right arrow keys browse only
the current category; closing the viewer restores focus to its opening link.

Add photographs and their web-image paths to `data/activities.json`. Run
`python3 scripts/update-activities.py` to regenerate the gallery and homepage
selection. This also gives frontend CSS/JS content-based version URLs, so new
HTML loads its matching assets. Run it after frontend asset edits as well.
Do not invent event names, dates, places, or identities from a photo's file
name or the presentation's title. Source metadata is in
`assets/activities/sources.json`, `assets/activities/album-sources.json`, and
`assets/activities/upload-sources.json`;
original inputs remain outside the website.

The homepage wall automatically includes every photograph in the activity
data, in the same order, grouped into sets of up to three with no omissions
or duplicates. Adding or removing a gallery entry updates the wall when the
generator runs. Optional `homepage_focal_points` percentages control the crop
in supporting tiles. The large photograph keeps its complete frame. The wall
rotates every eight seconds and supports previous/next buttons, a set chooser, left/right
keys, and a pause/play control. Manual navigation or keyboard focus pauses
rotation until Play is selected. Hovering over photos, leaving the homepage,
scrolling past the wall, or hiding the tab suspends automatic changes.
Reduced-motion preferences start the wall paused. Image previews pause the
wall and browse the three visible photographs. Without JavaScript, the first
set remains visible with native full-image links. Run the activity generator
after changing selections; it renders all photo blocks and refreshes cache
versions for the frontend files.

## Checks

```sh
node --check assets/site.js
node --check assets/members.js
python3 scripts/update-members.py --check
python3 scripts/update-activities.py --check
node --check assets/activities.js
node --check assets/home-photos.js
git diff --check
```

Before publishing, inspect desktop and narrow-screen rendering, open each route,
and check search, category combinations, an empty result, and clearing filters.
Check the photo wall, the full team photo's orientation, and photo/architecture
previews. The previews should close with either their close button or Escape,
restore keyboard focus, and retain working image links without JavaScript.
For member-directory changes, check category plus keyword filtering, empty
results and reset, optional fields and missing photos, native disclosures,
and profile-dialog closing/focus behavior on desktop and a narrow screen.
For Activities changes, check every category, full-image preview, Previous/Next
and arrow-key navigation, wrapping at the gallery ends, and focus after closing.
Check that research figures still open without photograph-navigation controls.
