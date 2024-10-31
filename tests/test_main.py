# tests/test_main.py

import unittest
from unittest.mock import MagicMock, patch
from main import Chatbot
from agents.sea_water_temperature_agent import SeaWaterTemperatureAgent
from agents.weather_agent import WeatherAgent
from agents.system_time_agent import SystemTimeAgent
from agents.command_execution_agent import CommandExecutionAgent
from agents.news_agent import NewsAgent
from agents.web_search_agent import WebSearchAgent
import json
import os

class TestChatbot(unittest.TestCase):
    def setUp(self):
        # Mock the LLM
        self.llm_mock = MagicMock()
        self.llm_mock.invoke = MagicMock()
        # Mock the response from the LLM
        self.llm_mock.invoke.return_value.content = "This is a test response from the LLM."

        # Initialize the chatbot with the mocked LLM
        self.chatbot = Chatbot(self.llm_mock)

        # Load data.json
        data_path = os.path.join('data', 'data.json')
        with open(data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    @patch('agents.sea_water_temperature_agent.get_paphos_sea_temperature')
    def test_sea_water_temperature_agent(self, mock_get_temperature):
        # Mock the sea water temperature
        mock_get_temperature.return_value = "Today's sea temperature in Paphos is 24°C"

        # Test the chatbot response when asking about sea water temperature
        user_input = "What is the current sea water temperature in Paphos?"
        response = self.chatbot.orchestrate(user_input)
        expected_response = "Today's sea temperature in Paphos is 24°C"
        self.assertEqual(response, expected_response)

    @patch('agents.weather_agent.WeatherAgent.get_weather')
    def test_weather_agent(self, mock_get_weather):
        # Mock the weather information
        mock_get_weather.return_value = "The current weather in Paphos is sunny with a temperature of 28°C."

        # Test the chatbot response when asking about weather
        user_input = "What's the weather like today?"
        response = self.chatbot.orchestrate(user_input)
        expected_response = "The current weather in Paphos is sunny with a temperature of 28°C."
        self.assertEqual(response, expected_response)

    @patch('agents.system_time_agent.datetime')
    def test_system_time_agent(self, mock_datetime):
        # Mock the current time
        mock_datetime.datetime.now.return_value.strftime.return_value = "15:42"

        # Test the chatbot response when asking for the current time
        user_input = "What time is it?"
        response = self.chatbot.orchestrate(user_input)
        expected_response = "The current system time is 15:42."
        self.assertEqual(response, expected_response)

    @patch('agents.command_execution_agent.subprocess.check_output')
    def test_command_execution_agent(self, mock_subprocess):
        # Mock the subprocess output
        mock_subprocess.return_value = "total 0\ndrwxr-xr-x  2 user  staff   64 Sep 28 10:00 folder\n"

        # Test the chatbot response when asking to list files
        user_input = "Can you list files?"
        response = self.chatbot.orchestrate(user_input)
        expected_response = f"Command output:\n{mock_subprocess.return_value}"
        self.assertEqual(response, expected_response)

    @patch('agents.news_agent.fetch_latest_paphos_news')
    def test_news_agent(self, mock_fetch_news):
        # Mock the news fetching function
        mock_fetch_news.return_value = "- [Paphos News 1](http://example.com/news1)\n- [Paphos News 2](http://example.com/news2)"

        # Test the chatbot response when asking for latest news
        user_input = "What's the latest news from Paphos?"
        response = self.chatbot.orchestrate(user_input)
        expected_response = mock_fetch_news.return_value
        self.assertEqual(response, expected_response)

    @patch('agents.web_search_agent.get_duckduckgo_links')
    def test_web_search_agent(self, mock_get_links):
        # Mock the web search function
        mock_get_links.return_value = "- [Result 1](http://example.com/result1)\n- [Result 2](http://example.com/result2)"

        # Test the chatbot response when asking to search
        user_input = "Search for best restaurants in Paphos"
        response = self.chatbot.orchestrate(user_input)
        expected_response = f"Here are some relevant links:\n{mock_get_links.return_value}"
        self.assertEqual(response, expected_response)

    def test_default_response(self):
        # Mock the LLM response for category extraction
        self.llm_mock.invoke.return_value.content = "historical_sites"

        # Mock the LLM response for the final answer
        def llm_invoke(messages):
            return MagicMock(content="Paphos is known for its historical sites such as the Tombs of the Kings.")

        self.llm_mock.invoke.side_effect = llm_invoke

        # Test the chatbot response for a general query
        user_input = "Tell me about the historical sites in Paphos."
        response = self.chatbot.orchestrate(user_input)
        expected_response = "Paphos is known for its historical sites such as the Tombs of the Kings."
        self.assertEqual(response, expected_response)

    def test_exit(self):
        # Capture the output
        with patch('builtins.print') as mock_print:
            self.chatbot.respond_to_user('exit')
            mock_print.assert_any_call("Bot: Goodbye!")

if __name__ == '__main__':
    unittest.main()