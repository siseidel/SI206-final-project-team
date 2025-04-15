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

###### Walk Score Collection

###### Median Income Collection

###### Air Quality Collection

###### Main

def main():
    print('start')
    cur, conn = set_up_database("final_project.db")
    create_main_database(cur, conn)

main()