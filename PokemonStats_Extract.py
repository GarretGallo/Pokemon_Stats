import requests
import sys
import pandas as pd
from datetime import datetime

#---Get Data from API---#
response = requests.request("GET", "https://pokedata.ovh/apiv2/vg/tournaments")
if response.status_code!=200:
    print('Unexcepted Status Code:', response.status_code)
    sys.exit()

events = response.json().get("vg", {}).get('data', [])

#---Map Regulation + Event Level + Event Cutoff---#
def get_regulation(start_date_str):
    d = pd.to_datetime(start_date_str)

    if datetime(2023, 1, 2) <= d < datetime(2023, 2, 1):
        return 'Regulation A'
    elif datetime(2023, 2, 1) <= d < datetime(2023, 4, 1):
        return 'Regulation B'
    elif datetime(2023, 4, 1) <= d < datetime(2023, 7, 1):
        return 'Regulation C'
    elif datetime(2023, 7, 1) <= d < datetime(2023, 10, 1):
        return 'Regulation D'
    elif datetime(2023, 10, 1) <= d < datetime(2024, 1, 4):
        return 'Regulation E'
    elif datetime(2024, 1, 4) <= d < datetime(2024, 5, 1):
        return 'Regulation F'
    elif datetime(2024, 5, 1) <= d < datetime(2024, 9, 1):
        return 'Regulation G'
    elif datetime(2024, 9, 1) <= d < datetime(2025, 1, 6):
        return 'Regulation H'
    elif datetime(2025, 1, 6) <= d < datetime(2025, 5, 1):
        return 'Regulation G'
    elif datetime(2025, 5, 1) <= d < datetime(2025, 9, 1):
        return 'Regulation I'
    else:
        return 'Unknown or out of range'
    
def event_level(tourn_name: str):
    name = tourn_name.lower()

    if 'regional championship' in name:
        return 'Regional'
    elif 'international championship' in name:
        return 'International'
    elif 'world championship' in name:
        return 'Worlds'
    else:
        return 'Other'

sv_start = datetime(2023, 1, 2)

#---Fetch Data and Store---#
teams = []
for event in events:
    start_date = event.get("date", {}).get("start")
    start_dt = pd.to_datetime(start_date)

    if start_dt < sv_start:
        continue

    tourn_id = event['id']
    tourn_name = event['name']
    regulation = get_regulation(start_date)
    level = event_level(tourn_name)

    detail_url = f"https://www.pokedata.ovh/apiv2/id/{tourn_id}/vg"
    detail_resp = requests.get(detail_url)

    # 1) Make sure we got a 200
    if detail_resp.status_code != 200:
        print(f"Skipping {tourn_id}: HTTP {detail_resp.status_code}")
        continue

    # 2) Try to parse JSON, otherwise skip
    try:
        detail_json = detail_resp.json()
    except ValueError:
        print(f"Skipping {tourn_id}: Invalid JSON:\n{detail_resp.text[:200]}")
        continue

    masters_div = None
    for div in detail_json.get('tournament_data', []):
        if div.get('division') == 'masters':
            masters_div = div
            break
    if masters_div is None:
        continue
    masters_data = masters_div.get('data', [])
 
    for player in masters_data:
        name = player.get('name')
        placing = player.get('placing')
        for mon in player.get("decklist", []):
            badges = mon.get("badges", [])
            teams.append({
                "Tournament ID": tourn_id,
                "Tournament":    tourn_name,
                "Start Date":    start_date,
                "Regulation":    regulation,
                "Event Level":   level,
                "Player":        name,
                "Placing":       placing,
                "Pokemon":       mon.get("name"),
                "Tera Type":     mon.get("teratype"),
                "Ability":       mon.get("ability"),
                "Item":          mon.get("item"),
                "Move 1":        badges[0] if len(badges)>0 else None,
                "Move 2":        badges[1] if len(badges)>1 else None,
                "Move 3":        badges[2] if len(badges)>2 else None,
                "Move 4":        badges[3] if len(badges)>3 else None})

df = pd.DataFrame(teams)

path = '*INSERT FILE PATH HERE*'
df.to_excel(path, index=False, sheet_name='Masters Data')
