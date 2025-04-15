#  SI 206 Final Project
# 
# Title: Air Pollution and Income in American Cities
# Team: S.U.I.T (Students of Urban Information Technology)
# Team Members: Faris Khojah, Sierra Seidel, Michelle Zheng

import requests
import os
import sqlite3
from bs4 import BeautifulSoup
import json
import time

def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

def create_main_database(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Main (city_id INTEGER PRIMARY KEY, city TEXT, state TEXT, county TEXT, transit_score INTEGER, median_income INTEGER, air_pollution INTEGER)")
    conn.commit()

###### Median Income Collection

def make_median_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Income (county TEXT PRIMARY KEY, median_income INTEGER)")
    conn.commit()

def read_csv(csv):
    with open(csv) as file:
        raw_data = file.readlines()
    data = {}
    for line in raw_data:
        if 'Median_Household_Income_2022' in line:
            line = line.split(',')
            data[line[2].lstrip('"')] = int(line[-1])
    return data

def enter_income_data(cur, conn, income_data):
    for name in income_data:
        cur.execute("INSERT OR IGNORE INTO Income (county, median_income) VALUES (?,?)", (name, income_data[name]))
    conn.commit()

def median_income_data(cur, conn, file):
    make_median_table(cur, conn)
    raw_data = read_csv(file)
    enter_income_data(cur, conn, raw_data)

###### City Collection

def get_cities(file):
    with open(file) as file:
        data = json.load(file)
    
    cityList = []
    for line in data:
        cityList.append((line['city'], line['state']))
    
    return cityList

def get_other_city_data(cityList):
    new_cityList = []
    for city, state in cityList[1:]:
        time.sleep(2)
        city_state = f"{'+'.join(city.split())}+{state}"
        url = f'https://nominatim.openstreetmap.org/search?q={city_state}&format=json&addressdetails=1'
        
        resp = requests.get(url)
        print(resp.text)
        data = json.loads(resp.text)

        lat = data['lat']
        lon = data['lon']
        county = data['address']['county']

        new_cityList.append((city, state, county, lat, lon))
        print(city, state, county, lat, lon)
    return new_cityList

###### Air Pollution Collection

def get_air_pollution():
    pass

def main():
    print('start')
    cur, conn = set_up_database("final_project.db")
    create_main_database(cur, conn)
    median_income_data(cur, conn,'Unemployment2023.csv')
    print('finished 1')
    cityList = get_cities('american_cities_simple.json')
    cityList = get_other_city_data(cityList)
    print('finished 2')
    print(cityList)
    # transitList = walk_transit(cityList)
    # print('finished 3')
    # enter_city_transit_data(cur, conn, transitList)
    # print('finished 4')

main()