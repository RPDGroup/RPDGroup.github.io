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
def render_news(data, home=False):
 records={r['doi']:r for r in data['publications']}
 rows=[records[d] for d in data['home_news_dois']] if home else sorted((r for r in records.values() if r.get('publication_type')!='preprint'),key=lambda r:(-r['year'],r['title']))
 out=[]
 labels={'10.1038/s41597-026-07759-2':'DynoDB','10.1038/s41467-026-73785-8':'GANBase','10.1093/bioinformatics/btag196':'MuFaDDG'}
 for r in rows:
  journal=r['journal'];journal=', '.join(journal) if isinstance(journal,list) else journal
  title=(labels[r['doi']]+' published in '+journal) if home else 'Publication in '+journal
  link=f'<a href="https://doi.org/{e(r["doi"],quote=True)}" target="_blank" rel="noopener">Read paper ↗</a>'
  if home:out.append(f'<article class="news-summary"><time datetime="{r["year"]}">{r["year"]}</time><div><h3>{e(title)}</h3><p>{e(r["title"])}</p>{link}</div></article>')
  else:out.append(f'<article class="news-item"><div><span class="tag">Publication</span><time class="news-date" datetime="{r["year"]}">{r["year"]}</time></div><div><h2>{e(title)}</h2><p>{e(r["title"])}</p>{link}</div></article>')
 return '\n'.join(out)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args()
 data=json.loads((R/'data/publications.json').read_text());html=(R/'index.html').read_text();body=START+'\n'+render(data)+'\n'+END
 updated=re.sub(re.escape(START)+r'.*?'+re.escape(END),lambda _:body,html,flags=re.S)
 for marker,home in [('HOME-NEWS',True),('PAPER-NEWS',False)]:
  start=f'<!-- {marker}:START -->';end=f'<!-- {marker}:END -->'
  assert start in updated and end in updated
  updated=re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda _:start+'\n'+render_news(data,home)+'\n'+end,updated,flags=re.S)
 assert START in html and len({r['doi'] for r in data['publications']})==len(data['publications'])
 if args.check:assert updated==html,'Publication data and HTML differ';print('Publication data and HTML match.')
 else:(R/'index.html').write_text(updated);print('Rendered',len(data['publications']),'publications.')
if __name__=='__main__':main()
