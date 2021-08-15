#import libraries
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

#scrape a single game shots. We will allow users to enter a base url (16379)
base_url = 'https://understat.com/match/'
match = str(input('Please enter the match id: '))
url = base_url+match

#Use requests to get the webpage and BeautifulSoup to parse the page
res = requests.get(url)
soup = BeautifulSoup(res.content, 'lxml')
scripts = soup.find_all('script')

#get only the shotsData
strings = scripts[1].string

# strip unnecessary symbols and get only JSON data 
ind_start = strings.index("('")+2 
ind_end = strings.index("')") 
json_data = strings[ind_start:ind_end] 
json_data = json_data.encode('utf8').decode('unicode_escape')

#convert string to json format
data = json.loads(json_data)

#making a list
x = []
y = []
xG = []
result = []
team = []
data_away = data['a']
data_home = data['h']

for index in range(len(data_home)):
    for key in data_home[index]:
        if key == 'X':
            x.append(data_home[index][key])
        if key == 'Y':
            y.append(data_home[index][key])
        if key == 'h_team':
            team.append(data_home[index][key])
        if key == 'xG':
            xG.append(data_home[index][key])
        if key == 'result':
            result.append(data_home[index][key])

for index in range(len(data_away)):
    for key in data_away[index]:
        if key == 'X':
            x.append(data_away[index][key])
        if key == 'Y':
            y.append(data_away[index][key])
        if key == 'a_team':
            team.append(data_away[index][key])
        if key == 'xG':
            xG.append(data_away[index][key])
        if key == 'result':
            result.append(data_away[index][key])

col_names = ['x','y','xG','result','team']

#Converting it to a dataframe
df = pd.DataFrame([x,y,xG,result,team],index=col_names)
df = df.T

print(df)

#convert dataframe to a csv file
output = df.to_csv('Chelsea vs Crystal Palace.csv')

