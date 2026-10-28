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


def homepage_carousel(data, by_id):
    photos = list(by_id.values())
    if not photos:
        raise ValueError('The homepage needs at least one photograph')
    focal_points = data.get('homepage_focal_points', {})
    if not isinstance(focal_points, dict) or any(key not in by_id for key in focal_points):
        raise ValueError('Homepage focal points must reference existing photographs')
    slides = []
    for start in range(0, len(photos), 3):
        group = photos[start:start + 3]
        categories = {photo['category'] for photo in group}
        label = CATEGORIES[group[0]['category']] if len(categories) == 1 else 'Life at RPDGroup'
        slides.append({'label': label, 'photos': [{'id': photo['id'], 'focus': focal_points.get(photo['id'], [50, 50])} for photo in group]})
    image_sizes = {}
    for name in ('sources.json', 'album-sources.json', 'upload-sources.json'):
        manifest = json.loads((ROOT / 'assets/activities' / name).read_text(encoding='utf-8'))
        for photo in manifest['photographs']:
            for output in photo['outputs']:
                image_sizes[output['file']] = (output['width'], output['height'])
    esc = lambda value: escape(str(value), quote=True)
    body = ['<section class="photo-hero" data-photo-carousel data-interval="8000" '
            'aria-label="Group photographs" aria-roledescription="carousel">',
            '<div class="photo-wall" id="home-photo-wall" aria-live="off">']
    options = []
    for i, slide in enumerate(slides):
        label, selections = slide.get('label'), slide.get('photos')
        if not isinstance(label, str) or not label.strip() or not isinstance(selections, list) or not 1 <= len(selections) <= 3:
            raise ValueError('Each homepage photo set needs a label and one to three photographs')
        ids = [selection.get('id') for selection in selections if isinstance(selection, dict)]
        if len(ids) != len(selections) or len(set(ids)) != len(ids) or any(key not in by_id for key in ids):
            raise ValueError('Homepage photo sets must reference different existing photographs')
        hidden = ' hidden' if i else ''
        layout = ' is-single' if len(ids) == 1 else ' is-pair' if len(ids) == 2 else ''
        body.append(f'<div class="photo-slide{layout}" role="group" aria-roledescription="slide" '
                    f'aria-label="{i + 1} of {len(slides)}: {esc(label)}" data-photo-label="{esc(label)}"{hidden}>')
        for j, selection in enumerate(selections):
            photo = by_id[selection['id']]
            focus = selection.get('focus', [50, 50])
            if not isinstance(focus, list) or len(focus) != 2 or any(type(n) is not int or not 0 <= n <= 100 for n in focus):
                raise ValueError('Photograph focal points must be two percentages from zero to 100')
            full_width, full_height = image_sizes[photo['image']]
            thumb = photo['thumbnail']
            sizes = '(max-width: 640px) 100vw, (max-width: 1600px) 58.33vw, 934px' if j == 0 else '(max-width: 640px) 50vw, (max-width: 1600px) 41.67vw, 667px'
            loading = 'eager' if i == 0 else 'lazy'
            priority = ' fetchpriority="high"' if i == j == 0 else ''
            srcset = f'{esc(photo["image"])} {full_width}w'
            if thumb['width'] < full_width:
                srcset = f'{esc(thumb["src"])} {thumb["width"]}w, ' + srcset
            body.append(f'<a class="wall-photo wall-{j + 1}" href="{esc(photo["image"])}" data-media '
                        f'data-gallery="hero-photos" data-title="{esc(photo["title"])}" '
                        f'aria-label="View photograph: {esc(photo["title"])}" target="_blank" rel="noopener" '
                        f'style="--photo-focus:{focus[0]}% {focus[1]}%">'
                        f'<img src="{esc(thumb["src"])}" srcset="{srcset}" sizes="{sizes}" '
                        f'alt="Ren Protein Design Group: {esc(photo["title"])}" width="{full_width}" '
                        f'height="{full_height}" loading="{loading}" decoding="async"{priority}>'
                        f'<span class="photo-caption">{esc(photo["title"])}<span aria-hidden="true">↗</span></span></a>')
        body.append('</div>')
        options.append(f'<option value="{i}">{i + 1:02d} / {len(slides):02d}</option>')
    body.extend(['</div>', '<div class="photo-controls" hidden>',
                 f'<p class="photo-set-name"><span data-photo-label>{esc(slides[0]["label"])}</span>'
                 f'<span class="photo-set-count">{len(photos)} photos</span></p>',
                 '<div class="photo-control-actions"><button type="button" class="photo-play" data-photo-play '
                 'aria-label="Pause photo rotation" aria-controls="home-photo-wall">'
                 '<span data-photo-play-icon aria-hidden="true">Ⅱ</span><span data-photo-play-text>Pause</span></button>',
                 '<button type="button" class="photo-arrow" data-photo-prev aria-label="Previous photo set" '
                 'aria-controls="home-photo-wall">←</button>',
                 '<select class="photo-select" data-photo-select aria-label="Choose photo set" '
                 'aria-controls="home-photo-wall">', *options, '</select>',
                 '<button type="button" class="photo-arrow" data-photo-next aria-label="Next photo set" '
                 'aria-controls="home-photo-wall">→</button></div>',
                 '<a class="photo-all" href="#activities">All photos <span aria-hidden="true">↗</span></a>',
                 '</div><p class="photo-announcement" role="status" aria-live="polite" aria-atomic="true"></p></section>'])
    return '\n'.join(body)


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
    result = replace_block(result, 'PHOTO-CAROUSEL', homepage_carousel(data, by_id))
    # New markup must load matching styles/scripts rather than a previous cache.
    for file in ('assets/site.css', 'assets/site.js', 'assets/members.js', 'assets/activities.js', 'assets/home-photos.js'):
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
