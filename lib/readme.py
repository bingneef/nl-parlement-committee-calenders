from lib.tools import generate_safe_filename
from datetime import date
import numpy as np


def generate_readme_from_committees(committees):
    with open('templates/index.md') as f:
        template = f.read()

    calendars_with_events = np.array([])
    calendars_without_events = np.array([])
    for __, committee in committees.iterrows():
        calendar_url = (
            "https://raw.githubusercontent.com/bingneef/rekenkamer-commissie-scraper/main/calendars/" +
            f"{generate_safe_filename(committee['Afkorting'])}.ics")

        committee_rows = "\n".join([
            f"**{committee['NaamNL']}** ({committee['Activiteiten Aantal']} gevonden)\\",
            f"[{calendar_url}]({calendar_url})"
        ])

        if committee['Activiteiten Aantal'] == 0:
            calendars_without_events = np.append(calendars_without_events, committee_rows)
        else:
            calendars_with_events = np.append(calendars_with_events, committee_rows)

    calendars_with_events_content = '\n\n'.join(calendars_with_events)
    calendars_without_events_content = '\n\n'.join(calendars_without_events)
    current_date = date.today().strftime("%d/%m/%Y")

    # Fill placeholders in template
    github_pages_content = template.replace(
        '[[[calendars_with_events]]]', calendars_with_events_content
    ).replace(
        '[[[calendars_without_events]]]', calendars_without_events_content
    ).replace(
        '[[[last_update]]]', current_date
    )

    with open('readme.md', 'w') as f:
        f.write(github_pages_content)

    return True
