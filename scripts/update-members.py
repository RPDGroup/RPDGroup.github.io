#!/usr/bin/env python3
"""Render the public member directory as static HTML. Uses only Python's stdlib."""
import argparse
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
START, END = '<!-- MEMBERS:START -->', '<!-- MEMBERS:END -->'
GROUPS = {'leader': 'Leader', 'phd': 'PhD students', 'master': "Master's students", 'alumni': 'Alumni', 'other': 'Other members'}


def text(value, field):
    if not isinstance(value, str):
        raise ValueError(f'{field} must be text')
    return value.strip()


def lines(value, field):
    if not isinstance(value, list):
        raise ValueError(f'{field} must be a list of text entries')
    return [entry for item in value if (entry := text(item, field))]


def initials(name):
    words = name.split()
    return ''.join(word[0] for word in words[:2]).upper() if len(words) > 1 else name[:2]


def portrait(member):
    if not member['photo']:
        return f'<span class="member-portrait member-initials" aria-hidden="true">{escape(initials(member["name"]))}</span>'
    return f'<span class="member-portrait"><img src="{escape(member["photo"], quote=True)}" alt="{escape(member["name"], quote=True)}" loading="lazy"></span>'


def normalize(record):
    if not isinstance(record, dict):
        raise ValueError('Every member must be an object')
    allowed = {'id', 'name', 'name_local', 'role', 'status', 'group', 'admission_year', 'photo', 'period', 'contact', 'education', 'research', 'bio', 'links'}
    unknown = set(record) - allowed
    if unknown:
        raise ValueError(f'Unknown member fields: {sorted(unknown)}')
    member = {key: text(record.get(key, ''), key) for key in ('id', 'name', 'name_local', 'role', 'photo', 'period', 'research', 'bio')}
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', member['id']):
        raise ValueError('Each id must be a unique lowercase slug')
    if not member['name']:
        raise ValueError(f'{member["id"]}: name is required')
    member['status'] = record.get('status', 'current')
    if member['status'] not in ('current', 'previous', 'future'):
        raise ValueError(f'{member["id"]}: invalid status')
    member['group'] = record.get('group', 'alumni' if member['status'] == 'previous' else 'other')
    if member['group'] not in GROUPS:
        raise ValueError(f'{member["id"]}: invalid member group')
    member['admission_year'] = record.get('admission_year')
    if member['admission_year'] is not None and (type(member['admission_year']) is not int or not 1900 <= member['admission_year'] <= 2100):
        raise ValueError(f'{member["id"]}: admission year must be an integer between 1900 and 2100')
    if member['photo']:
        path = Path(member['photo'])
        if path.is_absolute() or not path.parts or path.parts[0] != 'assets' or '..' in path.parts:
            raise ValueError(f'{member["id"]}: photo must be a local path inside assets/')
        resolved = (ROOT / path).resolve()
        if not resolved.is_relative_to((ROOT / 'assets').resolve()) or not resolved.is_file():
            raise ValueError(f'{member["id"]}: photo file is missing or outside assets/')
        if path.suffix.lower() not in ('.jpg', '.jpeg', '.png', '.webp', '.avif'):
            raise ValueError(f'{member["id"]}: unsupported photo format')
    member['contact'] = lines(record.get('contact', []), 'contact')
    member['education'] = lines(record.get('education', []), 'education')
    member['links'] = []
    if not isinstance(record.get('links', []), list):
        raise ValueError('links must be a list')
    for link in record.get('links', []):
        if not isinstance(link, dict) or set(link) != {'label', 'url'}:
            raise ValueError('Each link requires label and url')
        label, url = text(link['label'], 'link label'), text(link['url'], 'link URL')
        parsed = urlsplit(url)
        if not label or parsed.scheme not in ('https', 'http') or not parsed.netloc or parsed.username or parsed.password:
            raise ValueError('Profile links must be labeled public HTTP(S) URLs')
        member['links'].append({'label': label, 'url': url})
    return member


