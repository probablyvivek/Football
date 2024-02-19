import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd


# Headers for the request
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
}

# Function to extract player data
def extract_player_data(team_name, team_div, transfer_type, all_player_data):
    transfer_table = team_div.find_all('table')

    if transfer_table and len(transfer_table) >= 2:
        table_headers = [th.text.strip() for th in transfer_table[transfer_type].find('thead').find_all('th')]
        rows = transfer_table[transfer_type].find('tbody').find_all('tr')

        for row in rows:
            player_data = [team_name, 'In' if transfer_type == 0 else 'Out']
            for td in row.find_all('td'):
                data = td.text.strip()
                player_data.append(data)

            all_player_data.append(player_data)

# Function to scrape transfer data
def scrape_transfer_data(season):
    all_player_data = []
    
    base_url = f"https://www.transfermarkt.co.uk/premier-league/transfers/wettbewerb/GB1/plus/?saison_id={season}&s_w=&leihe=1&intern=0&intern=1"
    pageTree = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(pageTree.content, 'html.parser')
    
    teams = soup.select('h2.content-box-headline a')
    teams_list = [team.text.strip() for team in teams if team.text.strip()]

    for team_name in teams_list:
        team_anchor = soup.find('a', text=team_name)
        team_div = team_anchor.find_parent('div', class_='box') if team_anchor else None

        if team_div:
            extract_player_data(team_name, team_div, transfer_type=0, all_player_data=all_player_data)
            extract_player_data(team_name, team_div, transfer_type=1, all_player_data=all_player_data)

    # Define the columns for the DataFrame
    columns = ['Team', 'Transfer Direction', 'Player', 'Age', 'Nationality', 'Position', 'Short Position', 'Market Value', 'Left Team', 'Left Team Flag', 'Fee']

    # Create the DataFrame with the specified columns
    df = pd.DataFrame(all_player_data, columns=columns)

    # Drop the 'Nationality' column and 'Left Team' as it is not needed
    df = df.drop(columns=['Nationality', 'Left Team'])

    # Rename the 'Left Team Flag' column to 'Left Team'
    df = df.rename(columns={'Left Team Flag': 'Left Team'})

    return df

def clean_player_names(df):
    # First, attempt to insert a space between full names and their abbreviations or duplicates
    df['Player'] = df['Player'].str.replace(r'([a-z])([A-Z])', r'\1 \2', regex=True)
    
    # Second, remove common abbreviation patterns, like "K. Havertz" following the full name
    df['Player'] = df['Player'].str.replace(r'\b[A-Z]\. [A-Z][a-z]+', '', regex=True)
    
    # Optional: Remove any trailing spaces left after cleaning
    df['Player'] = df['Player'].str.strip()
    
    return df



def clean_fee_column(df):
    # Ensure the 'Fee' column is of type string
    df['Fee'] = df['Fee'].astype(str)
    
    df['Fee'] = (
        df['Fee']
        .str.replace('€', '', regex=False)  # Remove the Euro symbol
        .str.replace('m', 'e6', regex=False)  # Convert 'm' to 'e6' (for million)
        .str.replace('Loan fee:', '', regex=False)  # Remove 'Loan fee:' text
        .str.replace(',', '.', regex=False)  # Convert comma to dot for decimals
        .str.extract(r'(\d+\.?\d*)')  # Extract the numeric part
        .fillna(0)  # Fill NaN with 0
        .astype(float)  # Convert the column to float
    )
    return df


def create_charts(df):
    # Clean the fee column
    df = clean_fee_column(df)
    transfer_counts = df.groupby(['Team', 'Transfer Direction']).size().unstack().fillna(0)
    # Aggregating the total fees for incoming and outgoing transfers
    total_fees = df.groupby(['Team', 'Transfer Direction'])['Fee'].sum().unstack().fillna(0)
    
    
    # Plotting the data
    st.write("### Number of Players Transferred In and Out by Team")
    st.bar_chart(transfer_counts)
    
    st.write("### Total Fees for Players Transferred In and Out by Team (in €)")
    st.bar_chart(total_fees)

# Streamlit interface to include the charts
st.title('Premier League Transfer Data')
years = list(range(2000, 2025))

# Create a select box for the user to choose a season
season = st.selectbox('Select the season:', years)

if st.button('Fetch Transfer Data'):
    # No need to check if season is a digit since it's selected from a predefined list
    with st.spinner('Fetching data...'):
        df = scrape_transfer_data(str(season))
            
            # Clean the fee column to prepare data for analysis
        df = clean_fee_column(df)
            
            # Clean the player names to ensure data consistency
        df = clean_player_names(df)

            # Sort the DataFrame for better readability and analysis
        df = df.sort_values(by=['Team', 'Transfer Direction'], ascending=[True, True])
            
            # Reset the index to start from 1 for display purposes
        df.reset_index(drop=True, inplace=True)
            
            # Create and display charts based on the cleaned data
        create_charts(df)
            
            # Display the cleaned and sorted transfer data
        st.write("### Transfer Data")
        st.dataframe(df)  # Using st.dataframe for better formatting
            
            # Provide the option to download the cleaned data
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
                label='Download Data as CSV',
                data=csv,
                file_name='transfer_data.csv',
                mime='text/csv'
            )
else:
    st.error('Please click the button to fetch the transfer data.')
