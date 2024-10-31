# agents/news_agent.py

from agents.agent import Agent
from utils.get_rss import fetch_latest_paphos_news

class NewsAgent(Agent):
    def handle(self, user_input):
        # Define the URL of the Paphos news website
        url = "https://www.paphoslife.com/news"
        news = fetch_latest_paphos_news(url)
        if news:
            return f"Also, here are the latest news from Paphos:\n{news}"
        else:
            return "Sorry, I couldn't retrieve the latest news at the moment."