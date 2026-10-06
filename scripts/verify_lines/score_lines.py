"""Compare each row's company name, website and personalized line with what the company's own site says.
Usage: python3 score_lines.py <corrected.csv> <sites.jsonl> <out.csv>
Adds: site_title, site_summary, site_tech, name_on_site (YES/NO/UNCLEAR), site_fit (OK/WRONG/UNCLEAR), site_fit_note.
Rows judged WRONG (or whose site clearly belongs to another business) get the safe generic line; the original is kept in personalized_line_original.
UNCLEAR rows should go to a model pass (agent_prompt.md style) using site_summary instead of a web search.
"""
import csv,re,sys,json,collections
P,SITES,OUT=sys.argv[1:4]
rows=list(csv.DictReader(open(P,newline='',encoding='utf-8')))
sites={}
for line in open(SITES):
    try: j=json.loads(line); sites[j['domain']]=j
    except Exception: pass
def dom(u): return re.sub(r'^https?://(www\.)?','',u.lower()).split('/')[0]
STOP={'llc','inc','corp','company','group','services','solutions','international','enterprises','holdings','global','technologies','systems','associates','partners','consulting','management','logistics','staffing','properties','security','ltd','limited','incorporated','corporation','america','american','national','the','and'}
SUFFIX=r'(,?\s*(L\.?L\.?C\.?|Inc\.?|Corp\.?|Corporation|Ltd\.?|L\.?P\.?|P\.?L\.?L\.?C\.?|P\.?C\.?|Co\.?|Company|Incorporated|Limited))+\s*$'
def short(cn): s=re.sub(SUFFIX,'',cn.strip(),flags=re.I).strip().rstrip(','); return s or cn
# words that confirm each bucket, and words that contradict it
LEX={
'Education & training (non-university)':(r'training|course|curriculum|learn|workshop|certif|tutor|school|academy|instruct|coaching|e-?learning|students?|classes',r''),
'B2B SaaS / software':(r'software|platform|saas|app\b|cloud|api|automation|analytics|solution',r'staffing|recruit|cpa|accounting firm|law firm|freight'),
'Managed IT / MSP':(r'managed (it|services)|it support|help ?desk|cybersecurity|network|msp|it services|cloud services',r'restaurant|dental|law firm|realty|staffing'),
'Freight brokerage / 3PL':(r'freight|logistics|shipping|carrier|3pl|broker|trucking|transport|courier|deliver|warehouse|supply chain',r''),
'Accounting / CPA firms':(r'cpa|accounting|tax|bookkeeping|audit|payroll|advisory',r''),
'Staffing / recruiting':(r'staffing|recruit|talent|placement|workforce|temp\b|hiring',r'home health|home care'),
'Specialised field service':(r'service|repair|install|maintenance|inspection|technician|hvac|plumb|electric|boiler|elevator',r''),
'Private security':(r'security (guard|officer|services|patrol)|guard|patrol|armed|unarmed|protective services',r'cabling|network|software|alarm'),
'Restoration / disaster recovery':(r'restoration|water damage|fire damage|mold|remediation|disaster|cleanup|biohazard',r'environmental consulting|engineering'),
'Property management':(r'property management|propert|apartment|resident|leasing|tenant|hoa|community management|rental',r''),
'Facilities management':(r'facilit|janitorial|maintenance|building services|work order|cleaning|hvac|fire protection|inspection',r''),
'Mixed (SuperSearch)':(r'.',r''),
'Specialty construction':(r'construction|contractor|install|build|roofing|elevator|door|concrete|electrical|mechanical|glass|paint',r'scent|marketing|media'),
'Commercial cleaning / janitorial':(r'clean|janitorial|custodial|sanit|disinfect|maintenance',r''),
'Equipment rental / service':(r'rental|rent|equipment|lift|scaffold|crane|forklift|generator',r''),
'B2B distribution':(r'distribut|wholesale|supplier|supply|dealer|products',r''),
}
GENERIC="{n} likely has years of client, project and operational records sitting across its systems."
stats=collections.Counter()
for o in rows:
    d=dom(o['website']); s=sites.get(d); sn=short(o['company_name'])
    o.setdefault('site_title',''); o.setdefault('site_summary',''); o.setdefault('site_tech',''); o.setdefault('name_on_site',''); o.setdefault('site_fit',''); o.setdefault('site_fit_note','')
    if not s or not s.get('status') or s.get('status',999)>=400 or not (s.get('text') or s.get('description')):
        o['site_fit']='UNCLEAR'; o['site_fit_note']='site not reachable' if s else 'not crawled'; stats['unreachable']+=1; continue
    blob=' '.join([s.get('title',''),s.get('description',''),s.get('h1',''),s.get('text',''),s.get('about_text','')]).lower()
    o['site_title']=s.get('title',''); o['site_summary']=(s.get('description') or s.get('h1') or s.get('text','')[:300])[:300]; o['site_tech']=','.join(s.get('tech',[]))
    toks=[t for t in re.findall(r'[a-z0-9]+',sn.lower()) if len(t)>=3 and t not in STOP]
    hit=sum(1 for t in toks if t in blob)
    o['name_on_site']='YES' if toks and hit>=max(1,len(toks)//2) else ('NO' if toks else 'UNCLEAR')
    pos,neg=LEX.get(o['industry'],(r'.',r''))
    p=len(re.findall(pos,blob)) if pos else 0; n=len(re.findall(neg,blob)) if neg else 0
    if o['industry'].startswith('Mixed'): fit='OK'
    elif p>=3 and n<=p//3: fit='OK'
    elif p==0 or (n>=2 and n>p): fit='WRONG'
    else: fit='UNCLEAR'
    o['site_fit']=fit; o['site_fit_note']=f'bucket words {p}, contradicting words {n}'
    if fit=='WRONG' or o['name_on_site']=='NO':
        if 'client, project and operational records' not in o['personalized_line']:
            o.setdefault('personalized_line_original',o['personalized_line'])
            o['personalized_line']=GENERIC.format(n=sn); o['line_changed']='YES'
            o['change_reason']=(o.get('change_reason','')+' | ' if o.get('change_reason') else '')+('site check: line did not fit the site; made generic' if fit=='WRONG' else 'site check: company name not found on site; made generic')
        o['needs_review']='YES'
    elif fit=='OK' and o['name_on_site']=='YES':
        if o.get('needs_review')=='YES': o['needs_review']='checked'
    stats[fit]+=1
cols=list(rows[0].keys())
for c in ['site_title','site_summary','site_tech','name_on_site','site_fit','site_fit_note']:
    if c not in cols: cols.append(c)
with open(OUT,'w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=cols); w.writeheader(); w.writerows(rows)
print(dict(stats))
