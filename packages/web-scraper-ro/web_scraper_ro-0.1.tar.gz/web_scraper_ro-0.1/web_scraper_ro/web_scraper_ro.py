# web_scraper.py

import requests
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self, url):
        self.url = url

    def scrape(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            # Modify this part to extract the specific data you need from the webpage
            # For example, to scrape all the text within <p> tags:
            paragraphs = soup.find_all("p")
            scraped_data = [p.get_text() for p in paragraphs]
            return scraped_data
        except Exception as e:
            return str(e)


if __name__ == "__main__":
    url = input("Enter the URL you want to scrape: ")
    scraper = WebScraper(url)
    scraped_data = scraper.scrape()
    if isinstance(scraped_data, list):
        for item in scraped_data:
            print(item)
    else:
        print("An error occurred:", scraped_data)
