"""Apply the manual rewrites (80 verified companies) and mechanical fixes to the lead export.
Usage: python3 apply_fixes.py <original.csv> <flagged.csv> <out_corrected.csv> state/sample_verdicts.json
"""
import csv,re,collections,json
import sys
SRC,FLAGGED,OUT,VERD=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
rows=list(csv.DictReader(open(SRC,newline='',encoding='utf-8-sig')))
verd=json.load(open(VERD))
flagged={int(r['row']):r for r in csv.DictReader(open(FLAGGED,newline='',encoding='utf-8'))}

MANUAL={  # row: (new line, corrected industry or '', note)
24:("Seventy-two years of selling and servicing office technology should leave Edwards Business Systems with a deep history of service tickets and remediation notes.","Office technology dealer / MSP","Dropped unverified ConnectWise, client portal and 24/7 claims; 1954 founding verified."),
981:("Between HubSpot and your SIS implementations, Thesis should have a deep record of support tickets, implementations and product-usage data.","","Trading name is Thesis; 1987 date unconfirmed so no year used."),
998:("With HubSpot in the stack and over a decade of freight forwarding, Vector Global Logistics likely has years of quotes, carrier decisions and shipment exceptions on record.","","Removed scraped '36 projects' counter."),
1366:("After 22 years in managed IT, with ConnectWise in the stack, Kalleo Technologies likely has a long record of tickets, escalations and remediation notes.","","2004 founding verified; ConnectWise unverified but not contradicted."),
1933:("Forty-one years and close to 30 offices of environmental consulting should leave GES with a deep record of site data, compliance reports and remediation records.","Environmental consulting / remediation","Not a restoration contractor; data types rewritten."),
1949:("Running 24/7 emergency restoration, Anytime Restoration likely has years of intake, damage-assessment and claims documentation on record.","","Used trading name; 2003 date unverified (one source says 2013) so year dropped."),
2088:("With HubSpot in the stack and the Renzulli Learning System in schools for close to two decades, Renzulli Learning likely holds a long record of course content, assessments and learner feedback.","","Brand is ~20 years old; LLC is 2017."),
2523:("Sixty-two years of same-day and final-mile delivery should mean a deep record of quotes, dispatch decisions and shipment exceptions.","Same-day courier","Founded 1964 not 1963; asset-based courier so 'carrier decisions' replaced."),
3248:("Thirty-five years as a federal IT integrator, with Salesforce in the stack, likely leaves Wildflower International with a long record of quotes, deployments and support tickets.","Federal IT VAR / integrator","Founded 1991; reseller rather than help-desk MSP."),
3536:("Running the GyrusAim LMS since 1987, with Zoho in the stack, Gyrus Systems should have a deep record of support tickets, implementations and product-usage data.","","Company trades as Gyrus Systems, founded 1987; 'Manan' is the holding entity."),
3713:("Twelve years of putting Yondr pouches into schools, courts and venues likely means a deep record of deployments, support requests and customer feedback.","Consumer hardware / edtech","Not private security."),
4018:("With ConnectWise in the stack, VIP IT likely has years of tickets, escalations and remediation notes on record.","","Casing fix."),
4217:("Running a fleet of 200-plus trucks since 2002, MAG Carriers likely has a deep record of loads, dispatch decisions and delivery exceptions.","Trucking carrier","Dearing GA entity is MAG Carriers (2002), a carrier not a broker. Entity match uncertain, confirm before sending."),
4304:("Between JobDiva and Salesforce, Alura Workforce Solutions is probably sitting on a deep record of submissions, interviews and placement outcomes.","","Trading name is Alura Workforce Solutions."),
4563:("Running AI courses with knowledge checks and capstone projects, Applied AI Institute likely has years of course content, assessments and learner feedback on record.","","Absorb claim contradicted (courses run on Teachable)."),
5107:("Global Asset Development Group likely has years of client, project and operational records sitting across its systems.","Unknown","No evidence it is an MSP; made generic."),
5388:("With QuickBooks in the stack, DunlapSLK likely has years of engagement, review and close-process records on file.","","Casing fix; QuickBooks consulting confirmed."),
5714:("Placing talent across Montana since 1985, with Bullhorn in the stack, LC Staffing likely holds a long record of submissions, interviews and placement outcomes.","","Trades as LC Staffing, since 1985 not 2006."),
5742:("Decades of developing and leasing office and industrial space should leave Davis Properties with a deep record of leasing, maintenance and tenant records.","Commercial real estate","Industrial landlord; 'resident records' and 'Xii' removed."),
6258:("Between Jira and your training programs, LivingWorks should have a deep record of course content, assessments and learner feedback.","","Name casing fix."),
6516:("Running its own trucks, Swat Logistics likely has years of quotes, dispatch decisions and shipment exceptions sitting across its systems.","Trucking carrier","Carrier not broker."),
7065:("Twenty-three years of building eLearning and immersive training, with HubSpot in the stack, should leave Tipping Point Media with a deep record of course content, assessments and learner feedback.","","2003 founding verified."),
7172:("Close to three decades of elevator installs and modernizations should leave Skyline Elevators with a substantial record of estimates, RFIs and change orders.","","Trades as Skyline Elevators; 'years of inspections' non sequitur removed."),
7217:("Indigochart likely has years of client, project and operational records sitting across its systems.","Unknown","No public footprint; made generic."),
7457:("More than 35 years of garage door installs and repairs should leave Allied Garage Door with a deep record of estimates, work orders and service history.","","1979 unconfirmed; '35+ years' is what sources say."),
7607:("Twenty years in practice should leave Daniel E. Peterson, CPA with a substantial history of engagement, review and close-process records.","","Name was surname-first; 2006 unverified."),
7625:("Six years of bookkeeping, tax and payroll work should leave Actvisory with a substantial history of engagement, review and close-process records.","","Est. 2020 verified; '6 years of payroll' reworded."),
7802:("Years of managed IT for classified DoD and IC work should leave CSW Systems with a deep record of tickets, escalations and remediation notes.","","Trades as CSW Systems; acquired by Summit 7 in Nov 2023; 2011 unverified."),
8043:("Twenty years of language courses and tutoring should leave the International School of Languages with a substantial record of course content, assessments and learner feedback.","","Trades as International School of Languages; operating since 2006."),
8275:("With Zoho in the stack and 20 years of running an IoT platform, M2Mi likely has years of support tickets, implementations and product-usage data on record.","","2006 founding verified; shorter name."),
8319:("Supplying RFID transponders, readers and data loggers, Microsensys US likely has years of orders, support requests and device data on record.","RFID hardware","Hardware maker, not software."),
8487:("Lakeside Improvements likely has years of estimates, job and service records sitting across its systems.","Unknown (contractor)","No evidence of equipment rental or 24/7; brand is Lakeside Improvements."),
9622:("Lams Technology likely has years of client, project and operational records sitting across its systems.","Unknown","No record of this Arlington entity found; made generic."),
9744:("Years of structured cabling and network installs should leave Coastal Contracting with a deep record of site surveys, job tickets and service history.","Low-voltage / network cabling","2014 unverified; data types fitted to cabling work."),
10175:("Twenty years of scent marketing for hotels, retail and venues should leave Air Esscentials with a deep record of installs, service visits and client records.","Scent marketing","Not a specialty contractor; founded ~2005."),
10244:("Running 24/7 emergency restoration, Rainbow Restoration of Killeen likely has years of intake, damage-assessment and claims documentation on record.","","Franchise brand name used; Uresti link unverified."),
10554:("Nine years of running the alphaTUB literacy app should leave alphaTUB with a substantial record of learning content, engagement analytics and parent feedback.","Edtech product","App, not courses/certification."),
10570:("Sixteen years of running the ActiveFit+ wellness platform should leave Advanta Health Solutions with a substantial record of implementations, member activity and support data.","Health-tech SaaS","Not an MSP; 2010 verified."),
10709:("Building endpoint-hardening software, OnSystem Logic likely has a growing record of support tickets, deployments and product-usage data.","","CB Insights says founded 2015 (CSV 2008) and Catonsville; year and location dropped."),
10793:("Cloudseac likely has years of client, project and operational records sitting across its systems.","Unknown","No web presence found; made generic."),
10798:("Installing alarms, cameras and access control alongside IT support, AeroCreek likely has years of install tickets, service calls and help-desk records.","Security systems integrator / MSP","Not a guard/patrol company."),
10970:("Jayfini Global Investments likely has years of client, project and operational records sitting across its systems.","Unknown","No web footprint; made generic."),
10991:("Decades of contract guarding mean Guardian Security Services likely holds a steady history of patrol logs, incident reports and dispatch records.","","Brand is Guardian Security Services."),
11023:("Twenty-one years in commercial cleaning should leave VIP Special Services with a deep record of inspections, QA checks and site-level work orders.","","Casing fix; 2005 unverified."),
11206:("As a software business, A&A Inomatic likely has years of support tickets, implementations and product-usage data sitting in its systems.","","Name was mangled to 'A&An'; business itself unverified."),
11428:("Years of leadership coaching and capacity-building work should leave Developing Capacity Coaching with a substantial record of assessments, session notes and client feedback.","Leadership coaching / consulting","Coaching firm; founding 2017 per ZoomInfo vs CSV 2020."),
11707:("Forty-one years of medical coding, auditing and documentation work for military health should leave Standard Technology with a deep record of coding audits, training records and compliance documentation.","Health information management services","Not software; 'help desk' invented; 1985 verified."),
12200:("Nineteen years of lighting retrofits and energy-efficiency projects should leave Eco-Worx with a deep history of audits, project files and rebate records.","Energy-efficiency contractor","2007 loosely supported."),
12672:("Decades of importing buckles and hardware should leave Buckles International with a deep record of orders, inventory and supplier records.","Hardware import / distribution","Not staffing."),
12705:("Years of talent placement and procurement work should leave Alpha Group DNA with a substantial record of submissions, placements and purchasing records.","Staffing / procurement services","Not facilities management; 2016 unverified."),
12872:("Desert Saber likely has years of client, project and operational records sitting across its systems.","Unknown","No web presence found; made generic."),
13142:("Meridian Data Pro likely has years of client, project and operational records sitting across its systems.","Unknown","No evidence found; made generic."),
14011:("Running its own trucks, Expedite Express likely has years of loads, dispatch decisions and delivery exceptions on record.","Trucking carrier","1-4 truck carrier dba Expedite Express; 2017 doubtful."),
14097:("Ban Consulting Solutions likely has years of client, project and operational records sitting across its systems.","Unknown","Cannot confirm MSP; made generic."),
14392:("Decades of selling and servicing computers in Albuquerque should leave Computer Corner with a deep record of sales, repair tickets and service history.","Computer sales / service","Domain is Computer Corner, not an accounting firm."),
14459:("Seventeen years of 24/7 home health care should leave SmartCare with a substantial record of care plans, visit notes and caregiver schedules.","Home health care","Not staffing; trades as SmartCare. Health data: consider excluding."),
14867:("Rising Stars likely has years of program content, enrollment and family feedback sitting across its systems.","","Entity unconfirmed; year dropped."),
15388:("Years of couples coaching and workshops should leave Flourish with a substantial record of session notes, workshop content and client feedback.","Coaching","Not education/training; 2016 unverified."),
15882:("Years of financial-literacy workshops and budgeting content should leave Boujie Budgets with a solid record of course content and participant feedback.","","Solo creator; toned down."),
16413:("Eight years of PR and communications consulting should leave Constant Communicators with a substantial record of client briefs, drafts and campaign records.","PR / communications consulting","Not education/training; 2018 verified."),
16554:("Implementing Salesforce and HubSpot for clients, Seedx likely has years of project, integration and client records on file.","CRM consulting agency","They implement Salesforce for clients rather than merely use it."),
16601:("Between HubSpot and 24/7 customer-service teams, Moov Technologies should have a deep history of listings, transactions and support records.","Equipment marketplace","24/7 teams confirmed; HubSpot unverified."),
}
SUFFIX=r'(,?\s*(L\.?L\.?C\.?|Inc\.?|Corp\.?|Corporation|Ltd\.?|L\.?P\.?|P\.?L\.?L\.?C\.?|P\.?C\.?|Co\.?|Company|Incorporated|Limited))+\s*$'
ACR={'It':'IT','Cpa':'CPA','Hr':'HR','Ai':'AI','Usa':'USA','Us':'US','Pc':'PC','Hvac':'HVAC','Ems':'EMS','Nyc':'NYC','Dc':'DC','Erp':'ERP','Crm':'CRM','Iot':'IoT','Saas':'SaaS','Mri':'MRI','Cnc':'CNC','Rv':'RV','Llc':'LLC','Inc':'Inc','Ltd':'Ltd','Dba':'DBA','Xii':'XII','Iii':'III','Ii':'II','Iv':'IV'}
def short(cn):
    s=re.sub(SUFFIX,'',cn.strip(),flags=re.I).strip().rstrip(',')
    return s or cn
