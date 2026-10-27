# Website visuals

## Protein illustration

`protein-ensemble.svg` renders two real example outputs from the public
[DynoM repository](https://github.com/RPDGroup/DynoM/tree/main/example/Test_Task/ADK/02_Inference/Output/test_gen/9R71):
`9R71_sample0.pdb` and `9R71_sample1.pdb`.

Only common C-alpha atoms are used. Sample 1 is aligned to sample 0 by Kabsch
alignment; both share a PCA view, camera rotation, and scale. The two colors
distinguish the model outputs. The illustration is a static display, not an MD
trajectory or a quantitative comparison. Display interpolation does not change
the source coordinates. Exact source URLs, input hashes, and atom count are in
`ensemble-source.json`.

To regenerate, install NumPy in a suitable Python environment and run
`python3 scripts/render-ensemble.py`. This reads two small public PDB files and
does not run inference. Inspect source changes before replacing an existing
illustration or its recorded provenance.

## Project diagram

`dynom-model.webp` is a web encoding of the existing
[DynoM architecture figure](https://github.com/RPDGroup/DynoM/blob/main/model.jpg).
The complete figure is preserved. The owning repository includes its license.

## Group photo

`team-800.webp` and `team-1600.webp` are resized web encodings of the photograph
already used by the original website:
<https://raw.githubusercontent.com/RPDGroup/.github/main/profile/codex-clipboard-0e00ee94-61ae-4924-8c5d-4394a72ec271.jpg>.

The original dimensions are 3672 × 4896, in portrait orientation. The full image
is preserved without cropping. The page uses responsive sources and intrinsic
dimensions. The original photograph remains in the organization's profile repo.

## Other illustrations

The SVG symbols embedded in `index.html` are original schematic illustrations for
research topics and project categories. They are not experimental measurements,
generated structures, or performance plots. `favicon.svg` is an original RPD
monogram used as the site icon.
