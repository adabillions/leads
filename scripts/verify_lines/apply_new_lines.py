"""Apply freshly written opening lines (CSV: row,new_line,basis) to the corrected sheet with quality checks.
Usage: python3 apply_new_lines.py <corrected.csv> <results_dir> [more_dirs...]
Moves the previous personalized_line to personalized_line_checked, writes the new line into personalized_line,
and records line_basis and line_qc (empty when the line passes every check).
"""
import csv,glob,re,sys,collections
P=sys.argv[1]; DIRS=sys.argv[2:]
rows=list(csv.DictReader(open(P,newline='',encoding='utf-8')))
TOOLS=r'HubSpot|Salesforce|Jira|Zoho|Zendesk|ConnectWise|Autotask|QuickBooks|ServiceNow|NetSuite|Dynamics|Freshdesk|Kaseya|Absorb|Bullhorn|JobDiva|Canvas|Moodle|Intercom|Sage|Cornerstone|Yardi|Greenhouse|Teachable|NinjaOne|Datto|Procore|Buildertrend|McLeod|Acumatica|Workday|Gusto|AppFolio|Buildium|Blackbaud|Paycom|Paylocity|Pipedrive|Asana|Slack'
SUFFIX=r'(,?\s*(L\.?L\.?C\.?|Inc\.?|Corp\.?|Corporation|Ltd\.?|L\.?P\.?|P\.?L\.?L\.?C\.?|P\.?C\.?|Co\.?|Company|Incorporated|Limited))+\s*$'
def short(cn): s=re.sub(SUFFIX,'',cn.strip(),flags=re.I).strip().rstrip(','); return s or cn
new={}
for f in sorted(sum([glob.glob(d+'/*.csv') for d in DIRS],[])):
    for r in csv.DictReader(open(f,newline='',encoding='utf-8')):
        if (r.get('row') or '').strip().isdigit() and (r.get('new_line') or '').strip():
            new[int(r['row'])]={'line':r['new_line'].strip().strip('"'),'basis':(r.get('basis') or '').strip()}
qc=collections.Counter(); applied=0
for o in rows:
    v=new.get(int(o['row']))
    if not v: continue
    L=v['line']; issues=[]
    name=o['trading_name'] if o.get('name_website_match')=='DBA' and o.get('trading_name') else short(o['company_name'])
    toks=[t for t in re.findall(r'[A-Za-z0-9]+',name) if len(t)>=3]
    if toks and not any(t.lower() in L.lower() for t in toks): issues.append('name_missing')
    if len(L)<90: issues.append('too_short')
    if len(L)>230: issues.append('too_long')
    if '—' in L or '–' in L: issues.append('dash')
    if '!' in L: issues.append('exclamation')
    if re.search(r'likely has years of|I noticed|I hope|I came across|sitting across its systems',L): issues.append('boilerplate')
    orig=o.get('personalized_line_original') or o.get('personalized_line_checked') or ''
    allowed=set(re.findall(TOOLS,orig)); used=set(re.findall(TOOLS,L))
    if used-allowed: issues.append('tool_not_in_source:'+','.join(sorted(used-allowed)))
    if o.get('flags') and 'k12_school_or_church' in o['flags'] and re.search(r'student|pupil|learner|grade',L,re.I): issues.append('sensitive_student_ref')
    if not o.get('personalized_line_checked'): o['personalized_line_checked']=o['personalized_line']
    o['personalized_line']=L; o['line_basis']=v['basis']; o['line_qc']=';'.join(issues)
    o['line_changed']='YES'; applied+=1
    for i in issues: qc[i.split(':')[0]]+=1
cols=list(rows[0].keys())
for c in ['personalized_line_checked','line_basis','line_qc']:
    if c not in cols: cols.append(c)
for o in rows:
    for c in cols: o.setdefault(c,'')
with open(P,'w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=cols); w.writeheader(); w.writerows(rows)
print(f'applied {applied} new lines; {sum(1 for o in rows if not o.get("line_basis"))} rows still without a new line')
print('qc issues:',dict(qc))
print('basis:',dict(collections.Counter(o['line_basis'] for o in rows if o.get('line_basis')).most_common(8)))
