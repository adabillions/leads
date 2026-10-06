# Personalized line audit: AI_Data_Leads_INSTANTLY_verified.csv

Date: 2026-10-06. File checked: 16,900 leads, one per company.

## Bottom line

The personalized lines are not safe to send as they stand. In a stratified sample of 80 companies checked against public sources, 21 lines were factually wrong, 32 had a shaky or awkward detail, 10 could not be verified at all, and only 17 were fully right. The main causes are systemic, not random, so the same error rates should be expected across the whole file.

| Verdict | Count | Share of sample |
|---|---|---|
| OK (accurate and sensible) | 17 | 21% |
| MINOR (sensible, one detail shaky or awkward) | 32 | 40% |
| WRONG (false claim or wrong business type) | 21 | 26% |
| UNVERIFIED (no public footprint found) | 10 | 12% |

Company websites are blocked by this environment's network policy, so verification used web search results and third-party profiles (state registries, SAM, Crunchbase, CB Insights, ZoomInfo, LinkedIn snippets, news). Blitz was not used because only 116 records remain on the account.

## Systemic problems found (whole file)

1. **The industry label is the search bucket, not the company's real industry.** Lines are templated per bucket ("course content, assessments and learner feedback" for everything in the Education bucket, "tickets, escalations and remediation notes" for everything in Managed IT). When a company landed in the wrong bucket the line describes data it does not have. Examples: a buckle importer told it has "28 years in staffing and recruiting", a scent-marketing firm called a "specialty contracting business", a phone-pouch maker told it holds "patrol logs", an environmental-consulting firm with 700 staff treated as a disaster-restoration contractor, a computer store addressed as an accounting firm. Keyword screening flags 1,203 rows whose company name conflicts with its bucket; the real number is higher because many mismatches have neutral names.

2. **"N years in business" comes from a registration date, not the founding date.** Of about 45 year claims that could be checked, 9 were wrong by more than a year: LC Staffing (since 1985, CSV says 2006), Gyrus Systems (1987 vs 2009), MAG Carriers (2002 vs 2015), Concepts NREC (1980 vs 2015), OnSystem Logic (2015 vs 2008), Developing Capacity (2017 vs 2020), Air Esscentials (2005 vs 2007), Truckload LLC (2019-20 vs 2017), Chicago Messenger (1964 vs 1963). Roughly one in five year claims is off. 8,388 lines carry a year claim.

3. **Tool claims ("with HubSpot in the stack") are unverifiable and sometimes wrong.** 3,940 lines name a tool. None could be confirmed from public sources. One was contradicted outright: Applied AI Institute is told it runs Absorb when its courses are on Teachable. Several others are odd: Seedx is a Salesforce consultancy, so "with Salesforce in the stack" reads as if they are a customer. Jira is claimed at 127 non-software companies. Treat these as a risk unless you trust the technographic source.

4. **Legal entity names instead of trading names.** 2,618 rows have a company name that does not appear in the website domain, which usually means the line addresses a holding entity the recipient will not recognise: "Sho Place" (Anytime Restoration), "Manan" (Gyrus Systems), "Kebros & Associates" (SmartCare), "Clayco" (Skyline Elevators), "Medsearch Financial" (Alura Workforce Solutions), "Uresti Enterprises" (Rainbow Restoration of Killeen), "Warren Davis Properties Xii".

5. **Mechanical text defects.** 500 lines have title-cased acronyms ("Vip It", "Tuxera Us", "Erp Seminars", "Cpa"); 3 have a mangled name from an article bug ("A&An Inomatic", "D&An Enterprises", "P&An International"); 2,881 use the awkward "N years of help desk / payroll / implementations / courses" construction; 42 claim "help desk" at non-IT firms and 296 claim "implementations" at non-software firms (for example a security guard company "with 12 years of help desk"); 26 lines echo a scraped website counter ("HubSpot supporting 36 projects"); 412 mix "your" with the company name in the third person.

6. **Audience problems that matter for this pitch.** 133 Education-bucket rows are K-12 schools, charter schools or churches (Detroit Catholic Central High School, Archbishop Bergan Catholic School, Choice Charter School). Asking them to license "course content, assessments and learner feedback" means student data, which is a legal and reputational problem; recommend excluding them. 7,928 titles are "Owner / registered contact", meaning the person's actual role is unknown (one "CEO of Supreme Basketball" is attached to a Christian school). 363 "Mixed (SuperSearch)" rows have a fully generic line. 29 emails appear twice.

