import pandas as pd

#---Load the Data---#
file_path = 'C:\\Users\\garre\\OneDrive\\Desktop\\Coding\\PokemonStats\\raw_pokemon_data.xlsx'
sheet_name = 'Masters Data'
df = pd.read_excel(file_path, sheet_name=sheet_name)

"""print(df.info())"""

#---Perform Basic Cleaning---#
df['Start Date'] = pd.to_datetime(df['Start Date'])
df = df.rename(columns={'Tournament': 'tournament',
                        'Start Date': 'start_date',
                        'Regulation': 'regulation',
                        'Event Level': 'event_level',
                        'Player': 'player',
                        'Placing': 'placing',
                        'Pokemon': 'pokemon',
                        'Tera Type': 'tera_type',
                        'Ability': 'ability',
                        'Item': 'item',
                        'Move 1': 'move_1',
                        'Move 2': 'move_2',
                        'Move 3': 'move_3',
                        'Move 4': 'move_4'})

#---Create Dataframes---#
# 0. Get Total Number of Teams + Pokemon per Tournament
teams_per_tour = df.groupby('tournament')['player'].nunique().rename('total_teams').reset_index()
pokemon_per_tour = df.groupby(['tournament', 'pokemon'])['player'].nunique().rename('pokemon_count').reset_index()

# 1. Tournaments
tournaments = df[['tournament', 'start_date', 'regulation', 'event_level']]
tournaments = tournaments[['tournament', 'start_date', 'regulation', 'event_level']].drop_duplicates().reset_index(drop=True)
"""print(tournaments)"""

# 2. Pokemen Usage
usage_mons = df[['pokemon', 'tournament', 'player']]
usage_mons = usage_mons.groupby(['tournament', 'pokemon'])['player'].nunique().rename('teams_used').reset_index()
usage_mons = usage_mons.merge(teams_per_tour, on='tournament')

usage_mons['usage_perc'] = usage_mons['teams_used'] / usage_mons['total_teams'] * 100
usage_mons = usage_mons.sort_values(['tournament', 'usage_perc'])
usage_mons = usage_mons.drop(['total_teams'], axis=1)

# 3. Item Usage
usage_items = df[['pokemon', 'tournament', 'item', 'player']]
usage_items = usage_items.groupby(['tournament', 'pokemon', 'item'])['player'].nunique().rename('item_count').reset_index()
usage_items = usage_items.merge(pokemon_per_tour, on=['tournament', 'pokemon'])

usage_items['usage_perc'] = usage_items['item_count'] / usage_items['pokemon_count'] * 100
usage_items = usage_items.drop(['pokemon_count'], axis=1)

# 4. Move Usage
move_cols = ['move_1', 'move_2', 'move_3', 'move_4']

all_moves = (df[['tournament','pokemon','player'] + move_cols].melt(
         id_vars=['tournament','pokemon','player'],
         value_vars=move_cols,
         var_name='move_slot',
         value_name='move').dropna(subset=['move']))

usage_moves = all_moves.groupby(['tournament', 'pokemon', 'move'])['player'].nunique().rename('move_count').reset_index()
usage_moves = usage_moves.merge(pokemon_per_tour, on=['tournament', 'pokemon'])

usage_moves['usage_perc'] = usage_moves['move_count'] / usage_moves['pokemon_count'] * 100

print(usage_moves)

# 5. Tera Usage
usage_tera = df[['pokemon', 'tournament', 'tera_type', 'player']]
usage_tera = usage_tera.groupby(['tournament', 'pokemon', 'tera_type'])['player'].nunique().rename('teams_used').reset_index()
usage_tera = usage_tera.merge(pokemon_per_tour, on=['tournament', 'pokemon'])

usage_tera['usage_perc'] = usage_tera['teams_used'] / usage_tera['pokemon_count'] * 100
usage_tera = usage_tera.drop(['pokemon_count'], axis=1)