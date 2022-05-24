#Import Libraries
import requests
import pandas as pd

url = "https://fantasy.premierleague.com/api/bootstrap-static/"

#Request packagae to make GET request from the API endpoint
r = requests.get(url)

#Transform request variable to a JSON object
json = r.json()
json.keys()

#Build a Dataframe
elements_df = pd.DataFrame(json['elements'])

#Checking the columns
elements_df.columns

#Getting the required metrics for analysis
red_elements_df = elements_df[['team','id','first_name','second_name','web_name','element_type','now_cost','selected_by_percent', 'chance_of_playing_next_round', 'status', 'news']]

#Map Element type to actual position of the players
red_elements_df['element_type']=red_elements_df['element_type'].map({4:'Forward', 3:'Midfielder', 2:'Defender', 1:'Goalkeeper'})

#Map team names
red_elements_df['team']=red_elements_df['team'].map({1:'Arsenal',2:'Aston Villa',3:'Brentford',4:'Brighton',5:'Burnley',6:'Chelsea',7:'Palace',8:'Everton',9:'Leicester',10:'Leeds',11:'Liverpool',12:'City',13:'United',14:'Newcastle',15:'Norwich',16:'Southampton',17:'Spurs',18:'Watford',19:'West Ham',20:'Wolves'})

#Convert value to float
red_elements_df['selected_by_percent'] = red_elements_df.selected_by_percent.astype(float)

#Convert now_cost to actual value
red_elements_df['now_cost'] = red_elements_df['now_cost']/10

#Converting Datframe to Excel File
red_elements_df.to_excel("FPLData.xlsx", index=False)

