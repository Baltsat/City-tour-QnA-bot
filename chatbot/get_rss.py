import requests
from bs4 import BeautifulSoup

def fetch_latest_paphos_news(url, count=5):
    """
    Fetches and displays the latest news headlines from Paphos Life.

    Parameters:
    - url (str): The URL of the Paphos Life news page.
    - count (int): The number of latest news items to display.

    Returns:
    - str: A formatted string containing the latest news headlines with links.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the news articles
        news_items = []
        articles = soup.find_all('div', class_='pz-news', limit=count)
        for article in articles:
            # Extract title and link with error handling
            title_element = article.find('h3', class_='hover-effect')
            if title_element:
                title = title_element.get_text(strip=True)
                link = article.find('a')['href']
                news_items.append(f'- [{title}]({link})')

        # Check if news items were found
        if news_items:
            return "Here are the latest news from Paphos Life:\n" + "\n".join(news_items)
        else:
            return "No recent news found on the Paphos Life page."

    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"

# URL of the Paphos Life news page
url = "https://www.paphoslife.com/news"
if __name__ == "__main__":
    print(fetch_latest_paphos_news(url))