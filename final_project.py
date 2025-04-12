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

def US_state_city_url(cityList):
    list_url = []
    base_url = "https://www.walkscore.com"
    for state, city in cityList:
        abbr = state_abbreviations.get(state)
        if not abbr:
            #If abbreviations not found
            continue 
        correct_city = city.replace(" ", "_")
        new_url = f"{base_url}/{abbr}/{correct_city}"
        list_url.append(new_url)
    # print(list_url)
    # for url in list_url:
    new_url = "https://www.walkscore.com/NY/New_York"
    page = requests.get(new_url)
    if page.ok:
        soup = BeautifulSoup(page.content, 'html.parser')
        class_name = soup.find("div", style="padding: 0; margin: 0; border: 0; outline: 0; position: absolute; top: 0; bottom: 0; left: 0; right: 0;" )
        print(class_name)
        walk = class_name.find('img').get('alt')
        walk_score = int(walk.split()[0])
        transit = class_name.find_all('img')[1].get('alt')
        transit_score = int(transit.split()[0])
        print("\n")
        print(walk_score, transit_score)

def gas_prices():
    states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', ...]  # All 50 states
    url_template = "https://gasprices.aaa.com/index.php?premiumhtml5map_get_state_info={state}&map_id=18"

    for state in states:
        url = url_template.format(state=state)
        response = requests.post(url)
        print(state, response.text)  # Parse this with BeautifulSoup or regex


def main():
    cityList = US_state_city("US_States_and_Cities.json")
    US_state_city_url(cityList)
    gas_prices()

main()
       






