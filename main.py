# main.py

import os
import json
from langchain_community.chat_models.gigachat import GigaChat
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from dotenv import load_dotenv
from typing import List, Dict
from pydantic import BaseModel, Field

# Import agents
from agents.sea_water_temperature_agent import SeaWaterTemperatureAgent
from agents.weather_agent import WeatherAgent
from agents.system_time_agent import SystemTimeAgent
from agents.command_execution_agent import CommandExecutionAgent
from agents.news_agent import NewsAgent
from agents.web_search_agent import WebSearchAgent

# Load environment variables
load_dotenv('.env')

class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """In-memory implementation of chat message history."""
    messages: List[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Add a list of messages to the store."""
        self.messages.extend(messages)

    def clear(self) -> None:
        """Clear the message history."""
        self.messages = []

# Global store for chat histories
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]

class Chatbot:
    def __init__(self, llm, session_id='default_session'):
        self.llm = llm
        self.session_id = session_id

        # Define the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ])

        # Create the chain
        self.chain = self.prompt | self.llm

        # Wrap the chain with message history management
        self.conversation_chain = RunnableWithMessageHistory(
            self.chain,
            get_session_history=get_session_history,
            input_messages_key="question",
            history_messages_key="history",
        )

        # Load data.json
        data_path = os.path.join('data', 'data.json')
        with open(data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        # Initialize agents
        self.agents: Dict[str, Agent] = {
            'sea_water_temperature': SeaWaterTemperatureAgent(),
            'weather': WeatherAgent(self.llm),
            'system_time': SystemTimeAgent(),
            'command_execution': CommandExecutionAgent(),
            'news': NewsAgent(),
            'web_search': WebSearchAgent(),
            # Additional agents can be added here
        }

    def display_welcome_message(self):
        print("Welcome to the Paphos City Information Bot! Type 'exit' to quit.")

    def get_user_input(self):
        return input("You: ")

    def respond_to_user(self, user_input):
        if user_input.lower() == 'exit':
            print("Bot: Goodbye!")
            return

        # Orchestrate the response
        response = self.orchestrate(user_input)
        print(f"Bot: {response}")

    def orchestrate(self, user_input):
        # Simple keyword matching to decide which agent to use
        user_input_lower = user_input.lower()

        if any(keyword in user_input_lower for keyword in ['sea water temperature', 'water temperature', 'sea temperature', 'water temp']):
            response = self.agents['sea_water_temperature'].handle(user_input)
            return response
        elif any(keyword in user_input_lower for keyword in ['weather', 'temperature outside', 'forecast']):
            response = self.agents['weather'].handle(user_input)
            return response
        elif any(keyword in user_input_lower for keyword in ['what time is it', 'current time', 'system time']):
            response = self.agents['system_time'].handle(user_input)
            return response
        elif any(keyword in user_input_lower for keyword in ['execute command', 'run command', 'list files', 'disk usage', 'current directory']):
            response = self.agents['command_execution'].handle(user_input)
            return response
        elif any(keyword in user_input_lower for keyword in ['latest news', 'news from paphos', 'paphos news']):
            response = self.agents['news'].handle(user_input)
            return response
        elif any(keyword in user_input_lower for keyword in ['search', 'find', 'look up']):
            response = self.agents['web_search'].handle(user_input)
            return response
        else:
            # Proceed with the default behavior
            return self.default_response(user_input)

    def default_response(self, user_input):
        # Get relevant info from data.json
        relevant_info = self.get_relevant_info(user_input)

        # Build prompt for LLM
        prompt = f"{relevant_info}\nPlease provide a concise answer to the user's question without additional commentary."

        # Get response from LLM
        response = self._respond(prompt)
        return response

    def _respond(self, prompt):
        try:
            # Invoking the chain and ensuring we extract only the content
            response = self.conversation_chain.invoke(
                {"question": prompt},
                config={"configurable": {"session_id": self.session_id}}
            )

            if isinstance(response, dict):
                return response.get('content', "Sorry, I couldn't process your request.")
            return str(response.content)
        except Exception as e:
            return f"Sorry, I couldn't process your request due to an error: {e}"

    def get_relevant_info(self, user_input):
        # Define a strict prompt for the LLM to identify relevant categories
        agent_prompt = (
            f"Given the user query '{user_input}', identify which of the following categories are relevant:\n"
            "historical_sites, popular_spots, cultural_events, natural_wonders, museums, "
            "weather_facts, transportation, food_specialties, fun_facts.\n\n"
            "Respond only with the exact category names separated by commas if relevant (e.g., 'historical_sites, museums'). "
            "If none are relevant, respond with 'No'."
        )

        # Construct the message for the LLM
        messages = [
            {"role": "system", "content": "You are an assistant that extracts relevant categories from a user query."},
            {"role": "user", "content": agent_prompt}
        ]

        # Invoke the LLM agent to identify relevant categories
        agent_response = self.llm.invoke(messages)
        response_text = agent_response.content.strip().lower()

        if response_text == "no":
            return ""

        # Parse categories identified by the agent and retrieve matching data
        relevant_categories = [category.strip() for category in response_text.split(",")]

        # Retrieve and format data from relevant categories in data.json
        relevant_info = ""
        for category in relevant_categories:
            if category in self.data:
                relevant_info += self._format_data_items(category, self.data[category])
        return relevant_info

    def _format_data_items(self, category, data_items):
        formatted_info = ""
        if isinstance(data_items, list):
            for item in data_items:
                if isinstance(item, dict):
                    name = item.get('name', '')
                    description = item.get('description', '')
                    formatted_info += f"{name}: {description}\n"
                else:
                    formatted_info += f"{item}\n"
        elif isinstance(data_items, dict):
            for key, value in data_items.items():
                formatted_info += f"{key}: {value}\n"
        elif isinstance(data_items, str):
            formatted_info += f"{category}: {data_items}\n"
        return formatted_info

    def print_memory(self):
        history = store.get(self.session_id)
        if history:
            print("Conversation History:")
            for message in history.messages:
                print(f"{message.type.capitalize()}: {message.content}")

if __name__ == "__main__":
    giga_key = os.environ.get("SB_AUTH_DATA")
    if giga_key is None:
        print("Please set the SB_AUTH_DATA environment variable.")
    else:
        giga = GigaChat(
            credentials=giga_key,
            model="GigaChat",
            timeout=30,
            verify_ssl_certs=False
        )
        chatbot = Chatbot(giga)
        chatbot.display_welcome_message()
        while True:
            user_input = chatbot.get_user_input()
            chatbot.respond_to_user(user_input)
            if user_input.lower() == 'exit':
                break
        chatbot.print_memory()