[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/JcjKEa_w)


**Task Description:**

**Overview:**

You are required to implement the simplest text-based chatbot using OpenAI tools and models to provide information about Paphos city. This bot should combine general information from the LLM model (like GPT-4о-mini or Llama 3.1 or any other) with facts and extra context provided in the file `data.json`.

**Additional Requirements:**

1. **Internet Search for Links:**
   - The bot should be able to search for relevant links on the internet related to the user's query about Paphos and provide them in the response.
   - Use an appropriate web search API (e.g., Bing Search API or any other) to fetch the latest and most relevant links.

2. **Fetching Latest News from Paphos News Site:**
   - The bot should fetch and display the latest news headlines from a Paphos news website.
   - Use web scraping or RSS feeds to obtain the latest news.
   - Ensure compliance with the website's terms of service when accessing their content.

3. **Current Sea Water Temperature in Paphos:**
   - The bot should report the current sea water temperature in Paphos.
   - Use an appropriate API or data source to obtain the current sea water temperature.

4. **System Time Reporting:**
   - The bot should be able to report the current system time when asked by the user.

**Requirements:**

- **Chatbot Implementation:**
  - Develop a text-based chatbot that interacts with the user through the console or a web interface.
  - The bot should accept user queries and generate meaningful responses by combining general knowledge and data from `data.json`.

- **Integration of `data.json`:**
  - Load and process data from the `data.json` file.
  - Ensure that the bot utilizes information from this file to provide accurate facts about Paphos.

- **Internet Search Functionality:**
  - Implement a function that performs internet searches based on the user's query.
  - Provide no more than three relevant and up-to-date links in the response.
  - Use a search API like Bing Search API or Google Custom Search API.

- **Fetching Latest News:**
  - Implement functionality to fetch the latest news from a Paphos news website.
  - You can use RSS feeds or web scraping tools like BeautifulSoup.
  - Present the news headlines or summaries in the bot's responses.

- **Sea Water Temperature:**
  - Use a suitable API or data source to get the current sea water temperature in Paphos.
  - Integrate this data into the bot's responses when requested by the user.

- **System Time Reporting:**
  - The bot should be able to provide the current system time upon the user's request.

- **Execution of Command-Line Tools:**
  - Define a list of allowed commands that the bot can execute.
  - Use the `subprocess` module in Python to safely execute these commands.
  - Prevent execution of arbitrary or unsafe commands.

**Example Interaction:**

```
Welcome to the Paphos City Information Bot! Type 'exit' to quit.

User: What are the main attractions in Paphos?

Bot: Paphos is renowned for its ancient historical sites like the Tombs of the Kings and the beautiful mosaics in the House of Dionysus. Here are some links you might find helpful:
- [Paphos Archaeological Park](https://www.visitpafos.org.cy/archaeological_park)
- [Top Attractions in Paphos](https://www.example.com/paphos-attractions)
- [UNESCO Sites in Paphos](https://www.example.com/unesco-paphos)

Also, here are the latest news from Paphos:
- "Paphos hosts annual cultural festival."
- "New archaeological discoveries unveiled in Paphos."
- "Paphos beaches receive Blue Flag awards."

User: What's the current sea water temperature?

Bot: The current sea water temperature in Paphos is 24°C.

User: What time is it?

Bot: The current system time is 15:42.

User: exit

Bot: Goodbye!
```
