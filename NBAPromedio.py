import json
import csv

# Load the data from the JSON file
with open('nba_salaries.json', 'r') as file:
    data = json.load(file)

# Save the player names, seasons, and salaries to a CSV file
with open('players_seasons_salaries.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['player_name', 'season_2022_23', 'season_2023_24', 'season_2024_25', 'season_2025_26']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for player_info in data:
        player_name = player_info['name']
        player_salaries = player_info['salaries']
        row_data = {'player_name': player_name}
        for idx, season in enumerate(['season_2022_23', 'season_2023_24', 'season_2024_25', 'season_2025_26']):
            row_data[season] = player_salaries[idx] if idx < len(player_salaries) else ''
        writer.writerow(row_data)
