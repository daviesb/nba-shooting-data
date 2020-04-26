# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 18:49:43 2019

@author: daviesb
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import numpy as np
import re

### read in list of players and urls
df_players = pd.read_excel(r'data/Player List 2020.xlsx', usecols='G:H')
### edit url to point to shooting data
df_players['url'].replace({'gamelog':'shooting'}, inplace=True, regex=True)

### create dataframe that we will append to
df_shooting = pd.DataFrame(columns = ['Split',
                                      'Value',
                                      'FG',
                                      'FGA',
                                      'Player Name'])

### some players will be missing. let's store their names in a list
missing_record = []

### loop to collect shooting data from bbref (need to finish exception handling)
for url, player in zip(df_players['url'], df_players['Player Name']):
    try:
        response = requests.get(url)
        soup = bs(response.text, 'lxml')
        table = soup.find('table', id='shooting')
        df = pd.read_html(str(table))[0]
        start_index = df.loc[(df.Split=='Shot Points')].index[0]
        end_index = df.loc[(df.Split=='Quarter')].index[0]
        df = df.iloc[start_index:end_index-1,0:4]
        df['Player Name'] = player
        df = df[df['Split'] != 'Split']
        df_shooting = df_shooting.append(df)
    except:
        missing_record.append(player)
        
        
