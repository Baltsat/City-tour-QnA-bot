# agents/weather_agent.py

import os
import requests
from agents.agent import Agent

class WeatherAgent(Agent):
    def __init__(self, llm):
        self.llm = llm
        self.api_key = os.environ.get("OPENWEATHER_API_KEY")
        self.api_endpoint = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city: str) -> str:
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        try:
            response = requests.get(self.api_endpoint, params=params)
            data = response.json()

            if response.status_code == 200:
                weather_desc = data['weather'][0]['description']
                temp = data['main']['temp']
                return f"The current weather in {city} is {weather_desc} with a temperature of {temp}°C."
            else:
                return f"Error: {data.get('message', 'Unable to retrieve weather data.')}"
        except requests.RequestException as e:
            return f"Error fetching weather data: {e}"

    def extract_city(self, user_input: str) -> str:
        # Use the LLM to extract the city name from the user's input
        prompt = (
            f"Extract the city name from the following query: '{user_input}' "
            "and provide its standard international name in English. Do not include any additional text."
        )

        messages = [
            {"role": "system", "content": "You are an assistant that extracts city names from user queries."},
            {"role": "user", "content": prompt}
        ]

        response = self.llm.invoke(messages)
        return response.content.strip()

    def handle(self, user_input):
            city = self.extract_city(user_input)
            if not city or city.lower() == "weather":
                city = "Paphos"  # Default to Paphos if no city is extracted
            weather_info = self.get_weather(city)
            return weather_info