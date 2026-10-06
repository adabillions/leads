"""Fetch every company homepage and store what the site says about itself.
Usage: python3 crawl_sites.py <corrected.csv> <out_sites.jsonl> [workers]
Resumable: domains already in the output file are skipped. Needs network access to the company domains.
Each JSONL record: {domain, status, final_url, title, description, h1, text, about_text, tech}
"""
import csv,re,sys,json,os,time,concurrent.futures as cf
import requests
from bs4 import BeautifulSoup
P,OUT=sys.argv[1],sys.argv[2]; W=int(sys.argv[3]) if len(sys.argv)>3 else 32
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Accept-Language':'en-US,en;q=0.9'}
TECH={'hubspot':r'hs-scripts\.com|hubspot','zendesk':r'zdassets|zendesk','intercom':r'intercom','salesforce':r'pardot|salesforce|force\.com','freshdesk':r'freshdesk|freshworks','zoho':r'zoho','drift':r'drift\.com'}
def dom(u): return re.sub(r'^https?://(www\.)?','',u.lower()).split('/')[0]
def text_of(soup,limit):
    for t in soup(['script','style','noscript','svg','nav','footer','header','form']): t.decompose()
    s=re.sub(r'\s+',' ',soup.get_text(' ')).strip(); return s[:limit]
def fetch(d):
    rec={'domain':d,'status':None}
    for scheme in ('https://','http://'):
        try:
            r=requests.get(scheme+d,headers=UA,timeout=15,allow_redirects=True)
            rec['status']=r.status_code; rec['final_url']=r.url
            if r.status_code>=400: continue
            html=r.text; soup=BeautifulSoup(html,'lxml')
            rec['title']=(soup.title.string.strip() if soup.title and soup.title.string else '')
            md=soup.find('meta',attrs={'name':re.compile('^description$',re.I)}) or soup.find('meta',attrs={'property':'og:description'})
            rec['description']=(md.get('content','') if md else '').strip()[:500]
            rec['h1']=' | '.join(h.get_text(' ',strip=True) for h in soup.find_all('h1')[:3])[:300]
            rec['tech']=[k for k,p in TECH.items() if re.search(p,html,re.I)]
            about=None
            for a in soup.find_all('a',href=True):
                if re.search(r'about|who-we-are|company|our-story',a['href'],re.I): about=a['href']; break
            rec['text']=text_of(soup,2000)
            if about:
                try:
                    au=requests.compat.urljoin(r.url,about); ar=requests.get(au,headers=UA,timeout=15)
                    if ar.ok: rec['about_text']=text_of(BeautifulSoup(ar.text,'lxml'),2000)
                except Exception: pass
            return rec
        except Exception as e:
            rec['error']=str(e)[:120]
    return rec
rows=list(csv.DictReader(open(P,newline='',encoding='utf-8')))
domains=sorted({dom(r['website']) for r in rows if r['website']})
done=set()
if os.path.exists(OUT):
    for line in open(OUT): 
        try: done.add(json.loads(line)['domain'])
        except Exception: pass
todo=[d for d in domains if d not in done]
print(f'{len(domains)} domains, {len(done)} cached, {len(todo)} to fetch, {W} workers')
t0=time.time(); n=0
with open(OUT,'a') as fh, cf.ThreadPoolExecutor(W) as ex:
    for rec in ex.map(fetch,todo):
        fh.write(json.dumps(rec)+'\n'); n+=1
        if n%200==0: fh.flush(); print(f'{n}/{len(todo)} {time.time()-t0:.0f}s',flush=True)
print('done',n,f'{time.time()-t0:.0f}s')
