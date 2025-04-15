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