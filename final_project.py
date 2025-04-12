#  SI 206 Final Project
# 
# Title: Gas-prices, Walk Scores, and Transit Scores in American Cities
# Team: S.U.I.T (Students of Urban Information Technology)
# Team Members: Faris Khojah, Sierra Seidel, Michelle Zheng
#
# 
# 

import json
import requests
import os
import sqlite3
from bs4 import BeautifulSoup

# house keeping

state_abbreviations = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}

def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn


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

def median_income_data():
    cur, conn = set_up_database("final_project.db")
    make_median_table(cur, conn)
    raw_data = read_csv('Unemployment2023.csv')
    enter_income_data(cur, conn, raw_data)


###### City Collection


def US_state_city(jsonfile):
    with open(jsonfile, 'r') as file:
        data = json.load(file)

    state_city_pairs = []
    for state, cities in data.items():
        selected_cities = cities[:3]
        for city in selected_cities:
            state_city_pairs.append((state, city))
            if len(state_city_pairs) == 100:
                break
        if len(state_city_pairs) == 100:
            break

    cityList = []
    for state, city in state_city_pairs:
        cityList.append((state, city))
    # print(f"{cityList}")
    return cityList

###### Walk Score and Transit Score Collection

def walk_transit(cityList):
    base_url = "https://www.walkscore.com"
    transitList = []

    for state, city in cityList:
        abbr = state_abbreviations.get(state)
        correct_city = city.replace(" ", "_")
        new_url = f"{base_url}/{abbr}/{correct_city}"
        page = requests.get(new_url)
        if page.ok:
            soup = BeautifulSoup(page.content, 'html.parser')
            try:
                class_name = soup.find("div", style="padding: 0; margin: 0; border: 0; outline: 0; position: absolute; top: 0; bottom: 0; left: 0; right: 0;" )
                walk = class_name.find('img').get('alt')
                walk_score = int(walk.split()[0])
                transit = class_name.find_all('img')[1].get('alt')
                transit_score = int(transit.split()[0])
                transitList.append((state, city, walk_score, transit_score))
            except:
                transitList.append((state, city, 200, 200))

        else:
            transitList.append((state, city, 200, 200))


def main():
    cityList = US_state_city("US_States_and_Cities.json")
    transitList = walk_transit(cityList)
    print(transitList)
    

main()
       






