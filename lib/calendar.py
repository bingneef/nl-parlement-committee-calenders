import pandas as pd
from ics import Calendar, Event
from lib.tools import text_from_html_string


def _description_from_api_event(api_event: pd.DataFrame) -> str:
    description = ""
    if api_event['Noot'] is not None:
        description += f"Notitie:\n{text_from_html_string(api_event['Noot'])}\n\n"

    if api_event['Locatie'] is not None:
        description += f"Locatie:\n{api_event['Locatie']}\n\n"

    if api_event['Besloten']:
        description += "Het is een besloten evenement\n\n"
    else:
        description += "Het is niet een besloten evenement\n\n"

    if len(api_event['ActiviteitActor']) > 0:
        description += f"Aanwezigen ({len(api_event['ActiviteitActor'])}):\n"

        for actor in api_event['ActiviteitActor']:
            description += f"  {actor['ActorNaam']} ({actor['ActorFractie'] or 'onbekend'})\n"

        description += "\n\n"

    return description


def _event_from_api_event(api_event: pd.DataFrame) -> Event:
    # Escape hatch when no start- or end time is set
    if api_event['Aanvangstijd'] is None or api_event['Eindtijd'] is None:
        return None

    event = Event()
    event.name = api_event['Onderwerp']
    event.begin = api_event['Aanvangstijd']
    event.end = api_event['Eindtijd']
    event.description = _description_from_api_event(api_event)

    return event


def calendar_from_events(api_events: pd.DataFrame) -> Calendar:
    """
    Returns a calendar filled with the api_events
    :param pd.DataFrame api_events: Filename without the extension
    :return: The calendar object Calendar
    """
    calendar = Calendar()

    # If no api_events, just return an empty calendar
    if api_events.empty:
        return calendar

    for __, api_event in api_events.iterrows():
        event = _event_from_api_event(api_event)
        if event is not None:
            calendar.events.add(event)

    return calendar
