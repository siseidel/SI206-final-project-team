import sqlite3
import os

def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

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






