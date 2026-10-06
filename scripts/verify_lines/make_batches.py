"""Split rows that still lack a web-check verdict into 40-company batch files for search agents.
Usage: python3 make_batches.py <corrected.csv> <batches_dir> [batch_size]
Rows already carrying a line_fit value or a sample_verdict are skipped. Priority: flagged rows, then unflagged, then generic.
"""
import csv,re,sys,os
P,D=sys.argv[1],sys.argv[2]; B=int(sys.argv[3]) if len(sys.argv)>3 else 40
os.makedirs(D,exist_ok=True)
rows=list(csv.DictReader(open(P,newline='',encoding='utf-8')))
def dom(u): return re.sub(r'^https?://(www\.)?','',u.lower()).split('/')[0]
def prio(r):
    g='client, project and operational records' in r['personalized_line']
    return 0 if (r.get('needs_review')=='YES' and not g) else (1 if not g else 2)
todo=[r for r in rows if not r.get('line_fit') and not r.get('sample_verdict')]
todo.sort(key=lambda r:(prio(r),int(r['row'])))
for i in range(0,len(todo),B):
    with open(f'{D}/batch_{i//B+1:03d}.md','w') as f:
        for r in todo[i:i+B]:
            f.write(f"ROW {r['row']} | NAME: {r['company_name']} | DOMAIN: {dom(r['website'])} | LOCATION: {r['city']}, {r['state']} | BUCKET: {r['industry']}\n  LINE: {r['personalized_line']}\n")
print('batches',(len(todo)+B-1)//B,'companies',len(todo))
