from typing import Tuple
import pandas as pd
from lib.tools import generate_safe_filename
from datetime import datetime


def _generate_calendar_url(name: str) -> str:
    return (
        "https://raw.githubusercontent.com/bingneef/rekenkamer-commissie-scraper/main/calendars/" +
        generate_safe_filename(name, 'ics')
    )


def _generate_committee_rows(committees: pd.DataFrame) -> Tuple[list[str], list[str]]:
    calendars_with_events: [str] = []
    calendars_without_events: [str] = []

    for __, committee in committees.iterrows():
        calendar_url = _generate_calendar_url(committee['NaamNL'])

        committee_row = "\n".join([
            f"**{committee['NaamNL']}** ({committee['Events'].size} gevonden)\\",
            f"[{calendar_url}]({calendar_url})"
        ])

        if committee['Events'].size == 0:
            calendars_without_events.append(committee_row)
        else:
            calendars_with_events.append(committee_row)

    return calendars_with_events, calendars_without_events


def generate_docs_from_committees(committees: pd.DataFrame) -> bool:
    """
    Writes documentation files for the committees calendars
    :param pd.DataFrame committees: Dataframe of the committees with their events
    :return: True bool
    """

    calendars_with_events, calendars_without_events = _generate_committee_rows(committees)

    with open('templates/index.md') as f:
        template = f.read()

    # Fill placeholders in template
    doc_content = template.replace(
        '[[[calendars_with_events]]]', '\n\n'.join(calendars_with_events)
    ).replace(
        '[[[calendars_without_events]]]', '\n\n'.join(calendars_without_events)
    ).replace(
        '[[[last_update]]]', datetime.now().strftime("%d/%m/%Y %H:%M")
    )

    # Write to readme and doc/index
    for destination in ['readme.md', 'docs/index.md']:
        with open(destination, 'w') as f:
            f.write(doc_content)

    return True
