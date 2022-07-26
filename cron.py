from lib.api import fetch_commissions, fetch_events_for_commission_abbr
from lib.calender import generate_calendar_from_events
from lib.tools import generate_safe_filename
from lib.githubpages import generate_github_page_from_commissions
import logging


# Fetch commissions and write to csv
commissions = fetch_commissions()
commissions.sort_values('NaamNL').to_csv('data/commissies.csv', index=False)


# We cannot simply fetch all events, as calenders of commissions without events will not be updated 
for index, commission in commissions.iterrows():
    events = fetch_events_for_commission_abbr(commission['Afkorting'])
    calendar = generate_calendar_from_events(events)

    # Remove unsafe characters for filenames
    safe_file_name = generate_safe_filename(commission['Afkorting'])
    open(f"calenders/{safe_file_name}.ics", 'w').writelines(calendar)

# Generate new github pages
generate_github_page_from_commissions(commissions)

print("Done with CronJob")
