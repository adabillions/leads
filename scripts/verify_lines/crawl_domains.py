"""Fetch each domain's homepage (and about page when linked) and write compact summaries as JSONL.
Usage: python3 crawl_domains.py <domains.txt> <out.jsonl> [workers]
Record: {d: domain, s: status, t: title, m: meta description, h: h1s, x: visible text (first 900 chars), a: about text (600), k: tech markers}
"""
import sys,re,json,time,concurrent.futures as cf
import requests
from bs4 import BeautifulSoup
SRC,OUT=sys.argv[1],sys.argv[2]; W=int(sys.argv[3]) if len(sys.argv)>3 else 48
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Accept-Language':'en-US,en;q=0.9'}
TECH={'hubspot':r'hs-scripts\.com|hubspot','zendesk':r'zdassets|zendesk','intercom':r'intercom','salesforce':r'pardot|salesforce','freshdesk':r'freshdesk|freshworks','zoho':r'zoho'}
def text_of(soup,limit):
    for t in soup(['script','style','noscript','svg','nav','footer','header','form','iframe']): t.decompose()
    s=re.sub(r'\s+',' ',soup.get_text(' ')).strip()
    s=re.sub(r'(?i)(we use cookies|this website uses cookies|accept all cookies|skip to (main )?content)[^.]*\.?','',s)
    return s[:limit]
def fetch(d):
    rec={'d':d}
    for scheme in ('https://','http://'):
        try:
            r=requests.get(scheme+d,headers=UA,timeout=12,allow_redirects=True)
            rec['s']=r.status_code
            if r.status_code>=400 or 'text/html' not in r.headers.get('content-type','text/html'): continue
            html=r.text[:1500000]; soup=BeautifulSoup(html,'lxml')
            rec['t']=(soup.title.get_text(' ',strip=True) if soup.title else '')[:140]
            md=soup.find('meta',attrs={'name':re.compile('^description$',re.I)}) or soup.find('meta',attrs={'property':'og:description'})
            rec['m']=(md.get('content','') if md else '').strip()[:300]
            rec['h']=' | '.join(h.get_text(' ',strip=True) for h in soup.find_all(['h1','h2'])[:4])[:200]
            rec['k']=[k for k,p in TECH.items() if re.search(p,html,re.I)]
            about=None
            for a in soup.find_all('a',href=True):
                if re.search(r'about|who-we-are|our-story|company',a['href'],re.I): about=a['href']; break
            rec['x']=text_of(soup,900)
            if about:
                try:
                    ar=requests.get(requests.compat.urljoin(r.url,about),headers=UA,timeout=10)
                    if ar.ok: rec['a']=text_of(BeautifulSoup(ar.text[:1000000],'lxml'),600)
                except Exception: pass
            return rec
        except Exception as e:
            rec['e']=type(e).__name__
    return rec
doms=[l.strip() for l in open(SRC) if l.strip()]
t0=time.time(); n=0
with open(OUT,'w') as fh, cf.ThreadPoolExecutor(W) as ex:
    for rec in ex.map(fetch,doms):
        fh.write(json.dumps(rec,ensure_ascii=False)+'\n'); n+=1
        if n%500==0: fh.flush(); print(f'{n}/{len(doms)} {time.time()-t0:.0f}s',flush=True)
print('done',n,f'{time.time()-t0:.0f}s')
