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
    committees = fetch_api_data(
        "Commissie?$select=NaamNL&$filter=NaamNL ne null&$orderby=NaamNL asc"
    )

    # Commissie voor de Rijksuitgaven exists multiple times, so we need to remove the duplicates
    return committees.drop_duplicates()


def fetch_events_for_committee_name(committee_name):
    safe_committee_name = urllib.parse.quote(committee_name.encode('utf8'))
    return fetch_api_data(
        "Activiteit?" +
        "$filter=(Soort eq 'Commissiedebat' and Aanvangstijd ne null " +
        f"and (Status eq 'Gepland' or Status eq 'Uitgevoerd') and Voortouwnaam eq '{safe_committee_name}')&" +
        "$select=Aanvangstijd,Besloten,Eindtijd,Kamer,Locatie,Noot,Onderwerp,Status,Voortouwnaam&" +
        "$orderby=Aanvangstijd asc&" +
        "$expand=ActiviteitActor($select=ActorNaam,ActorFractie)")
