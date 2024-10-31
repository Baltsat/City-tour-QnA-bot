# agents/sea_water_temperature_agent.py

from agents.agent import Agent
from utils.get_sea_temperature import get_paphos_sea_temperature

class SeaWaterTemperatureAgent(Agent):
    def handle(self, user_input):
        temperature_info = get_paphos_sea_temperature()
        if temperature_info:
            return temperature_info
        else:
            return "Sorry, I couldn't retrieve the sea water temperature at the moment."