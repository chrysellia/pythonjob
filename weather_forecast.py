import requests
import pandas as pd
from dotenv import load_dotenv
import os
import sys
from datetime import datetime

def get_weather_forecast(city):
    # Step 1: Load environment variables from .env file
    load_dotenv()

    # Step 2: Get the API key from environment variables
    API_KEY = os.getenv('OPEN_WEATHER_API_KEY')
    
    if not API_KEY:
        raise ValueError("API key not found. Please check your .env file contains OPEN_WEATHER_API_KEY")

    # Step 3: Construct the API request URL
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&cnt=5&appid={API_KEY}'

    try:
        # Step 4: Make the request to the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        # Step 5: Check if the API response contains an error message
        if 'cod' in data and data['cod'] != '200':
            raise ValueError(f"API Error: {data.get('message', 'Unknown error')}")

        # Step 6: Verify the expected data structure exists
        if 'list' not in data:
            raise KeyError("Invalid API response format: 'list' key not found in response")

        # Step 7: Extract relevant data
        weather_data = []
        for entry in data['list']:
            weather_data.append({
                'datetime': datetime.strptime(entry['dt_txt'], '%Y-%m-%d %H:%M:%S'),
                'temperature': entry['main']['temp'],
                'humidity': entry['main']['humidity'],
                'pressure': entry['main']['pressure']
            })

        # Step 8: Load data into a pandas DataFrame
        df = pd.DataFrame(weather_data)
        
        # Step 9: Format datetime for better readability
        df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d %H:%M')

        # Step 10: Calculate statistics
        stats = {
            'average_temp': df['temperature'].mean(),
            'max_humidity': df['humidity'].max(),
            'average_pressure': df['pressure'].mean()
        }

        return df, stats

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to connect to the API: {str(e)}")
    except KeyError as e:
        raise KeyError(f"Error parsing API response: {str(e)}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")

def main():
    try:
        # Get city from command line argument or use default
        city = sys.argv[1] if len(sys.argv) > 1 else 'London'
        
        print(f"Fetching weather forecast for {city}...")
        df, stats = get_weather_forecast(city)

        # Print results
        print("\nWeather Forecast:")
        print("-" * 80)
        print(df.to_string(index=False))
        print("\nCalculations:")
        print("-" * 80)
        print(f"Average Temperature: {stats['average_temp']:.2f}°C")
        print(f"Max Humidity: {stats['max_humidity']}%")
        print(f"Average Pressure: {stats['average_pressure']:.2f} hPa")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()