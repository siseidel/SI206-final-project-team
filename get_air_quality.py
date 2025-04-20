import requests
import sqlite3

API_KEY = "2B7FD6DF-81FB-4965-8A64-8267C2CFF58D"
BASE_URL = "https://www.airnowapi.org/aq/forecast/zipCode/"

def fetch_air_quality(zip_code, date="2025-04-15", distance=10):
    params = {
        "format": "application/json",
        "zipCode": zip_code,
        "date": date,
        "distance": distance,
        "API_KEY": API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed for zip code {zip_code}: {e}")
        return []

def create_air_quality_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS AirQuality (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zip_code TEXT,
            parameter TEXT,
            aqi INTEGER,
            category TEXT,
            forecast_date TEXT,
            date_fetched TEXT,
            UNIQUE(zip_code, parameter, forecast_date)
        )
    """)

def insert_air_quality(cur, conn, zip_codes):
    new_inserts = 0
    for zip_code in zip_codes:
        results = fetch_air_quality(zip_code)
        for item in results:
            date_forecast = item.get("DateForecast")
            parameter = item.get("ParameterName")
            aqi = item.get("AQI")
            category = item.get("Category", {}).get("Name")

            cur.execute("""
                INSERT OR IGNORE INTO AirQuality 
                (zip_code, parameter, aqi, category, forecast_date, date_fetched)
                VALUES (?, ?, ?, ?, ?, DATE('now'))
            """, (zip_code, parameter, aqi, category, date_forecast))

            if cur.rowcount == 1:
                new_inserts += 1
                print(f"Inserted: {zip_code}, {parameter}, AQI {aqi}, Category: {category}, Forecast: {date_forecast}")

            if new_inserts >= 25:
                print("Reached 25 new inserts. Stopping.")
                conn.commit()
                return
    conn.commit()

def main():
    conn = sqlite3.connect("climate_data.db")
    cur = conn.cursor()
    
    create_air_quality_table(cur)

    # Replace zipcodes 
    zip_codes = ["07008", "10001", "30301", "60601", "94102"]
    
    insert_air_quality(cur, conn, zip_codes)

    conn.close()

if __name__ == "__main__":
    main()
