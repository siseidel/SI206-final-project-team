#  SI 206 Final Project
# 
# Title: Air Pollution and Income in American Cities
# Team: S.U.I.T (Students of Urban Information Technology)
# Team Members: Faris Khojah, Sierra Seidel, Michelle Zheng


####### Housekeeping

# First we imported everything we needed to complete the code.
import requests
import os
import sqlite3
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# Next we defined the api code we will need to gather our data
income_api_key = "af614668bd001dc7e26d03720691fff838c126cd" 
air_api_key = '02BAEBFB-182C-4DA5-AA70-3CF3DAA392EA'
# Switch with this key if the one above does not work: #2B7FD6DF-81FB-4965-8A64-8267C2CFF58D


# We set up a SQL database called final_project to house all of our data
def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

# We created the tables that will house our data in our database, defining each of the value headers of the tables
def create_main_database(cur, conn):
    # This table holds our main city data, used to connect each of the other tables
    cur.execute("CREATE TABLE IF NOT EXISTS Main (city_id INTEGER PRIMARY KEY, city TEXT, state_id INTEGER, zip_code INTEGER)")
    # This table holds the median incomes of zip codes for each city
    cur.execute("CREATE TABLE IF NOT EXISTS Income (zip_code INTEGER PRIMARY KEY, median_income INTEGER)")
    # This table holds the air quality of zip codes for each city
    cur.execute("CREATE TABLE IF NOT EXISTS AQ (zip_code INTEGER PRIMARY KEY, air_quality INTEGER)")
    # This table holds the walk score of each city, using the city id to identify them
    cur.execute("CREATE TABLE IF NOT EXISTS Walk_Score (city_id INTEGER PRIMARY KEY, walk_score INTEGER)")
    conn.commit()

# To avoid repeated string data we created a database that assigns each state with a state_id as an integer
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

####### Data Collection

# This code identifies 100 cities that were not previously used in eariler rounds
# from the file 'uscities.csv' collected from an online source and gathers their name, state, and zip codes
def city_data(file, usedList):
    # Open file
    with open(file) as file:
        file = file.readlines()
    cityList = []
    # Collect data
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
    # Give update
    print('grabing', len(cityList), 'cities...')
    # Return data
    return cityList

# This code collects the walk score of a city by webscraping www.walkscore.com
def walk_transit(city, state):
    # This is the base url
    base_url = "https://www.walkscore.com"

    # Add the params to the url
    correct_city = city.replace(" ", "_")
    new_url = f"{base_url}/{state}/{correct_city}"
    page = requests.get(new_url)
    
    # Webscrape the page for the walk score
    if page.ok:
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            class_name = soup.find("div", style="padding: 0; margin: 0; border: 0; outline: 0; position: absolute; top: 0; bottom: 0; left: 0; right: 0;" )
            walk = class_name.find('img').get('alt')
            walk_score = int(walk.split()[0])
            return walk_score
        # if not found return None
        except:
            return None

    else:
        return None
    
# This code collects the median income of a city from its zip code using an US government API
def get_income_by_zip(zip_code, income_api_key):    
    # This is the base url
    url = "https://api.census.gov/data/2021/acs/acs5"

    # We add on the params and collect the response
    params = {
        "get": "B19013_001E",  # Median household income
        "for": f"zip code tabulation area:{zip_code}",
        "key": income_api_key
    }
    response = requests.get(url, params=params)

    # Collect data
    if response.status_code == 200:
        data = response.json()
        values = data[1]
        income = int(values[0])
        # If there is not data available return None
        if income == -666666666:
            return None
        else:
            # Return income
            return income
    else:
        return None
    
# This code collect the air quality from an online API www.airnowapi.org from a cities zip code
def air_quality(zip_code, air_api_key):
    # This is the base url with params
    url = f"https://www.airnowapi.org/aq/forecast/zipCode/?format=application/json&zipCode={zip_code}&date=2025-04-15&distance=10&API_KEY={air_api_key}"
    data = requests.get(url)

    # Collecting data
    if data.status_code == 200:
        data = data.json()
        if data == []:
            # Returned None is data is not available
            return None
        else:
            # Returned air quality data
            air_quality = data[0]['AQI']
            if air_quality == -1:
                return None
            return air_quality

    else:
        return None
    
# This code inserts 25 rows of values into the SQL database at a time
def insert_25(cur, con, cityList):
    # Gathers where to start the city_id
    previousCities = list(cur.execute("SELECT * FROM Main"))
    i = len(previousCities)

    new_inserts = 0
    # Runs through each city and gathers all data from webscraping and APIs
    for city, state, zip_code in cityList:
        # Defines city_id as an integer
        city_id = i
        walk_score = walk_transit(city, state)
        # if walk score is found, looks for income
        if walk_score is not None:
            income = get_income_by_zip(zip_code, income_api_key)
            # if income is found, looks for air quality
            if income is not None:
                air = air_quality(zip_code, air_api_key)
                # if air quality is found, idenifity the state id and adds the data to their respective databases
                if air is not None:
                    i += 1
                    cur.execute("SELECT state_id FROM States WHERE abbreviation = (?)", (state,))
                    state_id = int(cur.fetchone()[0])

                    cur.execute("INSERT OR IGNORE INTO Main (city_id, city, state_id, zip_code) VALUES (?,?,?,?)", (city_id, city, state_id, zip_code))
                    cur.execute("INSERT OR IGNORE INTO Income (zip_code, median_income) VALUES (?,?)", (zip_code, income))
                    cur.execute("INSERT OR IGNORE INTO AQ (zip_code, air_quality) VALUES (?,?)", (zip_code,air))
                    cur.execute("INSERT OR IGNORE INTO Walk_Score (city_id, walk_score) VALUES (?,?)", (city_id, walk_score))
                    
                    # counts to 25 and stops the function when 25 cities are added the the database
                    if cur.rowcount == 1:
                        new_inserts += 1
                        # gives an update on how many cities are in database
                        print('finished', new_inserts)
                    if new_inserts >= 25:
                        break
    con.commit()

# This code runs all the functions
def main():
    usedCities = []

    # makes databases
    cur, conn = set_up_database('test_final_project.db')
    create_main_database(cur, conn)
    create_state_id(cur, conn)

    # enters 25 cities to the SQL database at a time until one-hundered are collected
    i = 1
    while len(list(cur.execute("SELECT * FROM AQ"))) < 100:
        # collects cities for data collection
        cityList = city_data('uscities.csv', usedCities)
        # adds used cities to used cities list so they are not double counted
        usedCities.extend(cityList)
        insert_25(cur, conn, cityList)
        # give update on progress
        print('finish round', i)
        i += 1

main()

