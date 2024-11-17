import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Step 1: Load environment variables from .env file
load_dotenv()

# Step 2: Get the API key from environment variables
API_KEY = os.getenv('OPEN_WEATHER_API_KEY')

# Step 3: Define the city for the weather forecast
CITY = 'London'

# Step 4: Construct the API request URL
url = f'http://api.openweathermap.org/data/2.5/forecast?q={CITY}&units=metric&cnt=5&appid={API_KEY}'

# Step 5: Make the request to the API
response = requests.get(url)
data = response.json()

# Step 6: Extract relevant data (temperature, time, etc.) from the response
weather_data = []
for entry in data['list']:
    weather_data.append({
        'datetime': entry['dt_txt'],
        'temperature': entry['main']['temp'],
        'humidity': entry['main']['humidity'],
        'pressure': entry['main']['pressure']
    })

# Step 7: Load data into a pandas DataFrame
df = pd.DataFrame(weather_data)

# Step 8: Perform some calculations
# 8.1: Calculate the average temperature
average_temp = df['temperature'].mean()

# 8.2: Calculate the max humidity
max_humidity = df['humidity'].max()

# 8.3: Calculate the average pressure
average_pressure = df['pressure'].mean()

# Step 9: Print the results
print(f"Weather forecast for {CITY}:")
print(df)
print("\nCalculations:")
print(f"Average Temperature: {average_temp:.2f}°C")
print(f"Max Humidity: {max_humidity}%")
print(f"Average Pressure: {average_pressure:.2f} hPa")