## What was changed in the corrected sheet

`data/exports/AI_Data_Leads_INSTANTLY_verified_CORRECTED.csv` keeps every original column (so it imports into Instantly unchanged) and adds: `line_changed`, `change_reason`, `personalized_line_original`, `industry_corrected`, `flags`, `needs_review`, `sample_verdict`, `sample_actual_business`.

| Change | Rows |
|---|---|
| Rewritten from verified facts (the 80-company sample, non-OK rows) | 62 |
| Made generic because the company name conflicts with its bucket (verify before sending) | 1,179 |
| Made generic because it is a K-12 school or church (recommend excluding) | 133 |
| Reworded "N years of help desk / payroll / courses" constructions | 1,644 |
| Removed help-desk or implementation framing at non-IT companies | 303 |
| Acronym casing and legal-suffix cleanup in the name | about 415 |
| Removed scraped site counters, "on record" repetition, surname-first names | about 350 |
| Total lines changed | 3,765 |
| Rows still marked `needs_review` | 6,282 |

Generic replacement line: "<Company> likely has years of client, project and operational records sitting across its systems." It makes no claim that can be wrong, at the cost of personalization.

Not changed: tool claims (no way to verify them at scale from here), year claims on rows outside the sample (about one in five is wrong, see above), and the 10,000+ rows with no flag, which are consistent internally but were not checked against the real company.

`data/exports/AI_Data_Leads_INSTANTLY_verified_FLAGGED.csv` is the original file with only the flag columns added, for anyone who prefers to review rather than accept the rewrites. Both files are git-ignored like the other lead data.

## Verifying all 16,900 companies

Checking every company the way the 80 were checked (two to three web searches each) would need well over 100 million tokens and many hours, and is not possible in this session. The realistic route to full coverage is:

1. Allow company websites in this environment's network settings (cloud environment menu in the session title bar, then Edit, then Network access: a broader level, or Custom with the lead domains allowed). Steps: https://code.claude.com/docs/en/cloud-environments#network-access
2. Then a crawler can fetch all 16,900 homepages in a few hours, extract what each company does, its "since YYYY" claim and any tool fingerprints (HubSpot, Zendesk, Intercom scripts), and score each line against its own site automatically.
3. A cheaper partial option without network changes: fix the bucket problem at the source by re-classifying industry per company from SuperSearch's own industry field rather than from the search that found it, and drop year claims that come from registration dates.

## Sample results (80 companies)

