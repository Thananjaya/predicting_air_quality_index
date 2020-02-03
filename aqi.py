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

def get_climate_data():
    climate_df = pd.DataFrame(columns=['Day', 'T', 'TM', 'Tm', 'SLP', 'H', 'PP', 'VV', 'V', 'VM', 'VG', 'RA', 'SN', 'TS', 'FG'])
    for year in range(2013, 2016):
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
                row_data = []
                for row in table_data:
                    row_data.append(row.get_text())
                climate_df.loc[len(climate_df)] = row_data
    start_date = "1/1/2013"
    end_date = "31/12/2015"
    climate_df = climate_df.set_index(pd.date_range(start=start_date, end=end_date, freq='D'))
    return climate_df
                                    
def sampling_aqi_data():
    aqi_df = pd.DataFrame()
    for year in range(2013,2016):
        df = pd.read_csv("./data/aqi_data/aqi{}.csv".format(year))
        df["datetime"] = pd.to_datetime(df["Date"]+ ' ' +df["Time"], errors="coerce")
        df = df.set_index("datetime")
        df = df.drop(["Date", "Time"], axis=1)
        sampled_df = pd.to_numeric(df['PM2.5'], errors='coerce').resample('D').mean()
        if aqi_df.empty:
            aqi_df = sampled_df.copy()
        else:
            aqi_df = pd.concat([aqi_df, sampled_df], axis=0)
    return aqi_df

def merging_data(aqi_df, climate_df):
    final_df = pd.concat([climate_df, aqi_df], axis=1)
    return final_df

if __name__ == '__main__':
    climate_data = get_climate_data()
    aqi_data = sampling_aqi_data()
    final_df = merging_data(aqi_data, climate_data)
    print(final_df)
