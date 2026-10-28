#!/usr/bin/env python3
"""Render the activity gallery and homepage selection as static HTML."""
import argparse
from html import escape
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {'lab': 'Lab life', 'academic': 'Academic exchange', 'together': 'Group moments'}


def asset(value):
    if not isinstance(value, str):
        raise ValueError('Image paths must be text')
    path = Path(value)
    if path.is_absolute() or not path.parts or path.parts[0] != 'assets' or '..' in path.parts:
        raise ValueError('Images must be local files inside assets/')
    resolved = (ROOT / path).resolve()
    if not resolved.is_relative_to((ROOT / 'assets').resolve()) or not resolved.is_file():
        raise ValueError(f'Missing or invalid gallery image: {value}')
    return value


def normalize(photo):
    if not isinstance(photo, dict):
        raise ValueError('Every photograph must be an object')
    if set(photo) != {'id', 'category', 'title', 'thumbnail', 'image'}:
        raise ValueError('Expected id, category, title, thumbnail and image')
    if not isinstance(photo['id'], str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', photo['id']):
        raise ValueError('Photograph ids must be lowercase slugs')
    if photo['category'] not in CATEGORIES:
        raise ValueError('Unknown activity category')
    if not isinstance(photo['title'], str) or not photo['title'].strip():
        raise ValueError('Each photograph needs a title')
    thumb = photo['thumbnail']
    if not isinstance(thumb, dict) or set(thumb) != {'src', 'width', 'height'}:
        raise ValueError('Each thumbnail needs src, width and height')
    for field in ('width', 'height'):
        if type(thumb[field]) is not int or thumb[field] <= 0:
            raise ValueError('Thumbnail dimensions must be positive integers')
    return {**photo, 'title': photo['title'].strip(), 'image': asset(photo['image']),
            'thumbnail': {**thumb, 'src': asset(thumb['src'])}}


def photograph(photo, featured=False):
    esc = lambda value: escape(str(value), quote=True)
    thumb = photo['thumbnail']
    group = 'home-activities' if featured else 'activities'
    attributes = '' if featured else f' data-activity-record data-activity-category="{photo["category"]}"'
    cls = 'activity-preview' if featured else 'activity-card'
    return (f'<figure class="{cls}"{attributes}>'
            f'<a class="activity-photo" href="{esc(photo["image"])}" data-media data-gallery="{group}" '
            f'data-title="{esc(photo["title"])}" aria-label="View photograph: {esc(photo["title"])}" target="_blank" rel="noopener">'
            f'<img src="{esc(thumb["src"])}" alt="Ren Protein Design Group: {esc(photo["title"])}" '
            f'width="{thumb["width"]}" height="{thumb["height"]}" loading="lazy" decoding="async"></a>'
            f'<figcaption><span class="activity-tag">{CATEGORIES[photo["category"]]}</span>'
            f'<h3>{esc(photo["title"])}</h3></figcaption></figure>')


def replace_block(source, name, body):
    start, end = f'<!-- {name}:START -->', f'<!-- {name}:END -->'
    if source.count(start) != 1 or source.count(end) != 1:
        raise ValueError(f'Expected one {name} marker pair')
    before, rest = source.split(start)
    _, after = rest.split(end)
    return before + start + '\n' + body + '\n' + end + after


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = json.loads((ROOT / 'data/activities.json').read_text(encoding='utf-8'))
    if not isinstance(data, dict) or data.get('version') != 1 or not isinstance(data.get('photos'), list):
        raise ValueError('Expected version 1 and a photos list')
    photos = [normalize(photo) for photo in data['photos']]
    by_id = {photo['id']: photo for photo in photos}
    if len(by_id) != len(photos):
        raise ValueError('Photograph ids must be unique')
    featured = data.get('featured', [])
    if not isinstance(featured, list) or len(featured) != 3 or len(set(featured)) != 3 or any(key not in by_id for key in featured):
        raise ValueError('Select three different existing photographs for the homepage')
    gallery = ['<div class="activities-toolbar"><div class="activity-filters" role="group" aria-label="Activity category" hidden>']
    for category, label in [('all', 'All photographs'), *CATEGORIES.items()]:
        gallery.append(f'<button type="button" data-activity-filter="{category}" aria-pressed="{str(category == "all").lower()}">{label}</button>')
    gallery.extend(['</div>', f'<p id="activity-count" role="status" aria-live="polite" aria-atomic="true">{len(photos)} photographs</p></div>',
                    '<div class="activity-gallery" id="activity-gallery">', *(photograph(photo) for photo in photos),
                    '</div><p class="activity-empty" hidden>No photographs in this category yet.</p>'])
    path = ROOT / 'index.html'
    source = path.read_text(encoding='utf-8')
    result = replace_block(source, 'ACTIVITY-PREVIEW', '\n'.join(photograph(by_id[key], True) for key in featured))
    result = replace_block(result, 'ACTIVITY-GALLERY', '\n'.join(gallery))
    # New markup must load matching styles/scripts rather than a previous cache.
    for file in ('assets/site.css', 'assets/site.js', 'assets/members.js', 'assets/activities.js'):
        digest = hashlib.sha256((ROOT / file).read_bytes()).hexdigest()[:12]
        pattern = r'((?:href|src)="' + re.escape(file) + r')(?:\?v=[^"]*)?"'
        result = re.sub(pattern, lambda match: match.group(1) + '?v=' + digest + '"', result)
    if args.check:
        if source != result:
            raise SystemExit('Activity HTML is stale. Run python3 scripts/update-activities.py')
        print('Activity data and static HTML match.')
    else:
        path.write_text(result, encoding='utf-8')
        print(f'Rendered {len(photos)} activity photographs and {len(featured)} homepage selections.')


if __name__ == '__main__':
    main()
