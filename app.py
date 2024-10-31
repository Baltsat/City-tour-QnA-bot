import streamlit as st
from main import Chatbot
from agents.news_agent import NewsAgent
from utils.get_rss import fetch_latest_paphos_news
from langchain_community.chat_models.gigachat import GigaChat
import os
import json
from datetime import datetime, timedelta

def main():
    st.set_page_config(page_title="Paphos City Information Bot", page_icon="🌴", initial_sidebar_state="collapsed")

    st.title("🌴 Paphos City Information Bot")

    # Retrieve API keys from Streamlit secrets
    giga_key = st.secrets.get("GIGACHAT_API_KEY", "")
    openweather_key = st.secrets.get("OPENWEATHER_API_KEY", "")

    # Sidebar for optional user-provided API keys
    with st.sidebar:
        st.title("Configuration")
        user_giga_key = st.text_input("Enter your GigaChat API Key (optional)", type="password")
        user_openweather_key = st.text_input("Enter your OpenWeather API Key (optional)", type="password")

    # Use user-provided keys if available
    if user_giga_key:
        giga_key = user_giga_key
    if user_openweather_key:
        openweather_key = user_openweather_key

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

    # Countdown to AI Paphos Summit
    summit_date = datetime(2024, 11, 15, 0, 0, 0)
    now = datetime.now()
    countdown = summit_date - now
    days, seconds = countdown.days, countdown.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    st.sidebar.markdown(f"🕒 Countdown to AI Paphos Summit: {days}d {hours}h {minutes}m {seconds}s")

    # Credits
    st.markdown(
        """
        <style>
            .credits {
                position: fixed;
                bottom: 5px;
                left: 5px;
                font-size: 0.8em;
                color: #6c757d;
                font-family: 'Courier New', monospace;
            }
        </style>
        <div class="credits">Credits to Konstantin BALTSAT</div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()