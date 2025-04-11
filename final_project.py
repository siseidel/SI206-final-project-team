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
from bs4 import BeautifulSoup

# house keeping

state_abbreviations = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}

def US_state_city(jsonfile):
    with open(jsonfile, 'r') as file:
        data = json.load(file)

    state_city_pairs = []

    for state, cities in data.items():
        selected_cities = cities[:3]
        for city in selected_cities:
            state_city_pairs.append((state, city))
            if len(state_city_pairs) == 100:
                break
        if len(state_city_pairs) == 100:
            break
    cityList = []
    for state, city in state_city_pairs:
        cityList.append((state, city))
    # print(f"{cityList}")
    return cityList

def US_state_city_url(cityList):
    list_url = []
    base_url = "https://www.walkscore.com"
    for state, city in cityList:
        abbr = state_abbreviations.get(state)
        if not abbr:
            #If abbreviations not found
            continue 
        correct_city = city.replace(" ", "_")
        new_url = f"{base_url}/{abbr}/{correct_city}"
        list_url.append(new_url)
    # print(list_url)
    # for url in list_url:
    new_url = "https://www.walkscore.com/NY/New_York"
    page = requests.get(new_url)
    if page.ok:
        soup = BeautifulSoup(page.content, 'html.parser')
        class_name = soup.find("div", style="padding: 0; margin: 0; border: 0; outline: 0; position: absolute; top: 0; bottom: 0; left: 0; right: 0;" )
        print(class_name)
        walk = class_name.find('img').get('alt')
        walk_score = int(walk.split()[0])
        transit = class_name.find_all('img')[1].get('alt')
        transit_score = int(transit.split()[0])
        print("\n")
        print(walk_score, transit_score)


            




    

def main():
    cityList = US_state_city("US_States_and_Cities.json")
    US_state_city_url(cityList)

main()
       






