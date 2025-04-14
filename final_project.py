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

Gov_Key = "af614668bd001dc7e26d03720691fff838c126cd"

def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

def create_main_database(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Main (city TEXT PRIMARY KEY, state TEXT, county TEXT, walk_score INTEGER, transit_score INTEGER, median_income INTEGER)")
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

def city_data(file):
    with open(file) as file:
        file = file.readlines()
    cityList = []
    for i in range(len(file)):
        line = file[i].split(',')
        city_name = line[0].strip('"')
        state = line[2].strip('"')
        county_name = line[5].strip('"')
        cityList.append((city_name, state, county_name))
        if len(cityList) == 200:
            break
    return cityList

###### Walk Score and Transit Score Collection

def walk_transit(cityList):
    base_url = "https://www.walkscore.com"
    transitList = []

    for city, state, county in cityList:
        correct_city = city.replace(" ", "_")
        new_url = f"{base_url}/{state}/{correct_city}"
        page = requests.get(new_url)
        if page.ok:
            soup = BeautifulSoup(page.content, 'html.parser')
            try:
                class_name = soup.find("div", style="padding: 0; margin: 0; border: 0; outline: 0; position: absolute; top: 0; bottom: 0; left: 0; right: 0;" )
                walk = class_name.find('img').get('alt')
                walk_score = int(walk.split()[0])
                transit = class_name.find_all('img')[1].get('alt')
                transit_score = int(transit.split()[0])
                transitList.append((city, state, county, walk_score, transit_score))
            except:
                transitList.append((city, state, county, 200, 200))

        else:
            transitList.append((city, state, county, 200, 200))
    return transitList

def enter_city_transit_data(cur, conn, transitList):
    for city in transitList:
        state = city[1]
        city_name = city[0]
        walk_score = city[3]
        transit_score = city[4]
        county = city[2]
        try:
            cur.execute("SELECT median_income FROM Income WHERE county = (?)", (f"{county} County",))
            median_income = int(cur.fetchone()[0])
        except:
            print("couldn't find county for", state, city_name, county)
            continue
        cur.execute("INSERT OR IGNORE INTO Main (city, state, county, walk_score, transit_score, median_income) VALUES (?,?,?,?,?,?)", (state, city_name, county, walk_score, transit_score, median_income))
    conn.commit()

def main():
    print('start')
    cur, conn = set_up_database("final_project.db")
    print('finished 1')
    create_main_database(cur, conn)
    median_income_data(cur, conn,'Unemployment2023.csv')
    cityList = city_data('uscities.csv')
    print('finished 2')
    transitList = walk_transit(cityList)
    print('finished 3')
    enter_city_transit_data(cur, conn, transitList)
    print('finished 4')
    

main()
       






