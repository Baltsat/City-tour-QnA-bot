# app.py

import streamlit as st
from main import Chatbot
from agents.news_agent import NewsAgent
from utils.get_rss import fetch_latest_paphos_news
from langchain_community.chat_models.gigachat import GigaChat  # Import GigaChat
import os
import json  # Import json

def main():
    st.set_page_config(page_title="Paphos City Information Bot", page_icon="🌴")

    st.title("🌴 Paphos City Information Bot")

    # Sidebar for API keys
    st.sidebar.title("Configuration")
    giga_key = st.sidebar.text_input("Enter your GigaChat API Key", type="password")
    openweather_key = st.sidebar.text_input("Enter your OpenWeather API Key", type="password")

    if giga_key and openweather_key:
        os.environ['SB_AUTH_DATA'] = giga_key
        os.environ['OPENWEATHER_API_KEY'] = openweather_key

        # Initialize the chatbot
        giga = GigaChat(
            credentials=giga_key,
            model="GigaChat",
            timeout=30,
            verify_ssl_certs=False
        )
        chatbot = Chatbot(giga)

        # Display sample template requests
        st.subheader("Sample Questions")
        sample_questions = [
            "What are the main attractions in Paphos?",
            "Tell me about the historical sites.",
            "What's the current weather?",
            "Show me the latest news from Paphos.",
            "What time is it?",
            "What's the current sea water temperature?"
        ]
        for question in sample_questions:
            if st.button(question):
                response = chatbot.orchestrate(question)
                st.write(f"**You:** {question}")
                st.write(f"**Bot:** {response}")

        # Chat interface
        st.subheader("Chat with the Bot")
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

        user_input = st.text_input("You:", key="user_input")
        if st.button("Send"):
            if user_input:
                response = chatbot.orchestrate(user_input)
                st.session_state.chat_history.append(("You", user_input))
                st.session_state.chat_history.append(("Bot", response))

        # Display chat history
        for sender, message in st.session_state.chat_history:
            st.write(f"**{sender}:** {message}")

        # Display latest news
        st.subheader("📰 Latest News from Paphos")
        news_agent = NewsAgent()
        news = news_agent.handle("latest news")
        st.write(news)

        # Display interesting facts
        st.subheader("🌟 Interesting Facts")
        with open(os.path.join('data', 'data.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)
            fun_facts = data.get('fun_facts', [])
            for fact in fun_facts:
                st.write(f"- {fact}")

        # Display places to go
        st.subheader("🏖️ Places to Go")
        popular_spots = data.get('popular_spots', [])
        for spot in popular_spots:
            st.write(f"**{spot['name']}**: {spot['description']}")

    else:
        st.info("Please enter your API keys to start using the bot.")

if __name__ == "__main__":
    main()