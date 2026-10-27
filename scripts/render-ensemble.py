"""Render the website's static C-alpha illustration from two public DynoM outputs.

Requires Python 3 and NumPy. Downloads only two small PDB files; does not run
inference or generate a trajectory. Run from any directory with:
    python3 scripts/render-ensemble.py
"""
from pathlib import Path
from urllib.request import urlopen
from hashlib import sha256
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://raw.githubusercontent.com/RPDGroup/DynoM/main/example/Test_Task/ADK/02_Inference/Output/test_gen/9R71/'


def read_ca(data):
    atoms = {}
    for line in data.decode().splitlines():
        if line.startswith('ENDMDL'):
            break
        if line.startswith('ATOM') and line[12:16].strip() == 'CA' and line[16] in ' A':
            key = (line[21], line[22:27])
            atoms.setdefault(key, [float(line[30:38]), float(line[38:46]), float(line[46:54])])
    return atoms


def render():
    records, models = [], []
    for sample in (0, 1):
        url = SOURCE + f'9R71_sample{sample}.pdb'
        data = urlopen(url, timeout=30).read()
        models.append(read_ca(data))
        records.append(dict(url=url, sha256=sha256(data).hexdigest(), bytes=len(data)))
    keys = [key for key in models[0] if key in models[1]]
    if len(keys) < 20:
        raise ValueError('Not enough common C-alpha atoms to render the structure.')
    a, b = [np.array([model[key] for key in keys]) for model in models]
    a -= a.mean(axis=0)
    b -= b.mean(axis=0)
    u, _, vt = np.linalg.svd(b.T @ a)
    correction = np.diag([1, 1, np.linalg.det(u @ vt)])
    b = b @ u @ correction @ vt
    # A shared PCA view followed by a fixed camera rotation. Same transform and
    # scale for both models; depth controls drawing order, not a scientific score.
    _, _, axes = np.linalg.svd(a, full_matrices=False)
    angle = np.deg2rad(23)
    camera = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
    projected = [m @ axes.T @ camera for m in (a, b)]
    xy = np.concatenate(projected)[:, :2]
    extent = np.ptp(xy, axis=0)
    scale = min(560 / extent[0], 520 / extent[1])
    center = (xy.min(axis=0) + xy.max(axis=0)) / 2
    for model in projected:
        model[:, :2] = (model[:, :2] - center) * scale + [360, 330]
    segments = []
    for mi, model in enumerate(projected):
        for i in range(len(model) - 1):
            if keys[i][0] != keys[i+1][0] or np.linalg.norm(a[i] - a[i+1]) > 6:
                continue
            p0, p1 = model[i, :2], model[i+1, :2]
            prev_index = i-1 if i > 0 and keys[i-1][0] == keys[i][0] and np.linalg.norm(a[i] - a[i-1]) <= 6 else i
            after_index = i+2 if i+2 < len(model) and keys[i+2][0] == keys[i+1][0] and np.linalg.norm(a[i+2] - a[i+1]) <= 6 else i+1
            prev = model[prev_index, :2]
            after = model[after_index, :2]
            c1, c2 = p0+(p1-prev)/6, p1-(after-p0)/6
            path = f'M{p0[0]:.2f},{p0[1]:.2f} C{c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} {p1[0]:.2f},{p1[1]:.2f}'
            t = i / max(1, len(model)-2)
            color = '#df947f' if mi else '#%02x%02x%02x' % tuple(int(x+(y-x)*t) for x, y in zip((111, 151, 246), (131, 211, 222)))
            opacity, width = ('.58', '5.2') if mi else ('.98', '8.2')
            segment = f'<path d="{path}" stroke="{color}" stroke-width="{width}" opacity="{opacity}"/>'
            segments.append(((model[i, 2]+model[i+1, 2])/2, segment))
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 660" role="img" aria-labelledby="title desc"><title id="title">Two DynoM example conformations</title><desc id="desc">Static C-alpha backbone traces from 9R71 sample 0 and sample 1 in the DynoM repository, aligned on common C-alpha atoms. Blue and coral distinguish the model outputs. This is not a trajectory.</desc><g fill="none" stroke-linecap="round" stroke-linejoin="round">' + ''.join(s for _, s in sorted(segments)) + '</g></svg>'
    (ROOT/'assets'/'protein-ensemble.svg').write_text(svg, encoding='utf-8')
    (ROOT/'assets'/'ensemble-source.json').write_text(json.dumps(dict(sources=records, common_ca_atoms=len(keys), method='Common C-alpha atoms; Kabsch alignment of sample 1 to sample 0; shared PCA projection and fixed camera rotation; Catmull-Rom interpolation for display. Static model outputs, not a trajectory.'), indent=2)+'\n', encoding='utf-8')
    print(f'Rendered {len(keys)} common C-alpha atoms from two model outputs.')


if __name__ == '__main__':
    render()
