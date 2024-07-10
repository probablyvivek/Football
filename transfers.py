import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Headers for the request
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
}

def extract_player_data(team_name, team_div, transfer_type, all_player_data):
    transfer_table = team_div.find_all('table')

    if transfer_table and len(transfer_table) >= 2:
        rows = transfer_table[transfer_type].find('tbody').find_all('tr')

        for row in rows:
            player_data = [team_name]
            for td in row.find_all('td'):
                data = td.text.strip()
                player_data.append(data)

            all_player_data.append(player_data)

def scrape_transfer_data():
    transfers_in = []
    transfers_out = []
    
    base_url = "https://www.transfermarkt.co.uk/premier-league/transfers/wettbewerb/GB1/plus/?saison_id=2024&s_w=&leihe=1&intern=0&intern=1"
    pageTree = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(pageTree.content, 'html.parser')
    
    teams = soup.select('h2.content-box-headline a')
    teams_list = [team.text.strip() for team in teams if team.text.strip()]

    for team_name in teams_list:
        team_anchor = soup.find('a', text=team_name)
        team_div = team_anchor.find_parent('div', class_='box') if team_anchor else None

        if team_div:
            extract_player_data(team_name, team_div, transfer_type=0, all_player_data=transfers_in)
            extract_player_data(team_name, team_div, transfer_type=1, all_player_data=transfers_out)

    return transfers_in, transfers_out, teams_list

def clean_data(df):
    # Rename columns
    df = df.rename(columns={
        'Market Value': 'Current Team',
        'Current Team': 'Market Value',
        'Joined': 'Joined From'
    })

    # Remove unnecessary columns
    df = df.drop(columns=['Contract Expires'])

    # Clean market value
    df['Market Value'] = df['Market Value'].str.replace('€', '').str.replace('m', '')
    df['Market Value'] = pd.to_numeric(df['Market Value'], errors='coerce')

    # Clean fee
    df['Fee'] = df['Fee'].str.replace('€', '').str.replace('m', '')
    df['Fee'] = pd.to_numeric(df['Fee'], errors='coerce')

    return df

def create_summary(team, df_in, df_out):
    total_spent = df_in[df_in['Team'] == team]['Fee'].sum()
    total_received = df_out[df_out['Team'] == team]['Fee'].sum()
    players_in = len(df_in[df_in['Team'] == team])
    players_out = len(df_out[df_out['Team'] == team])
    
    summary = f"""
    Transfer Summary for {team} (2024/2025 Season):
    - Players In: {players_in}
    - Players Out: {players_out}
    - Total Spent: €{total_spent:.2f}m
    - Total Received: €{total_received:.2f}m
    - Net Spend: €{total_spent - total_received:.2f}m
    """
    return summary

st.title('Premier League Transfer Data 2024/2025')

if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

if not st.session_state.data_loaded:
    if st.button('Fetch Transfer Data for 2024/2025 Season'):
        with st.spinner('Fetching data...'):
            transfers_in, transfers_out, teams_list = scrape_transfer_data()

            # Create DataFrames
            columns = ['Team', 'Player', 'Age', 'Position', 'Market Value', 'Current Team', 'Joined', 'Contract Expires', 'Fee']
            st.session_state.df_in = pd.DataFrame(transfers_in, columns=columns)
            st.session_state.df_out = pd.DataFrame(transfers_out, columns=columns)

            # Clean the data
            st.session_state.df_in = clean_data(st.session_state.df_in)
            st.session_state.df_out = clean_data(st.session_state.df_out)

            st.session_state.teams_list = teams_list
            st.session_state.data_loaded = True

if st.session_state.data_loaded:
    selected_team = st.selectbox('Select Team:', ['All Teams'] + st.session_state.teams_list)

    if selected_team != 'All Teams':
        df_in_display = st.session_state.df_in[st.session_state.df_in['Team'] == selected_team]
        df_out_display = st.session_state.df_out[st.session_state.df_out['Team'] == selected_team]
        st.text(create_summary(selected_team, st.session_state.df_in, st.session_state.df_out))
    else:
        df_in_display = st.session_state.df_in
        df_out_display = st.session_state.df_out

    st.subheader('Transfers In')
    st.dataframe(df_in_display)

    st.subheader('Transfers Out')
    st.dataframe(df_out_display)

    csv_in = df_in_display.to_csv(index=False).encode('utf-8')
    csv_out = df_out_display.to_csv(index=False).encode('utf-8')

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label='Download Transfers In as CSV',
            data=csv_in,
            file_name=f'transfers_in_2024_2025_{selected_team}.csv',
            mime='text/csv'
        )
    with col2:
        st.download_button(
            label='Download Transfers Out as CSV',
            data=csv_out,
            file_name=f'transfers_out_2024_2025_{selected_team}.csv',
            mime='text/csv'
        )
else:
    st.info('Click the button to fetch the transfer data for the 2024/2025 season.')