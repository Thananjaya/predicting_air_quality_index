#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 18:25:59 2020

@author: thananjaya
"""

import requests
import os
import pandas as pd
from bs4 import BeautifulSoup

def get_data():
    for year in range(2013, 2016):
        climate_df = pd.DataFrame(columns=['Day', 'T', 'TM', 'Tm', 'SLP', 'H', 'PP', 'VV', 'V', 'VM', 'VG', 'RA', 'SN', 'TS', 'FG'])
        for month in range(1, 13):
            if month < 10:
                http_url = "https://en.tutiempo.net/climate/0{}-{}/ws-432950.html".format(month, year)
            else:
                http_url = "https://en.tutiempo.net/climate/{}-{}/ws-432950.html".format(month, year)
            
            retreived_data = requests.get(http_url).text

            soup = BeautifulSoup(retreived_data, "lxml")
            climate_table = soup.find("table", attrs={"class": "medias mensuales numspan"})
            
            climate_data = climate_table.find_all("tr")
            for data in climate_data[1:-2]:
                table_data = data.find_all("td")
                for row in table_data:
                    row_data.append(row.get_text())
                climate_df.loc[len(climate_df)] = row_data

        start_date = "1/1/{}".format(year)
        end_date = "1/12/{}".format(year)
        climate_df.index = pd.date_range(start=start_date, end=end_date, greq='MS')


# def lol():
#     http_url = "https://en.tutiempo.net/climate/0{}-{}/ws-432950.html".format(1, 2013)
#     retreived_data = requests.get(http_url).text

#     soup = BeautifulSoup(retreived_data, "lxml")
#     climate_table = soup.find("table", attrs={"class": "medias mensuales numspan"})

#     tags = []
#     climate_header = climate_table.find_all("th")
#     for header in climate_header:
#         tags.append(header.get_text())
#     tags.pop()
    
#     climate_df = pd.DataFrame(columns=tags)

#     climate_data = climate_table.find_all("tr")
#     for data in climate_data[1:-2]:
#         table_data = data.find_all("td")
#         row_data = []
#         for row in table_data:
#             row_data.append(row.get_text())
#         climate_df.loc[len(climate_df)] = row_data
#     start_date = date(2013,1)
#     end_date= date(2013,1)
#     climate_df.index = pd.date_range(start_date, end_date)
#     print(climate_df)
                
                    
def sampling_data():
    new_sampled_df = pd.DataFrame()
    for year in range(2013, 2016):
        df = pd.read_csv("./data/aqi_data/aqi{}.csv".format(year))
        df["datetime"] = pd.to_datetime(df["Date"]+ ' ' +df["Time"], errors="coerce")
        df = df.set_index("datetime")
        df = df.drop(["Date", "Time"], axis=1)
        new_df = pd.to_numeric(df['PM2.5'], errors='coerce').resample('D').mean()
        if new_sampled_df.empty:
            new_sampled_df = new_df.copy()
        new_sampled_df = pd.concat([new_sampled_df, new_df], axis=0)
    return new_sampled_df

lol()