def fixcase(s): return re.sub(r'\b('+'|'.join(ACR)+r')\b',lambda m:ACR[m.group(1)],s)
GENERIC="{n} likely has years of client, project and operational records sitting across its systems."
YEARSOF={'help desk':'help-desk work','payroll':'payroll and bookkeeping work','implementations':'implementation work','courses':'running courses','curriculum':'curriculum work','dispatch':'dispatch work','ticketing':'ticketing','customer success':'customer-success work','client onboarding':'client onboarding','a client portal':'running a client portal','assessments':'assessment work'}
out=[];stats=collections.Counter()
for i,r in enumerate(rows):
    row=i+2; L=r['personalized_line']; reasons=[]; ind_corr=''
    fl=flagged[row]['flags'].split(';') if flagged[row]['flags'] else []
    if row in MANUAL:
        L,ind_corr,note=MANUAL[row]; reasons.append('verified_rewrite: '+note); stats['manual']+=1
    else:
        orig=L
        sn=short(r['company_name']); disp=fixcase(sn)
        if 'name_mangled_article' in fl:
            L=L.replace('&An ','&A '); reasons.append('fixed mangled name')
        if 'k12_school_or_church' in fl:
            L=GENERIC.format(n=disp); reasons.append('K-12 school or church: made generic; recommend excluding (student data)')
        elif 'industry_keyword_mismatch' in fl:
            L=GENERIC.format(n=disp); reasons.append('industry label looks wrong for this company name: made generic, verify manually')
        else:
            # casing of acronyms inside the company name as it appears in the line
            if disp!=sn and sn.lower() in L.lower():
                L=re.sub(re.escape(sn),disp,L,flags=re.I); reasons.append('acronym casing in name')
            # awkward "years of X"
            def yo(m):
                return m.group(1)+' years of '+YEARSOF[m.group(2)]
            L2=re.sub(r'(\d+|[A-Z][a-z]+(?:-[a-z]+)?) years of ('+'|'.join(map(re.escape,YEARSOF))+r')\b(?=,| should| likely| probably| with| and| at| in)',yo,L)
            if L2!=L: reasons.append('reworded "years of ..."'); L=L2
            if not r['industry'].startswith(('Managed IT','B2B SaaS')):
                L2=re.sub(r'\bhelp[- ]desk work\b','operations',L); L2=re.sub(r'\bhelp desk\b','operations',L2)
                L2=re.sub(r'\bimplementation work\b','client work',L2); L2=re.sub(r'\bimplementations\b','client work',L2)
                if L2!=L: reasons.append('removed help-desk/implementation framing outside IT'); L=L2
            L2=re.sub(r'With (\w+) supporting ([\d,]+\+? \w+),',r'With \1 in the stack,',L)
            if L2!=L: reasons.append('removed scraped site counter'); L=L2
            L2=L.replace('records on record','records on file')
            if L2!=L: reasons.append('wording'); L=L2
            L2=re.sub(r'\b(\w+) (\w+) ([A-Z]) CPA\b',r'\2 \3. \1, CPA',L)
            if L2!=L: reasons.append('surname-first name fixed'); L=L2
        if L!=orig: stats['auto']+=1
    o=dict(r); o['personalized_line']=L
    o['row']=row; o['line_changed']='YES' if L!=r['personalized_line'] else ''
    o['change_reason']=' | '.join(reasons); o['personalized_line_original']=r['personalized_line']
    o['industry_corrected']=ind_corr; o['flags']=flagged[row]['flags']; o['needs_review']=flagged[row]['needs_review']
    v=verd.get(str(row)); o['sample_verdict']=v['verdict'] if v else ''; o['sample_actual_business']=v['actual'] if v else ''
    out.append(o)
