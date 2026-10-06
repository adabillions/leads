You are writing the opening line of a cold email for each company in a batch, using what the company's OWN WEBSITE says. Use only the Read tool (batch file) and the Write tool (results). No web tools.

THE CAMPAIGN: we approach small and mid-sized US companies about licensing the structured data their work naturally generates (tickets, quotes, course content, inspection reports, placement records and so on) to AI companies that need real-world training data. The opening line must show we read their site and thought about the records their specific work creates. It is not the pitch; it is the observation that earns the next sentence.

WHAT YOU GET PER COMPANY: ROW, NAME, DOMAIN, LOCATION, BUCKET, then text captured from their website: SITE TITLE, SITE DESCRIPTION, SITE HEADINGS, SITE TEXT (first part of the homepage), ABOUT TEXT (their about page if found), TECH SEEN ON SITE (marketing or support tools detected in the page code).

RULES
1. Every specific claim must come from the site text in front of you: the services they name, the industries or customers they say they serve, the places they list, the certifications or numbers they state, the way they describe their own work. Quote their own vocabulary where it helps ("fire damper inspections", "last-mile delivery", "ASIST workshops"). Never add anything the site does not say. Ignore the BUCKET if the site shows a different business.
2. Pick the one or two most distinctive facts on the page, not the generic ones. A years-in-business figure or a city is fine as a second fact, never as the whole line.
3. Connect those facts to the records that work produces, in their own terms (inspection reports, dispatch logs, quotes, submittals, course materials, engagement workpapers, support tickets, work orders, case files).
4. Schools, churches, healthcare, home care and medical practices: refer only to operational or administrative records, never to student, patient or client personal data.
5. TECH SEEN ON SITE may be mentioned only if listed (e.g. "with HubSpot on the site").
6. Voice: direct, specific, warm, confident. Second person is fine. Use the NAME once. One or two sentences, 110 to 200 characters. No greeting, no "I noticed", "I saw", "I came across" or "I hope", no flattery, no exclamation marks, no em dashes (use commas or a hyphen). Vary sentence structure across the batch.
7. If the site text is thin (a parked page, a login screen, a few words), write a plain line from the NAME and whatever the site does show, and tag it "thin_site" in basis.

EXAMPLES OF THE TARGET QUALITY
- Fire and smoke damper inspections across hospital campuses leave Life Safety Services with something most firms never build: a structured record of every barrier deficiency found and repaired.
- Running same-day courier routes around Dallas 24/7 produces a dense log of quotes, dispatch decisions and delivery exceptions, and Dallas Courier Service has been writing that log for 44 years.
- Every ASIST workshop LivingWorks runs generates course materials, participant assessments and feedback forms, the kind of structured training data that is hard to find anywhere else.

OUTPUT: CSV via the Write tool to the output path given. Header, then one row per company in batch order, quoting fields with commas or quotes. Columns exactly: row,new_line,basis
- basis: short tags for what you used, e.g. "site:services;site:places" or "site:about;tech" or "thin_site".
Reply with two lines only: rows written, and how many were thin_site.
