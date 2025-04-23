import matplotlib.pyplot as plt
import os
import sqlite3

####### Housekeeping

# Open up SQL database again
def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn

####### Data Calculation and Visulization

# Performs caluclation A to find the cities with the lowest and highest air quality scores and the average. In this case low is better.
def calculationA(cur, con):

    # finds average of all air quality scores collected
    airList = list(cur.execute("SELECT * FROM AQ"))
    total = 0
    for zip in airList:
        total += int(zip[1])
    AQ_average = total/len(airList)

    # connects the main and air quality databases to gather the city name and air quality score for each city
    cur.execute("SELECT Main.city, AQ.air_quality FROM Main JOIN AQ ON Main.zip_code = AQ.zip_code")
    city_AQ = cur.fetchall()

    # finds the cities with the lowest 4 and highest 4 air quality scores
    sorted_data = sorted(city_AQ, key=lambda x: x[1], reverse=True)
    lowest = sorted_data[:4]
    sorted_data = sorted(city_AQ, key=lambda x: x[1], reverse=False)
    highest = sorted_data[:4]

    # sorts the data into lists of names and data so it can be represented
    city_names = list()
    city_data = list()
    for i in range(len(lowest)):
        city_names.append(lowest[i][0])
        city_data.append(lowest[i][1])
        city_data.append(highest[i][1])
        city_names.append(highest[i][0])
    con.commit()

    # create bar graph
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

    ### Calculation Printing
    output = "\nCalculation A\n"
    output += "------------------------------------------------------------------------\n"
    output += "The 4 cities with the lowest air quality rating were:\n"
    for city in lowest:
        output += f"{city[0]} with score of {city[1]}\n"
    output += "\nThe 4 cities with the highest air quality rating were:\n"
    for city in highest:
        output += f"{city[0]} with score of {city[1]}\n"
    output += f"\nWith the average air quality score being {AQ_average}, air quality in the American cities we looked at were generally Okay to Poor.\n"
    output += "------------------------------------------------------------------------\n"

    return output

# Performs caluclation B to find correlation between median income of a city and the walk score of the city
def calculationB(cur, con):

    # collect all cities
    cur.execute("SELECT * FROM Main")
    cityList= cur.fetchall()

    median_income = list()
    walk_scores = list()
    cities = list()

    # finds the median income and walkscore of each city
    for city_id, city, state_id, zip_code in cityList:
        cur.execute("SELECT median_income FROM Income WHERE zip_code = (?)", (zip_code,))
        income = cur.fetchone()[0]
        median_income.append(income)

        cur.execute("SELECT walk_score FROM Walk_Score WHERE city_id = (?)", (city_id,))
        walk_score = cur.fetchone()[0]
        walk_scores.append(walk_score)

        cities.append(city)

    con.commit()

    # create scattergraph
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

    # Calculation for r score (correlation)
    n = len(median_income)
    sum_x = sum(median_income)
    sum_y = sum(walk_scores)
    sum_x_squared = sum(i ** 2 for i in median_income)
    sum_y_squared = sum(i ** 2 for i in walk_scores)
    sum_xy = sum(median_income[i] * walk_scores[i] for i in range(n))

    r = (n * sum_xy - sum_x * sum_y) / (
        ((n * sum_x_squared - sum_x ** 2) * (n * sum_y_squared - sum_y ** 2)) ** 0.5
)

    ### Calculation Output
    output = f"""

Calculation B
------------------------------------------------------------------------
The correlation coefficient for our data was {r}. This means that there is not correlation between median income and a city's walk score."
------------------------------------------------------------------------

"""
    return output

# Performs caluclation C to find the correlation between the air quality of a city and the median income through a pie graph
def calculationC(cur, con):

    # collects all cities with Good air quality
    cur.execute("SELECT zip_code FROM AQ WHERE air_quality <= 50")
    results = cur.fetchall()

    # creates pie chart labels
    labels = ['$75,000+', '$50,000-$75,000', '$25,000-$50,000', '$0-$25,000']
    # finds the median income of each of the cities with air quality score of Good and sorts them into groups
    group_1 = cur.execute('SELECT COUNT(*) FROM Income WHERE median_income >= 75000')
    group_2 = cur.execute('SELECT COUNT(*) FROM Income WHERE median_income >= 50000 AND median_income < 75000')
    group_3 = cur.execute('SELECT COUNT(*) FROM Income WHERE median_income >= 25000 AND median_income < 50000')
    group_4 = cur.execute('SELECT COUNT(*) FROM Income WHERE median_income >= 0 AND median_income < 25000')

    sizes = [group_1, group_2, group_3, group_4]

    colors = ['lightblue', 'lightgreen', 'lightcoral', 'red']

    # Create a pie chart
    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.0f cities', startangle=90)

    # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.axis('equal')

    # Title
    plt.title('Cities Fitting Different Characteristics')

    # Show the plot
    plt.show()

    ### Calculation Printing
    output = "\n\nCalculation C\n"
    output += "------------------------------------------------------------------------\n"
    output += "When looking at cities with air quality scores in the Good range (0-50)...\n"

    for i in range(len(sizes)):
        percentage = round(100 * sizes[i] / sum(sizes), 1)
        output += f"{sizes[i]} ({percentage}%) had a median income of {labels[i]}\n"

    output += "\nThis shows a correlation between the median income of a city and how clean the air is. "
    output += "The more money a city has, the better the air quality will be.\n"
    output += "------------------------------------------------------------------------\n"

    return output



# This code consolidates each data visulation and calculation function to make the main function cleaner
def main():
    cur, con = set_up_database('final_project.db')
    answerA = calculationA(cur, con)
    answerB = calculationB(cur, con)
    answerC = calculationC(cur, con)

    with open('calculations.txt', 'w') as file:
        file.write(answerA)
        file.write(answerB)
        file.write(answerC)

main()

