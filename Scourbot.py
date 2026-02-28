import requests
from bs4 import BeautifulSoup
import time

def google_search(query):
    # This searches for the top 10 non-sponsored results
    headers = {'User-Agent': 'Mozilla/5.0'}
    search_url = f"https://www.google.com/search?q={query}+specs+archive"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = []
    for g in soup.find_all('div', class_='tF2Cxc'):
        link = g.find('a')['href']
        if "google.com" not in link:
            links.append(link)
    return links[:5]

def scour_bike_specs(bike_name):
    print(f"--- Starting autonomous search for: {bike_name} ---")
    potential_sites = google_search(bike_name)
    
    for site in potential_sites:
        print(f"Checking: {site}")
        try:
            res = requests.get(site, timeout=10)
            page_soup = BeautifulSoup(res.text, 'html.parser')
            
            # Logic to find Frame Material, Weight, and Top Tube
            # This looks for common keywords in table cells or list items
            data = {}
            for tag in page_soup.find_all(['td', 'li', 'p']):
                text = tag.get_text().lower()
                if "material" in text or "chromoly" in text:
                    data['Material'] = tag.get_text().strip()
                if "weight" in text or "lbs" in text:
                    data['Weight'] = tag.get_text().strip()
                if "top tube" in text or "tt" in text:
                    data['Top Tube'] = tag.get_text().strip()
            
            if data:
                print(f"Found Data: {data}")
                return data # Stops once it finds a good source
        except Exception as e:
            continue
    
    print("No specific specs found in top results.")
    return None

# List of frames from your app to check
bikes_to_scour = ["Haro Sport 1987", "Ozone Damage", "Haro Master 1986"]

for bike in bikes_to_scour:
    specs = scour_bike_specs(bike)
    time.sleep(2) # To avoid being blocked by search engines
