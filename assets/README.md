# Website visuals

## Homepage photo wall

The main photograph is the existing group photograph from the organization's
[profile repository](https://raw.githubusercontent.com/RPDGroup/.github/main/profile/codex-clipboard-0e00ee94-61ae-4924-8c5d-4394a72ec271.jpg),
selected again by the user for the homepage. The original stores a 3672 × 4896
image with EXIF orientation 5. Apply that orientation before web encoding: the
upright image is 4896 × 3672. `team-upright-800.webp` and
`team-upright-1600.webp` preserve the complete photograph at its correct aspect
ratio. The homepage, People, and About sections share these corrected assets.
`team-photo-source.json` records the input hash, orientation, and output sizes.

The five other photographs were extracted directly from the user-supplied
`photos-2026(2).pptx`. Only selected photographs are served; the presentation,
slide text, certificates, and original media files are not website assets.
The original presentation remains unchanged. `photos/sources.json` records the
selected embedded media, slide numbers, input hashes, and web encodings.

The desktop wall uses a complete main photograph with five supporting tiles.
The narrow-screen wall preserves complete image proportions in a masonry layout,
with the main photograph spanning both columns. Clicking a photograph opens its
complete web version. CSS may crop supporting tiles on wider screens; image
files themselves are not cropped.

The older `team-800.webp` and `team-1600.webp` encodings remain for compatibility
with earlier revisions; current pages use only `team-upright-*`.

## Original model architecture figures

- `dynom-model.webp`: the complete existing
  [DynoM architecture figure](https://github.com/RPDGroup/DynoM/blob/main/model.jpg).
- `abus-architecture.webp`: architecture panel b from the existing
  [ABUS figure](https://github.com/RPDGroup/ABUS/blob/main/figures/Figure1.png).
- `codonbert-architecture.webp`: architecture panel b from the existing
  [CodonBERT figure](https://github.com/RPDGroup/CodonBERT/blob/main/figures/2024.01.24-figure1.jpg).

These are source-image excerpts and web encodings, not redrawn or generated
architectures. Labels, connections, and relative geometry are preserved.
`architecture-sources.json` records original dimensions, Git blob hashes, and
the pixel rectangles used for panel extraction. Homepage cards and research
sections link to larger previews and the complete original source figures.
Each owning repository provides its license and citation guidance.

## Earlier protein illustration

`protein-ensemble.svg`, `ensemble-source.json`, and
`scripts/render-ensemble.py` are retained from the previous design. They are no
longer displayed on current pages. The illustration used two public DynoM
example outputs (`9R71_sample0.pdb` and `9R71_sample1.pdb`), common C-alpha atoms,
Kabsch alignment, a shared projection, and display interpolation. It was a
static illustration, not an MD trajectory or a quantitative comparison.

## Official group logo

`brand-logo.png` is the official logo supplied by the user. It is an unchanged
copy of the original PNG, used in the navigation and browser icons. Its colors,
wording, proportions, and background are preserved. `brand-logo-source.json`
records its dimensions and SHA256 hash.

## Other graphics

The three SVG research-topic icons embedded in `index.html` are schematic
icons. The earlier `favicon.svg` monogram is retained from the previous revision
and is no longer used. Neither represents measured data or a scientific
performance result.
