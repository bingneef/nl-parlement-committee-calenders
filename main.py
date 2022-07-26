from lib.api import fetch_committees, fetch_events_for_committee_abbr
from lib.calendar import generate_calendar_from_events
from lib.tools import generate_safe_filename
from lib.githubpages import generate_github_page_from_committees
import logging


# Fetch committees and write to csv
committees = fetch_committees()
committees.sort_values('NaamNL').to_csv('data/commissies.csv', index=False)


# We cannot simply fetch all events, as calendars of committees without events will not be updated 
for index, committee in committees.iterrows():
    events = fetch_events_for_committee_abbr(committee['Afkorting'])
    calendar = generate_calendar_from_events(events)

    # Remove unsafe characters for filenames
    safe_file_name = generate_safe_filename(committee['Afkorting'])
    open(f"calendars/{safe_file_name}.ics", 'w').writelines(calendar)

# Generate new github pages
generate_github_page_from_committees(committees)

print("Done with main.py")
