import time
import sys
import urllib.robotparser
import requests
from bs4 import BeautifulSoup

def check_robots_txt(url, user_agent="*"):
    """
    Checks robots.txt for the target URL to see if scraping is allowed.
    """
    parsed_url = urllib.parse.urlparse(url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    
    print(f"Fetching robots.txt from: {robots_url}")
    rp = urllib.robotparser.RobotFileParser()
    try:
        # Use requests with a timeout to avoid hanging
        response = requests.get(robots_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        if response.status_code == 404:
            print("robots.txt not found. Proceeding with caution...")
            return True
        elif response.status_code == 403:
            print("Access to robots.txt forbidden. Skipping scraping...")
            return False
            
        rp.parse(response.text.splitlines())
        allowed = rp.can_fetch(user_agent, url)
        return allowed
    except Exception as e:
        print(f"Error checking robots.txt: {e}")
        return False

def scrape_listings():
    # We will attempt to scrape a directory-like search page.
    # Target directory search url: YellowPages Mumbai Restaurants (or similar sandbox)
    target_url = "https://www.yellowpages.com/search?search_terms=restaurants&geo_location_terms=Mumbai"
    
    # Check robots.txt
    allowed = check_robots_txt(target_url)
    
    if not allowed:
        print("\n[CRITICAL SAFETY CHECK]")
        print(f"Target directory '{target_url}' disallows scraping or is inaccessible according to robots.txt rules.")
        print("Skipping scraping to comply with Terms of Service and safety guidelines.")
        print("Scraper execution halted gracefully.")
        sys.exit(0)
        
    print(f"Scraping is allowed. Fetching page: {target_url}")
    
    # Proof of concept scraping logic if allowed
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(target_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch listings page. HTTP Status Code: {response.status_code}")
            return
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Select business cards (using yellowpages class mapping as an example)
        # Note: In real-world targets, these selectors must match the HTML structure.
        cards = soup.select('.search-results .result')
        
        listings = []
        count = min(len(cards), 15) # Target 10-15 listings
        
        print(f"Found {len(cards)} potential listings. Extracting up to {count} entries...")
        
        for i in range(count):
            card = cards[i]
            
            # Extract fields with safe defaults
            name_el = card.select_one('.business-name')
            category_el = card.select_one('.categories')
            city_el = card.select_one('.locality')
            address_el = card.select_one('.street-address')
            phone_el = card.select_one('.phone')
            
            name = name_el.get_text(strip=True) if name_el else "Unknown Business"
            category = category_el.get_text(strip=True) if category_el else "General"
            city = city_el.get_text(strip=True).replace(",", "").strip() if city_el else "Mumbai"
            address = address_el.get_text(strip=True) if address_el else ""
            phone = phone_el.get_text(strip=True) if phone_el else ""
            
            listings.append({
                "business_name": name,
                "category": category,
                "city": city,
                "address": address,
                "phone": phone,
                "source": "YellowPages (Scraped)"
            })
            
            print(f"Scraped: {name} in {city}")
            # Respectful delay between requests if paging or loading detail page
            time.sleep(1.5)
            
        print(f"\nSuccessfully scraped {len(listings)} listings.")
        
    except Exception as e:
        print(f"An error occurred during scraping: {e}")

if __name__ == "__main__":
    scrape_listings()
