import pandas as pd
import os
import ssl
import lxml
ssl._create_default_https_context = ssl._create_unverified_context # Ignore SSL certificate errors

def get_data(url):
    team_name = url.split('/')[-1].replace('-Stats', '')
    df = pd.read_html(url, match="Round")[0]  # Automatically selects the first table that contains 'Round'
    df = df[['Date', 'Round', 'Venue', 'Opponent', 'Result', 'GF', 'xG', 'GA', 'xGA', 'Formation', 'Referee']]
    df = df[df['Round'].str.contains('Matchweek', na=False)].dropna()
    print(f"Data fetched successfully for {team_name}")
    return df, team_name  # Return both the DataFrame and the team name

urls = [
    'https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats'
]

directory = "./Programming/Snippets/Football_Data"
if not os.path.exists(directory):
    os.makedirs(directory)

# Fetch data for each URL
for url in urls:
    data, team_name = get_data(url) 
    # Save each team's data to a separate CSV file
    file_path = os.path.join(directory, f"{team_name}.xlsx")
    data.to_excel(file_path, index=False)