def render_member(member):
    esc = lambda value: escape(value, quote=True)
    name = esc(member['name'])
    parts = [f'<details class="member-profile" id="member-{member["id"]}" data-member-record data-member-status="{member["status"]}" data-member-group="{member["group"]}">',
             '<summary class="member-card">', portrait(member), f'<h3 class="member-name">{name}</h3>']
    if member['name_local']:
        parts.append(f'<p class="member-local">{esc(member["name_local"])}</p>')
    if member['role']:
        parts.append(f'<p class="member-role">{esc(member["role"])}</p>')
    if member['admission_year'] is not None:
        parts.append(f'<p class="member-intake">{member["admission_year"]} intake</p>')
    parts.append('<span class="member-hint">View profile <span aria-hidden="true">↗</span></span></summary><div class="member-details">')
    if member['period']:
        parts.append(f'<p class="member-period">{esc(member["period"])}</p>')
    if member['admission_year'] is not None:
        parts.append(f'<p class="member-period">Admission year: {member["admission_year"]}</p>')
    for paragraph in member['bio'].split('\n\n'):
        if paragraph.strip():
            parts.append(f'<p>{esc(paragraph.strip())}</p>')
    for heading, entries in [('Contact', member['contact']), ('Education', member['education'])]:
        if entries:
            parts.append(f'<section><h4>{heading}</h4><ul>' + ''.join(f'<li>{esc(entry)}</li>' for entry in entries) + '</ul></section>')
    if member['research']:
        parts.append('<section><h4>Research</h4>' + ''.join(f'<p>{esc(paragraph.strip())}</p>' for paragraph in member['research'].split('\n\n') if paragraph.strip()) + '</section>')
    if member['links']:
        parts.append('<div class="member-links">' + ''.join(f'<a href="{esc(link["url"])}" target="_blank" rel="noopener">{esc(link["label"])} ↗</a>' for link in member['links']) + '</div>')
    if not any(member[key] for key in ('admission_year', 'period', 'bio', 'contact', 'education', 'research', 'links')):
        parts.append('<p>More about this member will be added soon.</p>')
    parts.append('</div></details>')
    return ''.join(parts)


def render_directory(records):
    members = [normalize(record) for record in records]
    if len({member['id'] for member in members}) != len(members):
        raise ValueError('Member ids must be unique')
    output = ['<div class="member-sections" id="members-grid">']
    for key, label in GROUPS.items():
        group = [member for member in members if member['group'] == key]
        if not group:
            continue
        quantity = f'{len(group)} ' + ('member' if len(group) == 1 else 'members')
        output.extend([f'<section class="member-section" data-member-section aria-labelledby="member-group-{key}">',
                       f'<div class="member-section-heading"><h2 id="member-group-{key}">{escape(label)}</h2><p data-member-section-count>{quantity}</p></div>',
                       '<div class="members-grid">', *(render_member(member) for member in group), '</div></section>'])
    output.append('</div>')
    output.append('<div class="members-empty" id="members-empty"' + (' hidden' if members else '') + '>')
    if not members:
        output.append('<div class="member-placeholder-grid" aria-hidden="true">' + '<span class="member-placeholder"><i></i></span>' * 6 + '</div>')
    output.append('<h2>' + ('No matching profiles' if members else 'Member profiles coming soon') + '</h2>')
    output.append('<p>' + ('Try another category or clear your search.' if members else 'Individual profiles will be added here. Meet our group in the photograph below.') + '</p></div>')
    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=ROOT / 'data/members.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'index.html')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = json.loads(args.data.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or data.get('version') != 1 or not isinstance(data.get('members'), list):
        raise ValueError('Expected version 1 with a members list')
    source = (ROOT / 'index.html').read_text(encoding='utf-8')
    if source.count(START) != 1 or source.count(END) != 1:
        raise ValueError('Expected one member directory marker pair')
    before, rest = source.split(START)
    _, after = rest.split(END)
    result = before + START + '\n' + render_directory(data['members']) + '\n' + END + after
    if args.check:
        if args.output.read_text(encoding='utf-8') != result:
            raise SystemExit('Member HTML is stale. Run python3 scripts/update-members.py')
        print('Member data and static HTML match.')
    else:
        args.output.write_text(result, encoding='utf-8')
        print(f'Rendered {len(data["members"])} member profiles.')


if __name__ == '__main__':
    main()
