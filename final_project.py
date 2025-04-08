#  SI 206 Final Project
# 
# Title: Gas-prices, Walk Scores, and Transit Scores in American Cities
# Team: S.U.I.T (Students of Urban Information Technology)
# Team Members: Faris Khojah, Sierra Seidel, Michelle Zheng
#
# 
# 
import json

with open('US_States_and_Cities.json', 'r') as file:
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

for state, city in state_city_pairs:
    print(f"State: {state}, City: {city}")
