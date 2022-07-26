import pandas as pd
from ics import Calendar, Event


def _add_event_to_calendar(calendar, event):
    e = Event()

    if event['Aanvangstijd'] is None or event['Eindtijd'] is None:
        return calendar
        
    e.name = event['Onderwerp']
    e.begin = event['Aanvangstijd']
    e.end = event['Eindtijd']
    calendar.events.add(e)

    return calendar


def generate_calendar_from_events(events):
    # If no events, just return an empty calendar
    if events.empty:
        return Calendar()
    
    events['ActorCount'] = events['ActiviteitActor'].apply(len)
    events = events.drop(columns=['ActiviteitActor'])

    c = Calendar()
    for __, event in events.iterrows():
        c = _add_event_to_calendar(c, event)

    return c
