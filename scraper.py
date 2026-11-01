import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def scrape_hibid_auctions():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    
    target_url = "https://hibid.com/"
    
    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        
        scraped_data = {
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "target_url": target_url,
            "status_code": response.status_code,
            "auctions": []
        }
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            page_title = soup.title.string if soup.title else "No Title Found"
            scraped_data["page_title"] = page_title
            scraped_data["success"] = True
        else:
            scraped_data["success"] = False
            scraped_data["error"] = f"HTTP Error {response.status_code}"

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(scraped_data, f, ensure_ascii=False, indent=4)

    except Exception as e:
        error_data = {
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "success": False,
            "error": str(e)
        }
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(error_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scrape_hibid_auctions()
