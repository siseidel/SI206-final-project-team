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

income_api_key = "af614668bd001dc7e26d03720691fff838c126cd" 

def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

def create_main_database(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Main (city_id INTEGER PRIMARY KEY, city TEXT, state_id TEXT, county_id INTEGER, zip_code INTEGER, walk_score INTEGER, median_income INTEGER, air_quality INTEGER)")
    conn.commit()

def create_state_id(cur, conn):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS states (
            state_id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT UNIQUE NOT NULL,
            abbreviation TEXT NOT NULL
        )
    """)
    
    states_data = [
        ('Alabama', 'AL'),
        ('Alaska', 'AK'),
        ('Arizona', 'AZ'),
        ('Arkansas', 'AR'),
        ('California', 'CA'),
        ('Colorado', 'CO'),
        ('Connecticut', 'CT'),
        ('Delaware', 'DE'),
        ('Florida', 'FL'),
        ('Georgia', 'GA'),
        ('Hawaii', 'HI'),
        ('Idaho', 'ID'),
        ('Illinois', 'IL'),
        ('Indiana', 'IN'),
        ('Iowa', 'IA'),
        ('Kansas', 'KS'),
        ('Kentucky', 'KY'),
        ('Louisiana', 'LA'),
        ('Maine', 'ME'),
        ('Maryland', 'MD'),
        ('Massachusetts', 'MA'),
        ('Michigan', 'MI'),
        ('Minnesota', 'MN'),
        ('Mississippi', 'MS'),
        ('Missouri', 'MO'),
        ('Montana', 'MT'),
        ('Nebraska', 'NE'),
        ('Nevada', 'NV'),
        ('New Hampshire', 'NH'),
        ('New Jersey', 'NJ'),
        ('New Mexico', 'NM'),
        ('New York', 'NY'),
        ('North Carolina', 'NC'),
        ('North Dakota', 'ND'),
        ('Ohio', 'OH'),
        ('Oklahoma', 'OK'),
        ('Oregon', 'OR'),
        ('Pennsylvania', 'PA'),
        ('Rhode Island', 'RI'),
        ('South Carolina', 'SC'),
        ('South Dakota', 'SD'),
        ('Tennessee', 'TN'),
        ('Texas', 'TX'),
        ('Utah', 'UT'),
        ('Vermont', 'VT'),
        ('Virginia', 'VA'),
        ('Washington', 'WA'),
        ('West Virginia', 'WV'),
        ('Wisconsin', 'WI'),
        ('Wyoming', 'WY')
    ]

    for state, abbr in states_data:
        cur.execute("INSERT OR IGNORE INTO states (state, abbreviation) VALUES (?, ?)", (state, abbr))


###### City Collection

def city_data(file):
    with open(file) as file:
        file = file.readlines()
    cityList = []
    for i in range(len(file)):
        line = file[i].split(',')
        city_name = line[0].strip('"')
        state = line[2].strip('"')
        county_name = line[5].strip('"')
        zip_code = line[15].strip('"')
        zip_code = zip_code.split()[0]
        cityList.append((city_name, state, county_name, zip_code))
        if len(cityList) == 150:
            break
    print(cityList)
    print(len(cityList))
    return cityList

###### Walk Score Collection

def walk_transit(cityList):
    base_url = "https://www.walkscore.com"
    transitList = []
    workedList = []
    count = 0
    print("0% done...")
    for city, state, county, zip_code in cityList:
        correct_city = city.replace(" ", "_")
        new_url = f"{base_url}/{state}/{correct_city}"
        page = requests.get(new_url)
        
        if page.ok:
            workedList.append(city)
            soup = BeautifulSoup(page.content, 'html.parser')
            try:
                class_name = soup.find("div", style="padding: 0; margin: 0; border: 0; outline: 0; position: absolute; top: 0; bottom: 0; left: 0; right: 0;" )
                walk = class_name.find('img').get('alt')
                walk_score = int(walk.split()[0])
                transitList.append((city, state, county, zip_code, walk_score))
            except:
                transitList.append((city, state, county, zip_code, 200))

        else:
            transitList.append((city, state, county, zip_code, 200))
            count += 1
        if count % 15 == 0:
            print(f"{count/1.5}% done...")
        count += 1
    print(transitList[:50])
    print(len(transitList))
    return transitList

###### Median Income Collection

def get_income_by_zip(cityList, income_api_key):
    # Census ZCTA codes use 5-digit format
    url = "https://api.census.gov/data/2021/acs/acs5"

    for city in cityList:
        zip_code = city[3]
        params = {
            "get": "B19013_001E",  # Median household income
            "for": f"zip code tabulation area:{zip_code}",
            "key": income_api_key
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            # First row is the column headers
            headers = data[0]
            values = data[1]
            income = values[0]
            return f"Median household income for ZIP code {zip_code}: ${income}"
        else:
            return f"Error: {response.status_code} - {response.text}"


###### Air Quality Collection

###### Main

def main():
    print('start')
    cur, conn = set_up_database("final_project.db")
    create_main_database(cur, conn)
    cityList = city_data('uscities.csv')
    print('finish city collection...')
    walk_transit(cityList)

main()