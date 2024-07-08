import requests
import os
from dotenv import load_dotenv

load_dotenv()
APPID = os.getenv('WEATHER_APPID')

def get_weather():
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": "Charleston",
        "appid": APPID,
        "units": "imperial"
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather = data['weather'][0]
        description = weather['description']
        temp = main['temp']
        feels_like = main['feels_like']
        humidity = main['humidity']
        wind = data['wind']['speed']
        
        weather_info = f"The weather in Charleston right now is {description} with a temperature of {temp} degrees Fahrenheit, but feels like: {feels_like} degrees Fahrenheit, with a humidity of {humidity}"
        return weather_info
    else:
        return "Weather information could not be retrieved."

if __name__ == "__main__":
    city = "Charleston"
    print(get_weather(city))
