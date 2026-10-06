"""Rule-based flags for every row of the lead export (no network needed).
Usage: python3 flag_rows.py <original.csv> <out_flagged.csv>
Adds columns: row, flags, flag_count, needs_review.
"""
import csv,re,sys,collections
SRC,OUT=sys.argv[1],sys.argv[2]
rows=list(csv.DictReader(open(SRC,newline='',encoding='utf-8-sig')))
STOP={'llc','inc','corp','company','group','services','solutions','international','enterprises','holdings','global','technologies','systems','associates','partners','consulting','management','logistics','staffing','properties','security','ltd','limited','incorporated','corporation','america','american','national','the'}
def dom(u): return re.sub(r'^https?://(www\.)?','',u.lower()).split('/')[0]
def toks(n): return [t for t in re.findall(r'[a-z0-9]+',n.lower()) if len(t)>=4 and t not in STOP]
INDFLAG={'Education & training (non-university)':r'\b(air|aviation|flight|media|marketing|realty|dental|law|plumbing|roofing|construction|logistics|trucking|communicat|consult|coaching|investments)\w*',
 'Managed IT / MSP':r'\b(dine|restaurant|cafe|grill|catering|realty|dental|law|plumbing|roofing|trucking|church|fair|staffing|health|asset|development)\w*',
 'Freight brokerage / 3PL':r'\b(wine|consulting|lodging|hotel|dental|law|realty|church|school|software|staffing|truckload|carriers|trucking|transport)\w*',
 'B2B SaaS / software':r'\b(consulting|consultants|cpa|accounting|law|realty|church|school|trucking|dental|staffing|resources|sensys|hardware|contractor)\w*',
 'Accounting / CPA firms':r'\b(investments|realty|construction|trucking|software|church)\w*',
 'Private security':r'\b(creek|aero|aviation|software|church|realty|pouch|yondr)\w*',
 'Property management':r'\b(investments|software|church|school|xii|iii|\bii\b|\biv\b|\bvi\b|\bvii\b)\w*',
 'Staffing / recruiting':r'\b(international|financial|health|home care|homecare|buckles)\w*',
 'Restoration / disaster recovery':r'\b(environmental|groundwater|engineering|consulting)\w*',
 'Facilities management':r'\b(dna|talent|staffing|consulting)\w*',
 'Specialty construction':r'\b(scent|aroma|esscentials|marketing|media)\w*'}
K12=r'\b(high school|elementary|middle school|academy|preparatory|prep|catholic|christian school|lutheran|montessori|charter|school district|preschool|day school|isd|public schools|church|ministries|diocese|ymca|\bY\b)\b'
ACR=r'\b(It|Cpa|Llc|Inc|Hr|Ai|Usa|Us|Pc|Pllc|Dba|Hvac|Ems|Rv|Nyc|Dc|Erp|Crm|Iot|Saas|Mri|Cnc|Llp|Ltd|Co|Corp|Xii|Iii|Ii|Iv)\b'
TOOLS=r'HubSpot|Salesforce|Jira|Zoho|Zendesk|ConnectWise|Autotask|QuickBooks|ServiceNow|NetSuite|Dynamics|Freshdesk|Kaseya|Absorb|Bullhorn|JobDiva|Canvas|Moodle|Intercom|Sage|Cornerstone|Yardi|Greenhouse|Teachable'
HARD={'name_mangled_article','industry_keyword_mismatch','k12_school_or_church','help_desk_outside_IT','surname_first_name','legal_name_not_in_domain','awkward_years_of_phrase','acronym_casing'}
def flags(r):
    f=[]; L=r['personalized_line']; cn=r['company_name']; ind=r['industry']
    if re.search(r'&An\b',L): f.append('name_mangled_article')
    if re.search(ACR,L): f.append('acronym_casing')
    d=dom(r['website']).split('.')[0].replace('-',''); t=toks(cn)
    if t and not any(x in d or d in x for x in t):
        ini=''.join(w[0] for w in re.findall(r'[a-z0-9]+',cn.lower()) if w not in {'llc','inc','corp'})
        if len(ini)<2 or ini not in d: f.append('legal_name_not_in_domain')
    if ind in INDFLAG and re.search(INDFLAG[ind],cn,re.I): f.append('industry_keyword_mismatch')
    if ind.startswith('Education') and re.search(K12,cn,re.I): f.append('k12_school_or_church')
    if re.search(r'\byour\b',L) and re.split(r'[,\s]',cn)[0].lower() in L.lower(): f.append('your_plus_company_name')
    if re.search(TOOLS,L): f.append('tool_claim_unverified')
    if re.search(r'years of (help desk|payroll|ticketing|implementations|assessments|courses|curriculum|certification programs|audits|inspections|patrols|dispatch|placements|a client portal|customer success|client onboarding)',L): f.append('awkward_years_of_phrase')
    if re.search(r'help desk',L,re.I) and not ind.startswith(('Managed IT','B2B SaaS')): f.append('help_desk_outside_IT')
    if re.search(r'implementation',L,re.I) and not ind.startswith(('Managed IT','B2B SaaS')): f.append('implementations_outside_software')
    if re.search(r'24/7',L) and ind.startswith(('Education','Accounting','Property','Staffing')): f.append('24x7_unlikely_for_industry')
    if ind.startswith('Mixed'): f.append('generic_mixed_bucket')
    if re.search(r'\bCpa\b',cn) and ',' not in cn and re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+ [A-Z]\b',cn): f.append('surname_first_name')
    if r['title'].startswith('Owner / registered'): f.append('title_is_registered_contact')
    if r['personalization'].startswith('runs') and re.search(r'runs (students|learners|24/7|technicians|load|carrier|capacity|offices in|courses|lessons|cohorts)',r['personalization']): f.append('garbled_personalization_field')
    if not r['personalization'].strip() and re.search(r'\d+ years',L): f.append('year_claim_without_personalization_source')
    return f
out=[];cnt=collections.Counter()
for i,r in enumerate(rows):
    f=flags(r); cnt.update(f)
    o=dict(r); o['row']=i+2; o['flags']=';'.join(f); o['flag_count']=len(f); o['needs_review']='YES' if any(x in HARD for x in f) else ''
    out.append(o)
cols=list(rows[0].keys())+['row','flags','flag_count','needs_review']
with open(OUT,'w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=cols); w.writeheader(); w.writerows(out)
for k,v in cnt.most_common(): print(f'{v:6d} {k}')
print('needs_review',sum(1 for o in out if o['needs_review']),'of',len(out))
