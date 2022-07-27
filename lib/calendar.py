from ics import Calendar, Event
from bs4 import BeautifulSoup


def _generate_calendar_description_from_event(event):
    description = ""
    if event['Noot'] is not None:
        note = BeautifulSoup(event['Noot'], "lxml").get_text(separator="\n")
        description += f"Notitie:\n{note}\n\n"

    if event['Locatie'] is not None:
        description += f"Locatie:\n{event['Locatie']}\n\n"

    if event['Besloten']:
        description += "Het is een besloten evenement\n\n"
    else:
        description += "Het is niet een besloten evenement\n\n"

    if len(event['ActiviteitActor']) > 0:
        description += f"Aanwezigen ({event['ActorCount']}):\n"
        for actor in event['ActiviteitActor']:
            description += f"  {actor['ActorNaam']} ({actor['ActorFractie']})\n"
        description += "\n\n"

    return description


def _add_event_to_calendar(calendar, event):
    e = Event()

    if event['Aanvangstijd'] is None or event['Eindtijd'] is None:
        return calendar

    e.name = event['Onderwerp']
    e.begin = event['Aanvangstijd']
    e.end = event['Eindtijd']
    e.description = _generate_calendar_description_from_event(event)
    calendar.events.add(e)

    return calendar


def generate_calendar_from_events(events):
    # If no events, just return an empty calendar
    if events.empty:
        return Calendar()

    events['ActorCount'] = events['ActiviteitActor'].apply(len)

    c = Calendar()
    for __, event in events.iterrows():
        c = _add_event_to_calendar(c, event)

    return c
