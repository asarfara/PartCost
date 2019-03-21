from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


class WebScraper:
    def scrape_page(self, url: str, element: str) -> str:
        """
        Scrapes the price from the page.

        Returns:
            str: Scraped price from the web.
        """

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
        }

        req = Request(url=url, headers=headers)

        page = urlopen(req)
        soup = BeautifulSoup(page, 'html.parser')
        return soup.select_one(element)
