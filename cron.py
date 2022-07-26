from lib.api import fetch_active_commissions, fetch_events_for_commission_abbr
from lib.calender import generate_calendar_from_events
import re
import logging

# We cannot simply fetch all events, since empty commissions will not be updated
commissions = fetch_active_commissions()

for index, commission in commissions.iterrows():
    events = fetch_events_for_commission_abbr(commission['Afkorting'])
    calendar = generate_calendar_from_events(events)

    # Remove unsafe characters for filenames
    safe_file_name = re.sub(r"[ /]", "-", commission['Afkorting'])
    open(f"data/{safe_file_name}.ics", 'w').writelines(calendar)

logging.info("Done with CronJob")
