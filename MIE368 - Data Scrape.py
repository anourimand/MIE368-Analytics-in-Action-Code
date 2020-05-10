import html 
import lxml.html as lh
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from time import sleep
import csv
import numpy as np

# Part 1 - get the data of the players who we want to scrape from hltv.org
df = pd.read_csv (r'C:\Users\Arash\Desktop\Player-List.csv')
player_col = df['Player Links'] #gives the player calling data

# Part 2 - generate the website and scraping information
base_url='https://www.hltv.org' #general site
dates = '?startDate=2019-05-01&endDate=2019-08-01' #date range
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
play_num = len(player_col) #getting the size of the datapool
data = []  #creating an array for the scraper to store

# Part 3 - create the for loop to gather the required scraping information for each player
for i in range(play_num):
    player_stats = []
    url=base_url+player_col[i]+dates #make the full url
    req = requests.get(url, headers = headers)
    soup = bs(req.content, "html.parser")
    s = soup.find_all("div", {"class": "statistics"})#.find("div", class_="bold").text
    ss = soup.find_all("div", class_="stats-row")
    player_stats.append(player_col[i])
    for j in range(len(ss)):
        k = ss[j].contents[1].text
        player_stats.append(k)
    data.append(player_stats)
    sleep(0.1)
    #print(data[i])
#print(data)

df = pd.DataFrame(data)

column_name = ['Player ID','Total kills', 'Headshot %','Total deaths','K/D Ratio','Damage PR','Grenade DPR','Maps_played','Rounds_played','KPR', 'APR', 'DPR', 'Saved by teammate PR', 'Saved teammates PR', 'Rating 1.0']
df.columns= column_name

#Part 4 - Scraping the categorical data
#Pull out the based categorical data
cat_col_name = ['Rating 2.0', 'DPR', 'KAST', 'IMPACT', 'ADR', 'KPR']
cat_data = [] #new list for the categorical data

for i in range(play_num):
    player_cat_stats = []
    url=base_url+player_col[i]+dates #make the full url
    req = requests.get(url, headers = headers)
    #print(req.status_code)
    soup = bs(req.content, "html.parser")
    d = soup.find_all("div", {"class": "summaryBreakdownAverage"})
    dd = soup.find_all("div", class_="summaryStatBreakdownRow")
    category = soup.find_all("div", class_="summaryStatBreakdownSubHeader")
    category_number = soup.find_all("div", class_="summaryStatBreakdownDataValue")
    for j in range(len(category)):
        k = category_number[j].contents[0]
        player_cat_stats.append(k)
    cat_data.append(player_cat_stats)
    #print(data)
    sleep(0.1)

cat_col_name = ['Rating', 'DPR', 'KAST', 'IMPACT', 'ADR', 'KPR']
df2 = pd.DataFrame(cat_data)
df2.columns = cat_col_name #Create categorical dataframe

player_master = pd.concat([df, df2], axis=1) #creating master dataframe
player_output = player_master #creating output dataset
player_output.drop(['Headshot %','K/D Ratio', 'Damage PR','Grenade DPR', 'APR', 'DPR','Saved by teammate PR','Saved teammates PR','Rating 1.0','IMPACT'],axis=1)

# Final part: export to csv for ML and EDA
player_output.to_csv(r'C:\Users\Arash\Desktop\player_data_export.csv')



