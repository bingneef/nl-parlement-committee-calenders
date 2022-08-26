from typing import NoReturn
import pandas as pd
from lib.api import fetch_committees, fetch_events_for_committee_name
from lib.calendar import calendar_from_events
from lib.tools import generate_safe_filename, current_formatted_time
from lib.docs import generate_docs_from_committees


def _persist_committee_calender(committee: pd.DataFrame) -> NoReturn:
    calendar = calendar_from_events(committee['Events'])

    # Remove unsafe characters for filenames
    safe_file_name = generate_safe_filename(committee['NaamNL'], '.ics')
    with open(f"calendars/{safe_file_name}", 'w') as file:
        file.writelines(calendar)


def main() -> NoReturn:
    print(f"START RUN AT {current_formatted_time()}")
    # Fetch committees
    committees = fetch_committees()

    # Assign events to committees
    committees['Events'] = committees['NaamNL'].apply(fetch_events_for_committee_name)

    # Persist calendars
    committees.apply(_persist_committee_calender, axis=1)

    # Generate new readme
    generate_docs_from_committees(committees)

    print(f"Found {committees['Events'].apply(len).sum()} events for {len(committees)} committees")
    print(f"COMPLETED RUN AT {current_formatted_time()}")


if __name__ == '__main__':
    main()
