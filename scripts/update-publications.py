#!/usr/bin/env python3
"""Render verified publications from curated source-backed metadata."""
import argparse,json,re
from pathlib import Path
from html import escape as e
R=Path(__file__).resolve().parents[1]
START='<!-- PUBLICATIONS:START -->';END='<!-- PUBLICATIONS:END -->'
FIGURES={
 '10.1038/s41597-026-07759-2':('assets/papers/dynodb-cover.webp','DynoDB conformational ensemble cover illustration'),
 '10.1038/s41467-026-73785-8':('assets/papers/ganbase-cover.webp','GANBase nanopore adaptive sequencing cover illustration'),
 '10.1016/j.virs.2026.03.015':('assets/papers/sars-jn1-cover.webp','SARS-CoV-2 JN.1 genomic epidemiology cover illustration'),
 '10.1093/bioinformatics/btag196':('assets/papers/mufaddg-cover.webp','MuFaDDG protein stability prediction cover illustration'),
 '10.21203/rs.3.rs-9549778/v1':('assets/dynom-model.webp','DynoM model architecture'),
 '10.21203/rs.3.rs-9629622/v1':('assets/papers/enzyme-atlas-cover.webp','Microbial enzyme atlas multimodal AI cover illustration'),
 '10.1016/j.crmicr.2025.100457':('assets/papers/mrna-vaccine-cover.webp','T cell-based mRNA influenza vaccine cover illustration'),
 '10.1093/gigascience/giaf018':('assets/papers/nanopore-deletion-cover.webp','Nanopore short deletion variation filtering cover illustration'),
 '10.1093/bib/bbae579':('assets/papers/deeppfp-cover.webp','DeepPFP multi-task protein function prediction cover illustration'),
 '10.1371/journal.pone.0335520':('assets/papers/omicron-forecast-cover.webp','Omicron lineage prevalence forecasting cover illustration'),
 '10.1016/j.jhazmat.2025.137336':('assets/papers/peg-hydrolase-cover.webp','N-terminal PEGylation of organophosphorus hydrolase cover illustration'),
 '10.1142/S0219720025500209':('assets/papers/plmabfw-cover.webp','PLMABFW antibody-antigen interaction cover illustration'),
 '10.1016/j.bpc.2024.107253':('assets/papers/antibody-benchmark-cover.webp','Antibody-antigen binding affinity benchmark cover illustration'),
 '10.1093/bioinformatics/btae330':('assets/codonbert-architecture.webp','CodonBERT architecture'),
 '10.1093/bib/bbae472':('assets/papers/nastra-cover.webp','NASTRA nanopore STR analysis cover illustration'),
 '10.3934/era.2023253':('assets/papers/ras-pathway-cover.webp','Pan-cancer RAS pathway graph autoencoder cover illustration'),
 '10.3934/era.2023276':('assets/papers/mtna-acetylation-cover.webp','MTNA N-terminal protein acetylation cover illustration'),
 '10.1186/s12859-023-05141-2':('assets/papers/oncogenic-gan-cover.webp','Semi-supervised GAN oncogenic variant prediction cover illustration'),
 '10.1109/BIBM58861.2023.10385963':('assets/papers/plmthp-cover.webp','PLMTHP tumor homing peptide prediction cover illustration'),
 '10.1093/bioinformatics/btad646':('assets/papers/thplm-cover.webp','THPLM protein stability change prediction cover illustration'),
 '10.3389/fmicb.2022.929241':('assets/papers/pcr-nanopore-cover.webp','Rapid PCR-based nanopore adaptive sequencing cover illustration'),
 '10.1007/s00414-021-02604-0':('assets/papers/forensic-minion-cover.webp','Forensic nanopore MinION STR and SNP sequencing cover illustration'),
}
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
  fig=FIGURES.get(r['doi'])
  thumb=f'<a class="citation-thumb" href="{e(fig[0],quote=True)}" data-media data-title="{e(r["title"],quote=True)}" target="_blank" rel="noopener"><img src="{e(fig[0],quote=True)}" alt="{e(fig[1],quote=True)}" loading="lazy" decoding="async"></a>' if fig else ''
  cls='citation has-thumb' if fig else 'citation'
  out.append(f'<article class="{cls}"><div class="citation-year">{r["year"]}</div><div><span class="tag">{e(journal)} · {kind}</span><h2>{e(r["title"])}</h2><p>{e(authors)}</p><p>{e(" · ".join(x for x in info if x))}</p><p><strong>{e(" · ".join(roles))}</strong></p>{note}<div class="project-links"><a href="https://doi.org/{e(r["doi"],quote=True)}" target="_blank" rel="noopener">{"Preprint" if kind=="Preprint" else "Publisher page"} ↗</a></div></div>{thumb}</article>')
 return '\n'.join(out)
def render_news(data, home=False):
 records={r['doi']:r for r in data['publications']}
 rows=[records[d] for d in data['home_news_dois']] if home else sorted((r for r in records.values() if r.get('publication_type')!='preprint'),key=lambda r:(-r['year'],r['title']))
 out=[]
 labels={'10.1038/s41597-026-07759-2':'DynoDB','10.1038/s41467-026-73785-8':'GANBase','10.1093/bioinformatics/btag196':'MuFaDDG','10.1016/j.virs.2026.03.015':'SARS-CoV-2 JN.1'}
 for r in rows:
  journal=r['journal'];journal=', '.join(journal) if isinstance(journal,list) else journal
  title=(labels[r['doi']]+' published in '+journal) if home else 'Publication in '+journal
  url=f'https://doi.org/{e(r["doi"],quote=True)}'
  link=f'<a class="text-link" href="{url}" target="_blank" rel="noopener">Read paper →</a>' if home else f'<a href="{url}" target="_blank" rel="noopener">Read paper ↗</a>'
  fig=FIGURES.get(r['doi'])
  if home:
   cover=f'<a class="news-cover" href="{url}" target="_blank" rel="noopener"><img src="{e(fig[0],quote=True)}" alt="{e(fig[1],quote=True)}" width="1280" height="720" loading="lazy" decoding="async"></a>' if fig else ''
   out.append(f'<article class="news-summary">{cover}<div class="news-summary-body"><div class="news-meta"><time datetime="{r["year"]}">{r["year"]}</time><span>{e(journal)}</span></div><h3><a href="{url}" target="_blank" rel="noopener">{e(title)}</a></h3><p>{e(r["title"])}</p>{link}</div></article>')
  else:
   thumb=f'<a class="news-item-thumb" href="{e(fig[0],quote=True)}" data-media data-title="{e(r["title"],quote=True)}" target="_blank" rel="noopener"><img src="{e(fig[0],quote=True)}" alt="{e(fig[1],quote=True)}" loading="lazy" decoding="async"></a>' if fig else ''
   cls='news-item has-thumb' if fig else 'news-item'
   out.append(f'<article class="{cls}"><div><span class="tag">Publication</span><time class="news-date" datetime="{r["year"]}">{r["year"]}</time></div><div><h2>{e(title)}</h2><p>{e(r["title"])}</p>{link}</div>{thumb}</article>')
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
