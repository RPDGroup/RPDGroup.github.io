# Website visuals

## Homepage photo wall

The original group photograph is from the organization's
[profile repository](https://raw.githubusercontent.com/RPDGroup/.github/main/profile/codex-clipboard-0e00ee94-61ae-4924-8c5d-4394a72ec271.jpg),
selected again by the user for the homepage. The original stores a 3672 × 4896
image with EXIF orientation 5. Apply that orientation before web encoding: the
upright image is 4896 × 3672. `team-upright-800.webp` and
`team-upright-1600.webp` preserve the complete photograph at its correct aspect
ratio. The homepage, People, and About sections share these corrected assets.
`team-photo-source.json` records the input hash, orientation, and output sizes.

Five earlier wall photographs were extracted directly from the user-supplied
`photos-2026(2).pptx`. Only selected photographs are served; the presentation,
slide text, certificates, and original media files are not website assets.
The original presentation remains unchanged. `photos/sources.json` records the
selected embedded media, slide numbers, input hashes, and web encodings.

The current homepage rotates all 105 activity images in 35 sets of three.
The activity generator derives the wall directly from `data/activities.json`,
so future additions and removals automatically update the rotation. Optional
`homepage_focal_points` set supporting-tile focal points. Desktop places one complete large
photograph beside two supporting frames. Phones place the complete large
photograph above two smaller frames. CSS may crop supporting tiles, while
image files remain complete. Clicking a photograph opens its full web version.
All assets are reused from the existing photo journal; the rotation creates
no duplicate image files.

The older `team-800.webp` and `team-1600.webp` encodings remain for compatibility
with earlier revisions; current pages use only `team-upright-*`.

## Member portraits

`members/xinyuan-zhao.webp` is the portrait supplied by the user for Xinyuan
Zhao, a master's student in the 2025 intake. It is a 640 × 640 square
head-and-shoulders excerpt for the circular directory portrait and profile
dialog, encoded as WebP at quality 86. No retouching is applied. Embedded
metadata is removed, and the supplied photograph remains unchanged.
`members/sources.json` records the input filename and hash, original dimensions,
crop rectangle, and output encoding and hash.

## Activity photo journal

The Activities page contains 105 images: 44 from `photos-2026(2).pptx`,
13 graduation photographs selected by the user from Photos, and 48 directly
supplied images of academic exchanges, group activities, and related keepsakes.
It reuses five earlier homepage photo encodings where possible and adds 39 pairs
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
are preserved. These photographs are included under Group moments, and one
is included in the homepage selection.

`activities/upload-sources.json` records directly supplied image attachments.
`upload-001` is an academic forum photograph, encoded as an uncropped
720 × 540 WebP thumbnail at quality 74 and a 1600 × 1200 full view at quality
80. Embedded metadata is removed, and the supplied source image is preserved.
It appears under Academic exchange.

The 20 other photographs from the earlier direct-upload batch show
sports, gatherings, graduation, a conference, and group outings. A repeated
conference selfie in the message is included once. The same quality settings
apply, with thumbnails bounded by 720 × 960 and full views by 1600 × 1600.
EXIF rotations and mirrored orientations are applied before encoding, while
the complete frame, any visible watermarks, and all source files are preserved.
Conference photographs are under Academic exchange; the other photographs
are under Group moments. Input filenames, hashes, dimensions, and output
metadata for the current selection are recorded in the same manifest. Original local paths and embedded
camera metadata are not published.

`upload-024` is the lab group selfie supplied again for the homepage. It uses
the existing `team-upright-800.webp` and `team-upright-1600.webp` encodings,
preserving the complete frame and adding no duplicate image files. It appears
first in the homepage rotation and in the activity journal. Its supplied PNG
hash and the reused asset hashes are recorded in `upload-sources.json`.

The next 27 supplied files add 26 images, `upload-025` through `upload-050`.
`IMG_20230825_141358.jpg` matches `photo-009` and remains represented once;
the upload manifest records the additional input under `duplicate_sources`.
The new files use the same thumbnail and full-view bounds and quality settings
as the earlier uploads, with no upscaling or cropping. The appointment letter
is rotated 90 degrees counterclockwise for reading; the transform is recorded
with its source hash. The group sketch and cat photograph are included.
These encodings total 4,724,872 bytes, with the original 27 inputs preserved.

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

## Group logo

The user selected [dyno-hero.webp](https://github.com/SIITW/SIITW/blob/main/assets/dyno-hero.webp)
as the replacement logo. `brand-logo.webp` is a 256-pixel navigation asset;
`brand-icon-32.png` and `brand-touch-icon.png` provide browser and touch icons.
All three resize the complete image onto a transparent square and preserve its
colors and transparency. No part is cropped or redrawn. The source Git blob,
input hash, dimensions, and output hashes are recorded in `brand-logo-source.json`.
The earlier user-supplied `brand-logo.png` remains available for provenance and
compatibility; current pages use the new logo and icons.

## Other graphics

The three SVG research-topic icons embedded in `index.html` are schematic
icons. The earlier `favicon.svg` monogram is retained from the previous revision
and is no longer used. Neither represents measured data or a scientific
performance result.
