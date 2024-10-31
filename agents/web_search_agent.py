# agents/web_search_agent.py

from agents.agent import Agent
from utils.get_web_search import get_duckduckgo_links

class WebSearchAgent(Agent):
    def handle(self, user_input):
        # Extract the search query from user input
        # For simplicity, we'll assume the entire input is the query
        links = get_duckduckgo_links(user_input)
        return f"Here are some relevant links:\n{links}"