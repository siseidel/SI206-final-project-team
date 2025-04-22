#  SI 206 Final Project
# 
# Title: Air Pollution and Income in American Cities
# Team: S.U.I.T (Students of Urban Information Technology)
# Team Members: Faris Khojah, Sierra Seidel, Michelle Zheng

import requests
import os
import sqlite3
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

income_api_key = "af614668bd001dc7e26d03720691fff838c126cd" 
air_api_key = '2B7FD6DF-81FB-4965-8A64-8267C2CFF58D'

def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

def create_main_database(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Main (city_id INTEGER PRIMARY KEY, city TEXT, state_id TEXT, zip_code INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS Income (zip_code INTEGER PRIMARY KEY, median_income INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS AQ (zip_code INTEGER PRIMARY KEY, air_quality INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS Walk_Score (city_id INTEGER PRIMARY KEY, walk_score INTEGER)")
    
    conn.commit()

def create_state_id(cur, conn):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS States (
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
        cur.execute("INSERT OR IGNORE INTO States (state, abbreviation) VALUES (?, ?)", (state, abbr))

###### City Collection

def city_data(file, usedList):
    with open(file) as file:
        file = file.readlines()
    cityList = []
    for i in range(len(file)):
        i = i + len(usedList)
        line = file[i].split(',')
        city_name = line[0].strip('"')
        state = line[2].strip('"')
        zip_code = line[15].strip('"')
        zip_code = zip_code.split()[0]
        cityList.append((city_name, state, zip_code))
        if len(cityList) == 100:
            break
    print('grabing', len(cityList), 'cities...')
    return cityList

###### Walk Score Collection

def walk_transit(city, state):
    base_url = "https://www.walkscore.com"

    correct_city = city.replace(" ", "_")
    new_url = f"{base_url}/{state}/{correct_city}"
    page = requests.get(new_url)
    
    if page.ok:
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            class_name = soup.find("div", style="padding: 0; margin: 0; border: 0; outline: 0; position: absolute; top: 0; bottom: 0; left: 0; right: 0;" )
            walk = class_name.find('img').get('alt')
            walk_score = int(walk.split()[0])
            return walk_score
        except:
            return None

    else:
        return None
    
###### Median Income Collection

def get_income_by_zip(zip_code, income_api_key):    
    url = "https://api.census.gov/data/2021/acs/acs5"

    params = {
        "get": "B19013_001E",  # Median household income
        "for": f"zip code tabulation area:{zip_code}",
        "key": income_api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        values = data[1]
        income = int(values[0])
        if income == -666666666:
            return None
        else:
            return income
    else:
        return None
    
###### Air Quality Collection

def air_quality(zip_code, air_api_key):

    url = f"https://www.airnowapi.org/aq/forecast/zipCode/?format=application/json&zipCode={zip_code}&date=2025-04-15&distance=10&API_KEY={air_api_key}"
    data = requests.get(url)
    if data.status_code == 200:
        data = data.json()
        if data == []:
            return None
        else:
            air_quality = data[0]['AQI']
            if air_quality == -1:
                return None
            return air_quality

    else:
        return None
    
def insert_25(cur, con, cityList):
    previousCities = list(cur.execute("SELECT * FROM Main"))
    i = len(previousCities)
    new_inserts = 0
    for city, state, zip_code in cityList:
        city_id = i
        walk_score = walk_transit(city, state)
        if walk_score is not None:
            income = get_income_by_zip(zip_code, income_api_key)
            if income is not None:
                air = air_quality(zip_code, air_api_key)
                if air is not None:
                    i += 1
                    cur.execute("SELECT state_id FROM States WHERE abbreviation = (?)", (state,))
                    state_id = int(cur.fetchone()[0])

                    cur.execute("INSERT OR IGNORE INTO Main (city_id, city, state_id, zip_code) VALUES (?,?,?,?)", (city_id, city, state_id, zip_code))
                    cur.execute("INSERT OR IGNORE INTO Income (zip_code, median_income) VALUES (?,?)", (zip_code, income))
                    cur.execute("INSERT OR IGNORE INTO AQ (zip_code, air_quality) VALUES (?,?)", (zip_code,air))
                    cur.execute("INSERT OR IGNORE INTO Walk_Score (city_id, walk_score) VALUES (?,?)", (city_id, walk_score))
                    
                    print('finished', i+1)
                    if cur.rowcount == 1:
                        new_inserts += 1
                    if new_inserts >= 25:
                        break
    
    con.commit()

def make_data():
    # usedCities = []
    # print(len(usedCities))
    cur, conn = set_up_database('final_project.db')
    # create_main_database(cur, conn)
    # create_state_id(cur, conn)
    # for i in range(4):
    #     cityList = city_data('uscities.csv', usedCities)
    #     usedCities.extend(cityList)
    #     insert_25(cur, conn, cityList)
    #     print('finish round', i+1)
    return cur, conn

def calculationA(cur, con):
    airList = list(cur.execute("SELECT * FROM AQ"))
    total = 0
    for zip in airList:
        total += int(zip[1])
    AQ_average = total/len(airList)
    print(total)
    print(AQ_average)

    cur.execute("SELECT Main.city, AQ.air_quality FROM Main JOIN AQ ON Main.zip_code = AQ.zip_code")
    city_AQ = cur.fetchall()

    sorted_data = sorted(city_AQ, key=lambda x: x[1], reverse=True)
    lowest = sorted_data[:4]
    sorted_data = sorted(city_AQ, key=lambda x: x[1], reverse=False)
    highest = sorted_data[:4]

    city_names = list()
    city_data = list()
    for i in range(len(lowest)):
        city_names.append(lowest[i][0])
        city_data.append(lowest[i][1])
        city_data.append(highest[i][1])
        city_names.append(highest[i][0])
    print(city_names, city_data)
    con.commit()

    plt.figure(figsize=(8, 6))
    bars = plt.bar(city_names, city_data, color='skyblue')

    # Add average line
    plt.axhline(AQ_average, color='red', linestyle='--', label=f'Average = {AQ_average:.1f}')

    # Labels and title
    plt.xlabel('City')
    plt.ylabel('Air Quality Index')
    plt.title('Air Quality by City')
    plt.legend()
    plt.tight_layout()

    # Show the plot
    plt.show()



def calculationB(cur, con):

    cur.execute("SELECT Main.city, Main.state_id FROM Income JOIN Walk_Score ON Income.zip_code = Walk.zip_code")
    city_AQ = cur.fetchall()

    median_income = list()
    walk_scores = list()
    cities = list()
    plt.figure(figsize=(8, 6))
    plt.scatter(median_income, walk_scores, color='blue')

    # Labels and title
    plt.xlabel('Median Income ($)')
    plt.ylabel('Walk Score')
    plt.title('Median Income vs Walk Score by City')

    # Optionally, label each point with the city name
    for i, city in enumerate(cities):
        plt.text(median_income[i], walk_scores[i], city, fontsize=9, ha='right')

    # Show the plot
    plt.tight_layout()
    plt.show()



def use_data(cur, con):
    calculationA(cur, con)
    calculationB()
    # calculationC()
    pass


def main():
    cur, con = make_data()
    use_data(cur, con)

main()

