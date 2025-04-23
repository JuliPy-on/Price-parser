import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from pathlib import Path
from typing import List, Dict, Optional
import time


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("parser.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


CONFIG = {
    "base_url": "https://webscraper.io/test-sites/e-commerce/static/computers",
    "headers": {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    },
    "max_pages": 3,  
    "timeout": 10,   
    "output_file": "products.csv"
}

class PriceParser:
    def __init__(self, config: Dict):
        self.base_url = config["base_url"]
        self.headers = config["headers"]
        self.max_pages = config["max_pages"]
        self.timeout = config["timeout"]
        self.output_file = Path(config["output_file"])
        self.session = requests.Session()

    def fetch_page(self, url: str) -> Optional[str]:
        """Fetches the HTML code of the page with error handling."""
        try:
            response = self.session.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            logger.info(f"Page successfully retrieved: {url}")
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error while fetching the page {url}: {str(e)}")
            return None

    def parse_items(self, soup: BeautifulSoup) -> List[Dict]:
        """Parses products on a single page."""
        items = []
        
        active_category = soup.find("a", class_=["category-link", "active"])
        category_name = active_category.text.strip() if active_category else "Неизвестно"

        products = soup.find_all("div", class_="thumbnail")

        for product in products:
            try:
                name = product.find("a", class_="title").text.strip()
                price = product.find("h4", class_="price").text.strip()
                link = product.find("a", class_="title")["href"]
                full_link = f"https://webscraper.io{link}" if link.startswith("/") else link

                items.append({
                    "Titple": name,
                    "Price": price,
                    "Category": category_name,
                    "Link": full_link
                })
            except AttributeError as e:
                logger.warning(f"Product parsing error: {str(e)}")
                continue

        return items

    def save_to_csv(self, items: List[Dict]) -> None:
        """Saves data to a CSV file."""
        if not items:
            logger.warning("No data to save.")
            return

        df = pd.DataFrame(items)
        df.to_csv(self.output_file, index=False, encoding="utf-8")
        logger.info(f"Data saved with {self.output_file}: {len(items)} entries")

    def run(self) -> None:
        """Main method to start parsing."""
        logger.info("Starting the price parser...")
        all_items = []

        
        html = self.fetch_page(self.base_url)
        if not html:
            logger.error("Failed to retrieve the first page. Terminating process.")
            return

        soup = BeautifulSoup(html, "html.parser")
        items = self.parse_items(soup)
        all_items.extend(items)

        
        page = 1
        while page < self.max_pages:
            page += 1
            next_url = f"{self.base_url}?page={page}"
            logger.info(f"Parsing page {page}: {next_url}")
            html = self.fetch_page(next_url)
            if not html:
                break

            soup = BeautifulSoup(html, "html.parser")
            items = self.parse_items(soup)
            if not items:  
                break
            all_items.extend(items)
            time.sleep(1)  

        self.save_to_csv(all_items)

def main():
    try:
        parser = PriceParser(CONFIG)
        parser.run()
    except Exception as e:
        logger.critical(f"Critical error: {str(e)}")
        raise

if __name__ == "__main__":
    main()