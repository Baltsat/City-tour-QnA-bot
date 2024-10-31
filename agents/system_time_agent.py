# agents/system_time_agent.py

import datetime
from agents.agent import Agent

class SystemTimeAgent(Agent):
    def handle(self, user_input):
        current_time = datetime.datetime.now().strftime("%H:%M")
        return f"The current system time is {current_time}."