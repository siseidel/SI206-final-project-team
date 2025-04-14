import sqlite3
import os

a = 'uscities.csv'

def create_main_database(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Main (city TEXT PRIMARY KEY, state TEXT, county TEXT, walk_score INTEGER, transit_score INTEGER, median_income INTEGER)")
    conn.commit()

def county_data(file, cur, conn):
    with open(file) as file:
        file = file.read()

    cityList = []

    for i in range(len(file)):
        if i % 30 == 0:
            line = file[i].split(',')
            city_name = line[0]
            state = line[2]
            county_name = line[5]
            cur.execute("INSERT OR IGNORE INTO Main (city, state, county) VALUES (?,?,?)", (city_name, state, county_name))
            cityList.append(state, city_name)
            listLen = list(cur.execute("SELECT * FROM Main"))
        if len(listLen[0]) == 110:
            break

    conn.commit()
    return cityList


def US_state_city(jsonfile):
    with open(jsonfile, 'r') as file:
        data = json.load(file)

    state_city_pairs = []
    for state, cities in data.items():
        selected_cities = cities[:3]
        for city in selected_cities:
            state_city_pairs.append((state, city))
            if len(state_city_pairs) == 110:
                break
        if len(state_city_pairs) == 110:
            break

    cityList = []
    for state, city in state_city_pairs:
        cityList.append((state, city))
    # print(f"{cityList}")
    return cityList
