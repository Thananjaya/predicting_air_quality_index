#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 18:25:59 2020

@author: thananjaya
"""

import requests
import os
import time
import pandas as pd


def get_data():
    if not os.path.exists("data/"):
        os.makedirs("data/")
        
    for year in range(2013, 2019):
        for month in range(1, 13):
            if month < 10:
                http_url = "https://en.tutiempo.net/climate/0{}-{}/ws-432950.html".format(month, year)
            else:
                http_url = "https://en.tutiempo.net/climate/{}-{}/ws-432950.html".format(month, year)
            
            retreived_data = requests.get(http_url)
            text = retreived_data.text.encode('utf=8')
            
            if not os.path.exists("data/html_data/{}".format(year)):
                os.makedirs("data/html_data/{}".format(year))
            
            with open("data/html_data/{}/{}.html".format(year, month), "wb") as output:
                output.write(text)

def sampling_data():
    df = pd.read_csv('./data/aqi_data/aqi2013.csv')
    df['datetime'] = pd.to_datetime(df['Date']+ ' ' +df['Time'])
    df = df.set_index('datetime')
    df = df.drop(['Date', 'Time'], axis=1)
    new_df = pd.to_numeric(df['PM2.5'], errors='coerce').resample('D').mean()
    print(new_df.head())



# get_data()
sampling_data()