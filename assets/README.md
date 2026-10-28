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

The desktop wall balances six photographs across two rows. The narrow-screen
wall places the complete main photograph above a compact supporting collage.
Clicking a photograph opens its complete web version. CSS may crop supporting
tiles to fit their frames; image files themselves are not cropped.

The older `team-800.webp` and `team-1600.webp` encodings remain for compatibility
with earlier revisions; current pages use only `team-upright-*`.

## Activity photo journal

The Activities page contains 84 photographs: 48 from `photos-2026(2).pptx`,
13 graduation photographs selected by the user from Photos, and 23 directly
supplied photographs of academic exchanges and group activities.
It reuses the five homepage photo encodings where possible and adds 43 pairs
of web-sized images in `activities/`. A small 166 × 163 thumbnail and the
presentation's award/administrative document images are outside this photo
journal. The original presentation and extracted source media remain unchanged.

`activities/sources.json` records every photograph's embedded-media path, slide,
source hash, PowerPoint picture transform, web dimensions, and output hashes.
Image orientation follows EXIF plus the presentation's right-angle rotations
and flips. In particular, image 25 uses the presentation's vertical flip and
image 39 uses its 90-degree clockwise rotation. Full web images are not cropped,
redrawn, or generated. Gallery thumbnails preserve image proportions; homepage
preview frames may crop their display. Captions describe the visible scene
without inferring missing event dates, locations, or individual identities.

`activities/album-sources.json` records the 13 supplied Photos filenames,
input hashes and dimensions, and the web-image sizes, quality settings, and
hashes. `album-001` through `album-013` each have a WebP thumbnail (up to
720 × 960, quality 74) and a full view (up to 1600 × 1600, quality 80).
Neither version upscales the supplied image. EXIF orientation is applied and
embedded metadata is removed. Complete frames and the source files in Photos
are preserved. These photographs appear first under Group moments, and one
is included in the homepage selection.

`activities/upload-sources.json` records directly supplied image attachments.
`upload-001` is an academic forum photograph, encoded as an uncropped
720 × 540 WebP thumbnail at quality 74 and a 1600 × 1200 full view at quality
80. Embedded metadata is removed, and the supplied source image is preserved.
It appears under Academic exchange.

`upload-002` through `upload-023` add 22 directly supplied photographs of
sports, gatherings, graduation, a conference, and group outings. A repeated
conference selfie in the message is included once. The same quality settings
apply, with thumbnails bounded by 720 × 960 and full views by 1600 × 1600.
EXIF rotations and mirrored orientations are applied before encoding, while
the complete frame, any visible watermarks, and all source files are preserved.
Conference photographs are under Academic exchange; the other photographs
are under Group moments. Input filenames, hashes, dimensions, and output
metadata are recorded in the same manifest. Original local paths and embedded
camera metadata are not published.

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
