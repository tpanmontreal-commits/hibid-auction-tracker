import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def scrape_hibid_auctions():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    target_url = "https://hibid.com/catalog/790832/furniture--home-goods-and-reseller-finds---ssn258"
    
    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        
        scraped_data = {
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "seller": "Chill Mart",
            "category": "Furniture & Home Goods",
            "target_url": target_url,
            "items": []
        }
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 抓取页面上的商品节点
            for card in soup.find_all(['div', 'tr'], class_=['item-card', 'catalog-item', 'lot-row']):
                title_node = card.find(['h3', 'a', 'div'], class_=['title', 'lot-title', 'item-title'])
                price_node = card.find(['span', 'div'], class_=['price', 'current-bid', 'bid-amount'])
                
                if title_node:
                    item_name = title_node.get_text(strip=True)
                    item_price = price_node.get_text(strip=True) if price_node else "N/A"
                    
                    scraped_data["items"].append({
                        "product_name": item_name,
                        "final_price": item_price
                    })
                    
            scraped_data["total_items"] = len(scraped_data["items"])
            scraped_data["success"] = True
        else:
            scraped_data["success"] = False
            scraped_data["error"] = f"HTTP {response.status_code}"

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
