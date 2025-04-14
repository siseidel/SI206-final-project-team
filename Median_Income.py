import sqlite3
import os

a = 'uscities.csv'

def make_county_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Income (city_id TEXT PRIMARY KEY, median_income INTEGER)")
    conn.commit()

def county_data(file, cur, conn):
    with open(file) as file:
        file = file.read()
    for i in range(len(file)):
        line = file[i].split(',')
        city_name = line[0]
        state = line[2]
        county_name = line[5]
        cur.execute("INSERT OR IGNORE INTO Income (county, median_income) VALUES (?,?)", (name, income_data[name]))
    conn.commit()

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


