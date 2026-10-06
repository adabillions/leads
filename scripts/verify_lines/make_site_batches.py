"""Build writer batches that carry what each company's own website says.
Usage: python3 make_site_batches.py <corrected.csv> <sites.jsonl> <batches_dir> [batch_size]
Requires crawl_sites.py output. Companies whose site could not be fetched are written to <batches_dir>/unreachable.txt
so they can fall back to the facts-only writing prompt.
"""
import csv,json,re,sys,os
P,SITES,D=sys.argv[1:4]; B=int(sys.argv[4]) if len(sys.argv)>4 else 100
os.makedirs(D,exist_ok=True)
rows=list(csv.DictReader(open(P,newline='',encoding='utf-8')))
def _norm(j):
    """Accept both crawl_sites.py (long keys) and crawl_domains.py (compact keys) records."""
    if 'domain' in j: return j
    return {'domain':j.get('d'),'status':j.get('s'),'title':j.get('t',''),'description':j.get('m',''),'h1':j.get('h',''),'text':j.get('x',''),'about_text':j.get('a',''),'tech':j.get('k',[]),'error':j.get('e')}
sites={}
for line in open(SITES):
    try: j=_norm(json.loads(line)); sites[j['domain']]=j
    except Exception: pass
SUFFIX=r'(,?\s*(L\.?L\.?C\.?|Inc\.?|Corp\.?|Corporation|Ltd\.?|L\.?P\.?|P\.?L\.?L\.?C\.?|P\.?C\.?|Co\.?|Company|Incorporated|Limited))+\s*$'
def short(cn): s=re.sub(SUFFIX,'',cn.strip(),flags=re.I).strip().rstrip(','); return s or cn
def dom(u): return re.sub(r'^https?://(www\.)?','',u.lower()).split('/')[0]
def clean(s,n): return re.sub(r'\s+',' ',s or '').strip()[:n]
ok=[];bad=[]
for o in rows:
    s=sites.get(dom(o['website']))
    if not s or not s.get('status') or s['status']>=400 or not (s.get('text') or s.get('description')): bad.append(o['row']); continue
    name=o['trading_name'] if o.get('name_website_match')=='DBA' and o.get('trading_name') else short(o['company_name'])
    ok.append((o,s,name))
for i in range(0,len(ok),B):
    with open(f'{D}/batch_{i//B+1:03d}.md','w') as f:
        for o,s,name in ok[i:i+B]:
            f.write(f"ROW {o['row']} | NAME: {name} | DOMAIN: {dom(o['website'])} | LOCATION: {o['city']}, {o['state']} | BUCKET: {o['industry']}\n"
                    f"  SITE TITLE: {clean(s.get('title'),120)}\n  SITE DESCRIPTION: {clean(s.get('description'),300)}\n  SITE HEADINGS: {clean(s.get('h1'),200)}\n"
                    f"  SITE TEXT: {clean(s.get('text'),700)}\n  ABOUT TEXT: {clean(s.get('about_text'),500)}\n  TECH SEEN ON SITE: {', '.join(s.get('tech',[])) or 'none'}\n")
open(f'{D}/unreachable.txt','w').write('\n'.join(bad))
print(f'batches {(len(ok)+B-1)//B} companies {len(ok)}; unreachable {len(bad)}')
