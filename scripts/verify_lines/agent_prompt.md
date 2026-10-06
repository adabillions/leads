You are checking cold-email personalization lines against reality for a batch of companies. For each company you get its ROW id, NAME (as written in our sheet), DOMAIN (its website), LOCATION, BUCKET (the industry group our template assumed) and LINE (the first line of the email, which assumes the company holds a certain kind of data, e.g. "course content, assessments and learner feedback" for trainers, "tickets, escalations and remediation notes" for IT service firms, "quotes, carrier decisions and shipment exceptions" for freight brokers, "submissions, interviews and placement outcomes" for staffing agencies, "support tickets, implementations and product-usage data" for software vendors).

The company's own website is BLOCKED in this environment. Do not try to fetch it. Use the WebSearch tool, mode "standard", ONE search per company, query like: "<NAME>" <DOMAIN> (if NAME is a bare person name or holding entity, search the DOMAIN alone). Do a second search only if the first returns nothing usable. Never spend more than two searches on one company. Do not use WebFetch.

For each company decide:
1. what_it_does: 4 to 10 words describing the real business ("unknown" if nothing found).
2. name_website_match: YES if the NAME (or an obvious short form of it) and the DOMAIN are the same business; DBA if the domain belongs to the business but it trades under a different name (give that name in trading_name); NO if the domain appears to belong to a different business; UNCLEAR if you could not tell.
3. line_fit: OK if the kind of data the LINE describes is what this business would actually hold; WRONG if the business clearly does not do that kind of work (e.g. a buckle importer told it has placement outcomes; a phone-pouch maker told it has patrol logs; a scent-marketing firm called a specialty contractor; a K-12 school or church when the line implies a training business); UNCLEAR if you could not determine what the company does. Ignore any year claims; years are not being checked. Ignore tool names (HubSpot, Salesforce, etc.); they are not being checked.
4. trading_name: the name the recipient would recognise, if different from NAME, else blank.
5. note: at most 12 words on what is wrong, else blank.

Write results as CSV to the file path given below using the Write tool (create the file with a header row, then one row per company; quote fields containing commas). Columns exactly: row,what_it_does,name_website_match,line_fit,trading_name,note

When done, reply with only two lines: the number of companies written, and counts of line_fit OK/WRONG/UNCLEAR. Do not include the table in your reply.