| Row | Company | Bucket in CSV | What it actually does | Verdict | Finding |
|---|---|---|---|---|---|
| 1933 | Groundwater And Environmental Services, Inc | Restoration | Environmental consulting/remediation, 700+ staff, founded 1985 | WRONG | Not restoration/disaster recovery; claims documentation wrong; year right. |
| 3536 | Manan, Llc (gyrus.com) | B2B SaaS | Gyrus Systems, LMS vendor founded 1987 | WRONG | Line calls them "Manan" (holding entity) not Gyrus; 2009 is CEO takeover, not founding. |
| 3713 | Yondr, Inc. | Private security | Lockable phone pouches for schools/events | WRONG | Not private security; patrol logs don't apply. 2014 correct. |
| 4217 | Mag Transportation Llc | Freight brokerage | Likely MAG Carriers, asset-based trucking, founded 2002 | WRONG | Carrier not broker; year 2015 vs 2002. |
| 4563 | Applied Ai Institute Llc | Education & training | AI courses (hosted on Teachable) | WRONG | "With Absorb in the stack" contradicted; courses run on Teachable. |
| 5714 | Alternative Staffing Corporation (LC Staffing) | Staffing | Montana staffing agency "since 1985" | WRONG | "20 years in" understates a 40-year firm; name should be LC Staffing. |
| 5742 | Warren Davis Properties Xii, L.L.C. | Property management | Commercial/industrial landlord-developer | WRONG | "Resident records" wrong for industrial tenants; "Xii" entity name awkward. |
| 8319 | Microsensys Us Inc | B2B SaaS | RFID hardware (US arm of German microsensys GmbH) | WRONG | Hardware maker, not software; SaaS data types don't fit. |
| 10175 | Air Esscentials Inc. | Specialty construction | Scent-marketing company | WRONG | Not a specialty contractor; founded ~2005 not 2007. |
| 10570 | Advanta Health Solutions, Inc. | Managed IT | Health-tech wellness-incentive platform (ActiveFit+) | WRONG | Not an MSP; "tickets, escalations and remediation notes" don't fit. 2010 founding correct. |
| 10798 | Aero Creek, Llc (AeroCreek) | Private security | Electronic security systems + IT integrator | WRONG | Not a guard/patrol firm; "patrol logs" wrong; "12 years of help desk" clumsy. |
| 11206 | A&A Inomatic Llc | B2B SaaS | Unknown | WRONG | Name mangled to "A&An Inomatic". |
| 11428 | Developing Capacity Consulting Llc | Education & training | Leadership/equity coaching firm | WRONG | Founding 2017 per ZoomInfo vs CSV 2020; "implementations/course content" misdescribes coaching practice. |
| 11707 | Standard Technology, Inc. | B2B SaaS | DoD/VA medical-coding & HIM services contractor | WRONG | Not software; "41 years of help desk" invented. 1985 founding correct. |
| 12672 | Buckles International, Inc. | Staffing | Importer of buckles and metal fasteners | WRONG | Nothing to do with staffing. |
| 12705 | Agdna Llc (Alpha Group DNA) | Facilities management | Talent placement / procurement firm | WRONG | Not facilities management; work orders don't fit. |
| 14011 | Truckload Llc (dba Expedite Express) | Freight brokerage | 1-4 truck motor carrier | WRONG | A carrier, not a broker; 2017 doubtful (USDOT number suggests 2019-2020). |
| 14392 | Ftl Investments Llc (compcorner.com) | Accounting | Computer Corner, Albuquerque computer dealer/service shop | WRONG | Not an accounting firm; "6 years in accounting" false. |
| 14459 | Kebros & Associates Llc (smartcarehh.com) | Staffing | Home health care agency (SmartCare) | WRONG | Not staffing; "submissions, interviews, placements" wrong; 2009 correct; name should be SmartCare. |
| 15388 | Flourish Llc | Education & training | Couples/relationship coaching | WRONG | Coaching practice, not education/training; 2016 unverified. |
| 16413 | Constant Communicators Llc | Education & training | PR/communications consultancy | WRONG | PR consulting, not education/training; data type does not fit. Year 2018 matches. |
| 5107 | Global Asset Development Group Llc | Managed IT | Unknown; name suggests real estate | UNVERIFIED | No evidence it is an MSP. |
| 7217 | Indigochart Llc | Managed IT | Unknown | UNVERIFIED | No public footprint; "Running managed IT out of Austin" unsupported. |
| 8487 | Schafer Contracting Services Llc (Lakeside Improvements) | Equipment rental | Small contractor, unclear | UNVERIFIED | No evidence of equipment rental or 24/7; brand name is Lakeside Improvements. |
| 9622 | Lams Technology Llc | Managed IT | Unknown (only a lookalike LAM Technology in TX found) | UNVERIFIED | No record of the Arlington entity; "17 years of help desk" awkward. |
| 10793 | Cloudseac Llc | B2B SaaS | Unknown | UNVERIFIED | No web presence found. |
| 10970 | Jayfini Global Investments Llc | Property management | Unknown | UNVERIFIED | No web footprint. |
| 12872 | Desert Saber Llc | B2B SaaS | Unknown | UNVERIFIED | No web presence found. |
| 13142 | Meridian Data Pro Llc | B2B SaaS | Unknown | UNVERIFIED | No evidence found. |
| 14097 | Ban Consulting Solutions, Llc. | Managed IT | Unknown | UNVERIFIED | Cannot confirm MSP or founding. |
| 14867 | Rising Stars Llc | Education & training | Probably after-school programs | UNVERIFIED | Could not confirm the Gilbert AZ entity or its age. |
| 24 | Edwards Business Systems | Managed IT | Copier/print dealer with MSP arm, founded 1954 | MINOR | Year confirmed; ConnectWise, client portal, 24/7 all unverified; CSV headcount 72 wrong (131-185+). |
| 981 | Thesis America, Inc. | B2B SaaS | Higher-ed SIS vendor (Thesis, ex-Unit4) | MINOR | Fits; HubSpot unverified; 1987/Cleves OH data unconfirmed (brand is 2021 spin-off, MO HQ). |
| 998 | Vector Global Logistics Llc | Freight brokerage | Atlanta freight forwarder, founded 2012/13 | MINOR | Fits; "HubSpot supporting 36 projects" is a scraped counter and reads oddly. |
| 1366 | Kalleo Technologies, Llc | Managed IT | Paducah KY MSP, founded 2004 | MINOR | Fits; whole hook rests on unverified ConnectWise. |
| 1949 | Sho Place, Inc. (Anytime Restoration) | Restoration | Water/fire restoration contractor | MINOR | Fits; addressed as holding-entity "Sho Place"; 2003 unverified, one source says 2013. |
| 2088 | Renzulli Learning, Llc | Education & training | K-12 gifted-ed online platform | MINOR | Fits; "9 years" right for LLC (2017) but brand is ~20 yrs old; HubSpot unverified. |
| 2134 | Caliber Living | Property management | Student-housing property manager, founded 2016 | MINOR | Year right; Zendesk unverified; brand likely absorbed by Peak Campus. |
| 2523 | Chicago Messenger Service | Freight brokerage | Same-day courier, founded 1964 | MINOR | CSV says 1963 (off by one); "carrier decisions" off for an asset-based courier. |
| 3248 | Wildflower International, Ltd. | Managed IT | Federal IT VAR/integrator, founded 1991 | MINOR | Year within 1 yr; help-desk data type weak fit for a reseller; Salesforce unverified. |
| 4018 | Vip It Inc. | Managed IT | LA MSP, founded 2015 | MINOR | Fits; ConnectWise unverified; "Vip It" should be VIP IT. |
| 4304 | Medsearch Financial Inc (Alura Workforce Solutions) | Staffing | Staffing agency | MINOR | Fits; name should be Alura Workforce Solutions; JobDiva/Salesforce unverified. |
| 5388 | Dunlapslk | Accounting | DunlapSLK CPA firm, 60+ staff, 25+ yrs | MINOR | Accurate, QuickBooks consulting confirmed; casing should be DunlapSLK. |
| 6258 | Livingworks Education Usa Inc | Education & training | Suicide-prevention training provider | MINOR | Fits; Jira unverified; US-entity 2004 unverified; "Usa" casing awkward. |
| 6516 | Swat Logistics Inc | Freight brokerage | 15-truck motor carrier | MINOR | Carrier not broker ("carrier decisions" soft mismatch); year plausible. |
| 7065 | Tipping Point Media Group Llc | Education & training | eLearning/immersive training agency | MINOR | Fits; HubSpot unverified; 2003 founding matches. |
| 7172 | Clayco, Inc. (DBA Skyline Elevators) | Specialty construction | Elevator contractor | MINOR | Recipient knows "Skyline Elevators"; "years of inspections" leading to RFIs is a non sequitur; year 1998 vs brochure 1994. |
| 7457 | Allied Garage Door, Inc | Specialty construction | Garage door install/repair | MINOR | "35+ years" consistent; RFIs/change orders slightly off-register. |
| 7607 | Peterson Daniel E Cpa | Accounting | Solo CPA practice | MINOR | Name is surname-first directory format; 2006 unverified. |
| 7625 | Actvisory Llc | Accounting | Accounting/tax/advisory firm, est. 2020 | MINOR | Facts right; "6 years of payroll" clumsy and narrow. |
| 7802 | Csw Superior It Solutions, Inc. | Managed IT | CSW Systems, managed IT for DoD/IC; acquired by Summit 7 in 2023 | MINOR | Fits; name rendering wrong (goes by CSW Systems); year unverified; now a subsidiary. |
| 8043 | Language Fundamentals Llc | Education & training | Language school (now International School of Languages) | MINOR | Fits; legacy name used; year within 1 yr (2006 vs 2007). |
| 8275 | Machine-To-Machine Intelligence M2Mi Corp | B2B SaaS | IoT platform (founded 2006) | MINOR | Fits; Zoho unverified; name rendering clunky. |
| 9744 | Coastal Contracting Llc | Specialised field service | Network cabling installer | MINOR | "Inspection and repair" generic; year unverified. |
| 10244 | Uresti Enterprises (Rainbow Restoration of Killeen) | Restoration | Restoration franchise | MINOR | Fits; legal-entity name instead of brand; 2014 unverified. |
| 10554 | Alphatub Corp | Education & training | Early-childhood literacy app | MINOR | Edtech fits broadly; "courses and curriculum"/"certification" overstate an app. Year within 1 yr. |
| 10709 | Onsystem Logic, Llc | B2B SaaS | Cybersecurity startup, $350K stage | MINOR | CB Insights says founded 2015 and Catonsville, vs CSV 2008 / Ellicott City; tiny startup unlikely to have "years of" data. |
| 10991 | Jk Guardian Security Services, Inc. | Private security | Chicagoland security-guard firm | MINOR | Accurate; name rendering "Jk Guardian" awkward. |
| 11023 | Vip Special Services Llc | Commercial cleaning | Commercial cleaning | MINOR | "Vip" should be VIP; 2005 unverified. |
| 12200 | Eco-Worx Inc | Specialised field service | Energy-efficiency retrofit contractor | MINOR | "Repair records" a stretch; 2007 loosely supported. |
| 15882 | Boujie Budgets Llc | Education & training | Personal-finance education brand (solo creator) | MINOR | Fits; "assessments ... systems" heavy for a one-person workshop brand. |
| 16554 | Seedx | Mixed | Salesforce/CRM consulting agency | MINOR | They sell/implement Salesforce; line treats them as an end-user. "operational records on record" redundant. |
| 16601 | Moov Technologies | Mixed | Used semiconductor-equipment marketplace | MINOR | No false claim; HubSpot unverified; generic. |
| 251 | Chmura Economics & Analytics, Llc | B2B SaaS | Labor-market analytics / JobsEQ SaaS | OK | 1998 confirmed; fits. |
| 894 | Dallas Courier Service | Freight brokerage | DFW same-day courier, 40+ years, 24/7 | OK | Consistent; 1982 inferred from "40+ years". |
| 1106 | Advanced Office Systems | B2B distribution | Copier/office tech dealer | OK | Since 1981 confirmed; 50 people in range. |
| 1400 | Life Safety Services Llc | Facilities management | Fire/life-safety inspection contractor, founded 2004 | OK | Year and "inspections" hook accurate. |
| 2530 | M7 Wine Solutions | Freight brokerage | Napa wine fulfillment 3PL, founded 2018 | OK | Year matches; fits fulfillment. |
| 2642 | Igx Solutions Corp | B2B SaaS | Grants-management software + IT consulting | OK | Fits; HubSpot unverified. |
| 2950 | Moxe Health Corporation | B2B SaaS | Clinical data exchange platform | OK | 2012 confirmed; fits; Salesforce unverified. |
| 3028 | Wistia | B2B SaaS | Video-hosting SaaS | OK | Fits; HubSpot unverified (support runs on Zendesk). |
| 3209 | Tina T. Chiang Accountancy Corp | Accounting | CPA firm, est. 1997 | OK | Facts match; line generic. |
| 4066 | Professional Development Training Center Llc | Education & training | Training/curriculum consulting | OK | 2012 registration matches; fits. |
| 5570 | Slope School | Education & training | Private PreK-8 school, Utah | OK | Founded 2019 verified; data type fits. |
| 6675 | Alaska Boiler & Burner Llc | Specialised field service | Boiler/burner mechanical contractor, founded 2014 | OK | Everything checks out. |
| 8491 | Mac Climber, Inc. | Equipment rental | Equipment rental (MAC Climber Rental) | OK | 2005 confirmed; fits. |
| 11591 | Speech Potential Associates Llc | Education & training | Accent/communication training | OK | 1993 founding verified; assessments and training confirmed. |
| 13043 | Metro Contracting Services Llc | Commercial cleaning | Janitorial contractor | OK | 2008 matches SAM; fits. |
| 14455 | Predica Inc | Staffing | IT staffing/recruiting | OK | Generic and accurate. |
| 16856 | Hit Subscribe | Mixed | Content-marketing agency | OK | Generic but accurate. |

