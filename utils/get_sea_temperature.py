import requests
from bs4 import BeautifulSoup

def get_paphos_sea_temperature():
    url = "https://seatemperature.net/current/cyprus/paphos-pafos-cyprus-sea-temperature"
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the row for today's date with the current Paphos sea temperature
        today_row = soup.find('tr', class_='trfore2a')
        if today_row:
            today_temp_cell = today_row.find('td', id='ftd2')
            if today_temp_cell:
                today_temp = today_temp_cell.get_text(strip=True)
                return f"Today's sea temperature in Paphos is {today_temp}"
            else:
                return "Could not find today's sea temperature data for Paphos."
        else:
            return "Could not find today's row for Paphos temperature."
        
    except requests.RequestException as e:
        return f"Error fetching sea temperature data: {e}"
    except AttributeError as e:
        return f"Error parsing data: {e}"

if __name__ == "__main__":
    print(get_paphos_sea_temperature())