from lib.api import fetch_committees, fetch_events_for_committee_abbr
from lib.calendar import generate_calendar_from_events
from lib.tools import generate_safe_filename
from lib.readme import generate_readme_from_committees

# Fetch committees and write to csv
committees = fetch_committees()
committees.to_csv('data/commissies.csv', index=False)


# We cannot simply fetch all events, as calendars of committees without
# events will not be updated
def write_calender_for_committee_and_return_committee(committee):
    events = fetch_events_for_committee_abbr(committee['Afkorting'])
    calendar = generate_calendar_from_events(events)

    # Remove unsafe characters for filenames
    safe_file_name = generate_safe_filename(committee['Afkorting'])
    open(f"calendars/{safe_file_name}.ics", 'w').writelines(calendar)

    committee['Activiteiten Aantal'] = len(calendar.events)

    return committee


committees = committees.apply(write_calender_for_committee_and_return_committee, axis=1)

# Generate new readme
generate_readme_from_committees(committees)

print("Done with main.py")
