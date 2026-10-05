# Lead Engine

Finds, enriches and verifies leads for the AI data licensing pitch: getting companies to license their
structured data to proprietary AI firms.

## Who we target

- US companies with 20 to 250 staff, roughly 1 to 5+ years in business
- They run on tools that hold structured data: Slack, HubSpot, Salesforce, Jira, Zendesk and other CRMs
- Mostly software companies, plus a mix of other industries
- Goal: 10,000+ contacts with verified emails

## Who we email at each company

1. **Owner, founder or CEO**: the main lead.
2. **Two colleagues**: named in the email ("Sandra or Jamie"). Ops, tech and data leaders come first;
   sales and HR come last.
3. **Data and IT leaders** (CTO, CIO, IT director, data or BI lead): their own lead list, with the CEO's
   name so the email can mention them.

## Pipeline

| Step | What it does | Sources |
| --- | --- | --- |
| Source | Find companies and people | Instantly SuperSearch (free previews), company websites, SBA small business database, Clearbit (free domain lookup) |
| Enrich | Find work emails | Blitz (only charged when it finds an email), GetLeads, Exa, emails built from the company's email format |
| Verify | Check each email will deliver | Instantly verifier (0.25 credits each), MillionVerifier for bulk. Plain SMTP checks don't work from here because port 25 is blocked. |
| Domain check | Count emails on another domain of the same company as verified (arketa.co and arketa.com, apiiro.com and apiiro.ai, atomic.work and atomicwork.com). Truly different companies stay flagged. | |
| Rank | Pick the two best colleagues per company | |
| Export | Write the three CSVs below | |

## Output files (in `data/exports/`, not committed)

- `AI_Data_Leads_INSTANTLY_verified.csv`: owners and CEOs with verified emails, plus colleague names and a data contact
- `AI_Data_Leads_DATA_PEOPLE_verified.csv`: data and IT leaders with verified emails, plus the CEO's name
- `AI_Data_Leads_MASTER.csv`: every company with all its people, emails, email status, tools, hooks and scores

## Layout

```
scripts/                  pipeline scripts (merge_instantly_preview.py and the rest)
data/imports/instantly/   raw Instantly preview pulls
data/exports/             finished CSVs
.env                      API keys (copy from .env.example)
```

Lead data and API keys are git-ignored on purpose. The CSVs have real people's names and emails, so
keep them in a private store such as Google Drive, not in git.

## Where things stand

- 698 companies worked so far
- 650 verified owners and CEOs, 176 verified data and IT leaders
- 51 emails built from company formats are waiting to be verified
- Credits left: Blitz 482, Instantly verifier 49.75 (about 199 checks)

## Getting to 10,000+

1. Pull SuperSearch names (free): about 37,000 matches. 6,518 software owners and CEOs, 18,708 in other
   industries, 11,892 data and engineering leaders.
2. Find emails: Blitz first, then emails built from company formats.
3. Verify in bulk: MillionVerifier (about $37 for this volume) or more Instantly credits.
4. Add SBA database owners (reachable, lists owners' own emails). US Department of Transportation freight
   data needs a US VPN.
5. Load the verified files into an Instantly list once approved.
