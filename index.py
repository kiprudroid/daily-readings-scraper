import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import time

# Get current date and end of year
current_date = datetime.now()
end_of_year = datetime(current_date.year, 10, 30)
all_readings = []

# Loop through dates until end of year
while current_date <= end_of_year:
    formatted_date = current_date.strftime("%m%d%y")
    url = f"https://bible.usccb.org/bible/readings/{formatted_date}.cfm"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract readings
        title = soup.find_all("h2")[3].get_text(strip=True)
        readings = [p.get_text(strip=True) for p in soup.find_all("p")[2:-4]]

        # Create daily entry
        daily_data = {
            "date": current_date.strftime("%Y-%m-%d"),
            "title": title,
            "readings": readings
        }
        all_readings.append(daily_data)
        
        # Add delay to be respectful to the server
        time.sleep(2)
        
    except Exception as e:
        print(f"Error scraping {formatted_date}: {str(e)}")
    
    current_date += timedelta(days=1)

# Save all readings to JSON file
with open("readings.json", "w", encoding="utf-8") as f:
    json.dump(all_readings, f, ensure_ascii=False, indent=2)
