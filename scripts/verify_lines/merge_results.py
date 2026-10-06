"""Merge web-search agent verdicts (CSV files: row,what_it_does,name_website_match,line_fit,trading_name,note) into the corrected sheet.
Usage: python3 merge_results.py <corrected.csv> <results_dir> [more_results_dirs...]
Result CSVs with a confidence column are treated as knowledge-pass verdicts; LOW confidence becomes UNCLEAR, a search verdict always wins.
"""
import csv,glob,re,collections,sys
P=sys.argv[1]; RESDIRS=sys.argv[2:]
rows=list(csv.DictReader(open(P,newline='',encoding='utf-8')))
res={}
bad=collections.Counter()
for f in sorted(sum([glob.glob(d+'/*.csv') for d in RESDIRS],[])):
    try:
        for r in csv.DictReader(open(f,newline='',encoding='utf-8')):
            if not r.get('row','').strip().isdigit(): bad['norow']+=1; continue
            note=(r.get('note') or '')
            if re.search(r'not searched|budget exhausted|not verified|unverified by search|judged from name|own knowledge|knowledge|guess|inference|from the name|from name',note,re.I): bad['skipped_unsearched']+=1; continue
            lf=(r.get('line_fit') or '').strip().upper(); nm=(r.get('name_website_match') or '').strip().upper()
            conf=(r.get('confidence') or '').strip().upper()
            src='knowledge' if 'confidence' in r else 'search'
            if lf not in {'OK','WRONG','UNCLEAR'}: lf='UNCLEAR'
            if nm not in {'YES','DBA','NO','UNCLEAR'}: nm='UNCLEAR'
            if src=='knowledge' and conf=='LOW': lf='UNCLEAR'; nm='UNCLEAR' if nm!='YES' else nm
            if src=='knowledge' and conf not in {'HIGH','MED'} and lf=='WRONG': lf='UNCLEAR'
            row=int(r['row'])
            if row in res and res[row]['src']=='search': continue  # a real search beats knowledge
            res[row]={'what':(r.get('what_it_does') or '').strip(),'nm':nm,'lf':lf,'tn':(r.get('trading_name') or '').strip(),'note':(r.get('note') or '').strip(),'batch':f,'src':src,'conf':conf}
    except Exception as e: bad['err:'+f]+=1
GENERIC="{n} likely has years of client, project and operational records sitting across its systems."
SUFFIX=r'(,?\s*(L\.?L\.?C\.?|Inc\.?|Corp\.?|Corporation|Ltd\.?|L\.?P\.?|P\.?L\.?L\.?C\.?|P\.?C\.?|Co\.?|Company|Incorporated|Limited))+\s*$'
def short(cn): s=re.sub(SUFFIX,'',cn.strip(),flags=re.I).strip().rstrip(','); return s or cn
for c in ['real_business','name_website_match','line_fit','trading_name','check_note']:
    pass
applied=collections.Counter()
for o in rows:
    row=int(o['row']); v=res.get(row)
    if not v: continue
    if o.get('check_source')=='search' and v['src']=='knowledge': continue
    o['real_business']=v['what']; o['name_website_match']=v['nm']; o['line_fit']=v['lf']; o['trading_name']=v['tn']; o['check_note']=v['note']
    o['check_source']=v['src']+(' '+v['conf'].lower() if v['conf'] else '')
    L=o['personalized_line']; sn=short(o['company_name']); name=v['tn'] if v['tn'] and v['nm']=='DBA' else None
    reasons=[]
    if v['lf']=='WRONG' or v['nm']=='NO':
        n=name or sn
        L=GENERIC.format(n=n); reasons.append('web check: line did not fit the real business (%s); made generic'%(v['what'] or 'unknown'))
        o['needs_review']='YES' if v['src']=='search' or v['conf']=='HIGH' else 'likely wrong'
    elif v['lf']=='OK':
        # restore a specific line if it had been made generic only on a name-keyword hunch
        if 'client, project and operational records' in L and 'industry label looks wrong' in o.get('change_reason',''):
            L=o['personalized_line_original']; reasons.append('web check: bucket confirmed, restored original line')
        if name and name.lower() not in L.lower() and sn.lower() in L.lower():
            L=re.sub(re.escape(sn),name,L,flags=re.I); reasons.append('web check: used trading name %s'%name)
        if o['needs_review']=='YES' and v['nm'] in {'YES','DBA'}: o['needs_review']='checked'
    else:
        if name and sn.lower() in L.lower(): L=re.sub(re.escape(sn),name,L,flags=re.I); reasons.append('web check: used trading name %s'%name)
        o['needs_review']='YES' if o['needs_review'] else 'unclear'
    if L!=o['personalized_line']:
        o['personalized_line']=L; o['line_changed']='YES'
        o['change_reason']=(o['change_reason']+' | ' if o['change_reason'] else '')+'; '.join(reasons)
    applied[v['lf']]+=1
cols=list(rows[0].keys())
for c in ['real_business','name_website_match','line_fit','trading_name','check_note','check_source']:
    if c not in cols: cols.append(c)
for o in rows:
    for c in cols: o.setdefault(c,'')
with open(P,'w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=cols); w.writeheader(); w.writerows(rows)
tot=len(rows); checked=sum(1 for o in rows if o.get('line_fit'))+80
lf=collections.Counter(o['line_fit'] for o in rows if o.get('line_fit')); nm=collections.Counter(o['name_website_match'] for o in rows if o.get('name_website_match'))
print('by source:',dict(collections.Counter(o.get('check_source','').split(' ')[0] for o in rows if o.get('line_fit'))))
print(f"merged results from {sum(len(glob.glob(d+'/*.csv')) for d in RESDIRS)} batch files: {len(res)} companies; bad rows {dict(bad)}")
print(f"progress: {checked}/{tot} companies checked ({checked/tot:.1%})")
print('line_fit:',dict(lf),' name_website_match:',dict(nm))
