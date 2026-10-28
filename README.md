# Ren Protein Design Group website

A buildless GitHub Pages website. The `main` branch is published from the
repository root at <https://rpdgroup.github.io/>. No npm install, framework, or
third-party runtime is required.

The layout takes cues from Baker Lab's photo-led homepage: a blue-purple
masthead, compact navigation, a balanced photo collage, and simple research
entries. Branding, photographs, project descriptions, and scientific figures
belong to RPDGroup. Home, News, About, and Contact are grouped under Info; the
logo also links home. Research, People, Publications, and Resources remain
direct navigation links.

## Preview

From the repository root:

```sh
python3 -m http.server 8766 --bind 127.0.0.1
```

Open <http://127.0.0.1:8766/>. Check the homepage, the eight navigation destinations,
the `#research/dynamics` deep link, resource search and category filters, the
Info dropdown, and the mobile menu. JavaScript enhances routing and search; without it, all sections
remain readable and navigation uses native anchors.

## Edit

- `index.html`: research, people, publication, news, contact, and resource content.
- `assets/site.css`: responsive styles and reduced-motion support.
- `assets/site.js`: hash navigation, accessible mobile disclosure, resource search.
- `assets/photos/`: selected photographs from the supplied presentation, with source metadata.
- `assets/README.md`: image sources and scientific illustration provenance.

Keep project descriptions and publication metadata grounded in their owning
repositories. Home project cards and resource cards are static HTML; update both
when adding or changing a project. Search indexes the resource cards themselves.

## Checks

```sh
node --check assets/site.js
git diff --check
```

Before publishing, inspect desktop and narrow-screen rendering, open each route,
and check search, category combinations, an empty result, and clearing filters.
Check the photo wall, the full team photo's orientation, and photo/architecture
previews. The previews should close with either their close button or Escape,
restore keyboard focus, and retain working image links without JavaScript.
