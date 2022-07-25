import requests
import pandas as pd

BASE_HREF = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/"
Sid_diza = 'S-1-365867521-2120874753-3622109579-1217932645-2021516714-2069959739'


def fetch_api(path):
    r = requests.get(BASE_HREF + path)
    if r.status_code == 200:
        return r.json()['value']
    else:
        print(r.json())


data = fetch_api(
    f"Activiteit?$filter=(Soort eq 'Commissiedebat' and (Status eq 'Gepland' or Status eq 'Uitgevoerd') and SidVoortouw eq '{Sid_diza}')&$select=Onderwerp,Aanvangstijd,Status&$orderby=Aanvangstijd asc&$expand=ActiviteitActor($select=ActorNaam,ActorFractie)")
print(len(data), data)

df = pd.DataFrame(data)
df['ActorCount'] = df['ActiviteitActor'].apply(len)
df.drop(columns=['ActiviteitActor']).to_csv('data/diza.csv')

print('Done')