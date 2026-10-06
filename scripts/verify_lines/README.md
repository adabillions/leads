# verify_lines: check company name, website and personalized line for every lead

Pipeline used in the 2026-10-06 audit (see `data/exports/personalized_line_audit.md` on this branch).
Lead CSVs are never committed; put the Instantly export in `data/exports/` first.

## One-off setup already done in the audit
- `state/sample_verdicts.json`: 80 companies verified by hand against public sources.
- `state/websearch_results/`: web-search agent verdicts for the first 192 companies (rows with unsearched notes are ignored by the merge).

## Rebuild the corrected sheet (no network needed, a few seconds)
```
python3 scripts/verify_lines/flag_rows.py   data/exports/AI_Data_Leads_INSTANTLY_verified.csv data/exports/AI_Data_Leads_INSTANTLY_verified_FLAGGED.csv
python3 scripts/verify_lines/apply_fixes.py data/exports/AI_Data_Leads_INSTANTLY_verified.csv data/exports/AI_Data_Leads_INSTANTLY_verified_FLAGGED.csv data/exports/AI_Data_Leads_INSTANTLY_verified_CORRECTED.csv scripts/verify_lines/state/sample_verdicts.json
python3 scripts/verify_lines/merge_results.py data/exports/AI_Data_Leads_INSTANTLY_verified_CORRECTED.csv scripts/verify_lines/state/websearch_results
```

## Route A: crawl every company website (needs Network access to company domains)
```
python3 scripts/verify_lines/crawl_sites.py data/exports/AI_Data_Leads_INSTANTLY_verified_CORRECTED.csv data/exports/sites.jsonl 32
python3 scripts/verify_lines/score_lines.py data/exports/AI_Data_Leads_INSTANTLY_verified_CORRECTED.csv data/exports/sites.jsonl data/exports/AI_Data_Leads_INSTANTLY_verified_CHECKED.csv
```
About 16,800 domains at 32 workers takes roughly 1 to 2 hours. `crawl_sites.py` is resumable.
`score_lines.py` is rule-based; rows it marks UNCLEAR should get a model pass that reads `site_summary` and applies the same OK / WRONG / DBA rules as `agent_prompt.md`.

## Route B: web-search agents (needs CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION raised, e.g. 25000)
```
python3 scripts/verify_lines/make_batches.py data/exports/AI_Data_Leads_INSTANTLY_verified_CORRECTED.csv /tmp/batches 40
```
Launch agents (10 at a time, model sonnet) with: "Read scripts/verify_lines/agent_prompt.md and follow it. Batch file: /tmp/batches/batch_NNN.md. Write CSV to <results_dir>/batch_NNN.csv." Then rerun `merge_results.py` with that results directory. 420 batches at about 1 minute each per agent, 10 in parallel, is roughly 45 to 90 minutes.

## Output columns added to the sheet
`line_changed`, `change_reason`, `personalized_line_original`, `industry_corrected`, `flags`, `needs_review`, `sample_verdict`, `sample_actual_business`, `real_business`, `name_website_match`, `line_fit`, `trading_name`, `check_note`, and from the crawl `site_title`, `site_summary`, `site_tech`, `name_on_site`, `site_fit`, `site_fit_note`.
Original Instantly columns are untouched except `personalized_line`.

## Route C: brand-new opening lines written from each company's own site (needs Network access to company domains)
```
python3 scripts/verify_lines/crawl_sites.py data/exports/AI_Data_Leads_INSTANTLY_verified_CORRECTED.csv data/exports/sites.jsonl 32
python3 scripts/verify_lines/make_site_batches.py data/exports/AI_Data_Leads_INSTANTLY_verified_CORRECTED.csv data/exports/sites.jsonl /tmp/site_batches 100
```
Launch writer agents (model sonnet, 20 at a time) with: "Read scripts/verify_lines/writing_prompt_site.md and follow it. Batch file: /tmp/site_batches/batch_NNN.md. Output: <results_dir>/batch_NNN.csv." Companies listed in `/tmp/site_batches/unreachable.txt` fall back to `writing_prompt.md` (facts on file only). Then:
```
python3 scripts/verify_lines/apply_new_lines.py data/exports/AI_Data_Leads_INSTANTLY_verified_CORRECTED.csv <results_dir>
```
About 170 batches of 100; with 20 writers in parallel the writing takes roughly 40 to 60 minutes after the crawl (1 to 2 hours).

## Facts-only lines (what ran on 2026-10-06 while sites were blocked)
`writing_prompt.md` writes from the verified business description, the site signal scraped by the original pipeline, location and tools. `apply_new_lines.py` puts the result in `personalized_line`, keeps the previous line in `personalized_line_checked`, and records `line_basis` and `line_qc`.
