import requests
from bs4 import BeautifulSoup

def get_paphos_sea_temperature(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the row for the current date (e.g., Oct 31) with Paphos temperature data
        today_row = soup.find('tr', class_='trfore2a')
        if not today_row:
            print("Could not find today's row for Paphos temperature.")
            return None
        
        # Extract the temperature from the relevant cell
        today_temp = today_row.find('td', id='ftd2').get_text(strip=True)
        
        return f"Today's sea temperature in Paphos is {today_temp}"
        
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
    except AttributeError as e:
        print(f"Error parsing data: {e}")

# Main entry point
if __name__ == "__main__":
    url = "https://seatemperature.net/current/cyprus/paphos-pafos-cyprus-sea-temperature"
    print(get_paphos_sea_temperature(url))