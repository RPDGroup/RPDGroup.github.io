#!/usr/bin/env python3
"""Render verified publications from curated source-backed metadata."""
import argparse,json,re
from pathlib import Path
from html import escape as e
R=Path(__file__).resolve().parents[1]
START='<!-- PUBLICATIONS:START -->';END='<!-- PUBLICATIONS:END -->'
def render(data):
 out=[]
 for r in sorted(data['publications'],key=lambda r:(-r['year'],r.get('publication_type')=='preprint',r['title'])):
  journal=r.get('journal','');journal=', '.join(journal) if isinstance(journal,list) else journal
  kind='Preprint' if r.get('publication_type')=='preprint' else ('Conference paper' if 'IEEE' in journal else 'Research article')
  info=[journal]+[str(r[k]) for k in ['volume','issue','article_number','page'] if r.get(k)]
  first=r.get('first_or_joint_first_authors') or []
  lead=[a for a in first if a in data['group_names']]
  corr=[a for a in (r.get('corresponding_authors') or []) if a in data['group_names']]
  roles=[]
  if lead:roles.append(('Co-first authors: ' if len(first)>1 else 'First author: ')+', '.join(lead))
  if corr:roles.append('Corresponding author: '+', '.join(corr))
  assert roles and r['sources'] and r['doi']
  authors=', '.join(r['authors'])
  note='<p>Author-name note: Zilin Ren is printed as “Zhuli Ren” in the original article.</p>' if r.get('identity_note') else '' 
  out.append(f'<article class="citation"><div class="citation-year">{r["year"]}</div><div><span class="tag">{e(journal)} · {kind}</span><h2>{e(r["title"])}</h2><p>{e(authors)}</p><p>{e(" · ".join(x for x in info if x))}</p><p><strong>{e(" · ".join(roles))}</strong></p>{note}<div class="project-links"><a href="https://doi.org/{e(r["doi"],quote=True)}" target="_blank" rel="noopener">{"Preprint" if kind=="Preprint" else "Publisher page"} ↗</a></div></div></article>')
 return '\n'.join(out)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args()
 data=json.loads((R/'data/publications.json').read_text());html=(R/'index.html').read_text();body=START+'\n'+render(data)+'\n'+END
 updated=re.sub(re.escape(START)+r'.*?'+re.escape(END),lambda _:body,html,flags=re.S)
 assert START in html and len({r['doi'] for r in data['publications']})==len(data['publications'])
 if args.check:assert updated==html,'Publication data and HTML differ';print('Publication data and HTML match.')
 else:(R/'index.html').write_text(updated);print('Rendered',len(data['publications']),'publications.')
if __name__=='__main__':main()
