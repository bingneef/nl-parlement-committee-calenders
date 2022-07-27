import requests
import pandas as pd
import urllib.parse
import logging


BASE_HREF = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/"


def fetch_api_data(path):
    logging.debug(f"Fetching: {BASE_HREF + path}")
    r = requests.get(BASE_HREF + path)
    if r.status_code == 200:
        return pd.DataFrame(r.json()['value'])
    else:
        print(r.json())
        raise Exception('API_FAIL')


def fetch_committees():
    return fetch_api_data(
        "Commissie?$select=NaamNL,Afkorting&$filter=DatumActief ne null and Afkorting ne null and " +
        "NaamNL ne null&$orderby=NaamNL asc"
    )


def fetch_events_for_committee_abbr(committee_abbr):
    safe_committee_abbr = urllib.parse.quote(committee_abbr.encode('utf8'))
    return fetch_api_data(
        "Activiteit?" +
        "$filter=(Soort eq 'Commissiedebat' and Aanvangstijd ne null and (Status eq 'Gepland' or Status eq 'Uitgevoerd') and " +
        f"Voortouwafkorting eq '{safe_committee_abbr}')&" +
        "$select=Onderwerp,Aanvangstijd,Eindtijd,Besloten,Status,Voortouwafkorting&" +
        "$orderby=Aanvangstijd asc&" +
        "$expand=ActiviteitActor($select=ActorNaam,ActorFractie)")