cols=list(rows[0].keys())+['row','line_changed','change_reason','personalized_line_original','industry_corrected','flags','needs_review','sample_verdict','sample_actual_business']
with open(OUT,'w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=cols); w.writeheader(); w.writerows(out)
print(stats, 'changed total', sum(1 for o in out if o['line_changed']))
rc=collections.Counter(); 
for o in out:
    for x in o['change_reason'].split(' | '):
        if x: rc[x.split(':')[0]]+=1
[print(f'{v:6d} {k}') for k,v in rc.most_common()]
# sanity: show some auto-changed examples
import random; random.seed(3)
ch=[o for o in out if o['line_changed'] and not o['change_reason'].startswith('verified')]
for o in random.sample(ch,12): print('\n-',o['personalized_line_original'],'\n+',o['personalized_line'],'\n  ',o['change_reason'])
# leftover checks
print('\nleftover acronym casing:',sum(1 for o in out if re.search(r'\b(It|Usa|Cpa|Llc|Xii)\b',o['personalized_line'])))
print('leftover &An:',sum(1 for o in out if '&An' in o['personalized_line']))
print('leftover years of help desk:',sum(1 for o in out if re.search(r'years of help desk\b',o['personalized_line'])))
print('generic lines now:',sum(1 for o in out if 'client, project and operational records' in o['personalized_line']))
