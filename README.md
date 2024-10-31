# 🌴 Paphos City Information Bot

Welcome to the **Paphos City Information Bot**! Whether you're a tourist planning to visit or a local resident, our bot offers a friendly and intuitive way to learn more about the beautiful city of Paphos. Explore attractions, get weather updates, check the latest news, and much more!

## 🚀 Key Strengths

- **Comprehensive Information**: Get a wealth of information about Paphos, including attractions, latest news, weather, and much more, all in one place.
- **Real-Time Updates**: Stay current with live news headlines, accurate weather, and sea water temperatures, ensuring you always have the latest information.
- **Seamless Interaction**: The bot's intuitive chat interface makes it easy for anyone to use—no technical knowledge required.
- **Integrated Knowledge Base**: Combines general language model knowledge with curated local data from `data.json` to provide well-rounded, accurate answers.
- **Link Recommendations**: Offers relevant, useful links related to Paphos attractions and events to enhance your experience.

## 🛠️ Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/yourusername/jass-ai-admission-Baltsat.git
    ```
2. Перейдите в директорию проекта:
    ```bash
    cd jass-ai-admission-Baltsat
    ```
3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

## Запуск

Для запуска бота выполните следующую команду:
```bash
python main.py
```

### **Using the Bot**

- Open the provided local URL from Streamlit in your browser.
- Start chatting! You can ask questions like "What's the current weather in Paphos?", "Tell me about the main attractions", or "What's the latest news?".

### **Sample Interaction**

```
User: What are the main attractions in Paphos?

Bot: Paphos is renowned for its ancient historical sites like the Tombs of the Kings and the beautiful mosaics in the House of Dionysus. Here are some links you might find helpful:
- [Paphos Archaeological Park](https://www.visitpafos.org.cy/archaeological_park)
- [Top Attractions in Paphos](https://www.example.com/paphos-attractions)

Also, here are the latest news from Paphos:
- "Paphos hosts annual cultural festival."
- "New archaeological discoveries unveiled in Paphos."

User: What's the current sea water temperature?

Bot: The current sea water temperature in Paphos is 24°C.

User: What time is it?

Bot: The current system time is 15:42.

User: Can you execute a command to show the current directory?

Bot: Here is the result of the command:
/home/user/project-directory
```

## 🧪 Тестирование

Для запуска тестов выполните:
```bash
pytest
```

## 🌐 Deployment

### **Deploy on Streamlit Cloud**

1. **Push the project to GitHub**.
2. **Sign up** on [Streamlit Cloud](https://streamlit.io/cloud).
3. **Create a new app** and connect your GitHub repository.
4. **Set `app.py`** as the entry point.
5. **Configure environment variables** in the app settings.
6. **Deploy and share** your app with the world!

## 🌟 Original Features & Usage Examples

- **Internet Search for Links**: The bot can perform real-time web searches to recommend relevant links about Paphos, using services like Bing or Google Custom Search.
- **Fetching Latest News from Paphos**: The bot fetches live news headlines from Paphos using RSS feeds or scraping techniques, providing fresh updates whenever you ask.
- **Sea Water Temperature**: Get the current sea water temperature in Paphos using integrated weather APIs.
- **Command-Line Tool Execution**: Safely execute specific command-line tools through the bot to access utility information such as directory listings or disk usage.

##