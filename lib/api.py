import requests
import pandas as pd
import urllib.parse


BASE_HREF = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/"


def _fetch_api_data(path: str) -> pd.DataFrame:
    print(f"Fetching: {BASE_HREF + path}")
    r = requests.get(BASE_HREF + path)
    if r.status_code == 200:
        return pd.DataFrame(r.json()['value'])
    else:
        print(r.json())
        raise Exception('API_FAIL')


def fetch_committees() -> pd.DataFrame:
    """
    Fetches all the committees from the API
    :return: Dataframe with the committees pd.DataFrame
    """
    committees = _fetch_api_data(
        "Commissie?$select=NaamNL&$filter=NaamNL ne null&$orderby=NaamNL asc"
    )

    print(f"Found {committees.shape[0]} committees from the API")

    # Commissie voor de Rijksuitgaven exists multiple times, so we need to remove the duplicates
    return committees.drop_duplicates()


def fetch_events_for_committee_name(committee_name: str) -> pd.DataFrame:
    """
    Fetches the events for the committee from the API
    :param str committee_name: Filename without the extension
    :return: A dataframe with the events of the committee pd.DataFrame
    """

    safe_committee_name = urllib.parse.quote(committee_name.encode('utf8'))

    events = _fetch_api_data(
        "Activiteit?" +
        "$filter=(Soort eq 'Commissiedebat' and Aanvangstijd ne null " +
        f"and (Status eq 'Gepland' or Status eq 'Uitgevoerd') and Voortouwnaam eq '{safe_committee_name}')&" +
        "$select=Aanvangstijd,Besloten,Eindtijd,Kamer,Locatie,Noot,Onderwerp,Status,Voortouwnaam&" +
        "$orderby=Aanvangstijd asc&" +
        "$expand=ActiviteitActor($select=ActorNaam,ActorFractie)")

    print(f"Found {events.shape[0]} events from the API")

    return events
