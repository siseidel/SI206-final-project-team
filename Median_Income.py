import sqlite3
import os
import re

def get_county(state, city):
    with open('uscities.csv') as file:
        file = file.read()
    
    cities = file.find_all(fr'\S{city}')



