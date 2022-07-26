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


def fetch_active_commissions():
    return fetch_api_data(
        f"Commissie?$select=NaamNL,Afkorting&$filter=(DatumInactief eq null) and (Afkorting ne null) and (NaamNL ne null)&$orderby=GewijzigdOp asc"
    )


def fetch_events_for_commission_abbr(commission_abbr):
    safe_commission_abbr = urllib.parse.quote(commission_abbr.encode('utf8'))
    return fetch_api_data(
        f"Activiteit?$filter=(Soort eq 'Commissiedebat' and (Aanvangstijd ne null) and (Status eq 'Gepland' or Status eq 'Uitgevoerd') and Voortouwafkorting eq '{safe_commission_abbr}')&$select=Onderwerp,Aanvangstijd,Eindtijd,Besloten,Status,Voortouwafkorting&$orderby=Aanvangstijd asc&$expand=ActiviteitActor($select=ActorNaam,ActorFractie)"
    )


def fetch_all_commission_events():
    return fetch_api_data(
        f"Activiteit?$filter=(Soort eq 'Commissiedebat' and (Aanvangstijd ne null) and (Status eq 'Gepland' or Status eq 'Uitgevoerd'))&$select=Onderwerp,Aanvangstijd,Eindtijd,Besloten,Status,Voortouwafkorting&$orderby=Aanvangstijd asc&$expand=ActiviteitActor($select=ActorNaam,ActorFractie)"
    )