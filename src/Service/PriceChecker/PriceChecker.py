import re
import validators
import logging
import json

from src.Entity.Part import Part
from typing import List, Dict, Union
from src.Service.WebScraper.WebScraper import WebScraper


class PriceChecker:
    """
    Scrapes the price for the product page.
    """

    def __init__(self, parts_list: Dict[str, Union[str, float]], logger: logging, web_scraper: WebScraper):
        self.parts_list = parts_list
        self.logger = logger
        self.web_scraper = web_scraper

    def check_prices(self) -> Union[List[Part], None]:
        """
        Creates a collection of parts.

        Returns:
            Union[List[Part], None]: Collection of parts or None.
        """

        if not self.parts_list:
            return None

        parts = []
        name = self.parts_list['name']
        suppliers = self.parts_list['suppliers']
        type = self.parts_list['type']

        if not suppliers or not name:
            return None

        for supplier in suppliers:  # type: Dict[str, Union[str, float]]
            element_html = ''
            cost = []

            url = supplier['url']
            element = supplier['element']
            supplier_name = supplier['name']

            if not element or (not url and not validators.url(url)):
                continue

            try:
                content = self.web_scraper.scrape_page(url, element)
                self.logger.info("Trying to open a page with url: " + url)
            except Exception as e:
                self.logger.error("Exception occurred while trying to parse page: {0}".format(e))
                continue

            if content:
                element_html = content.text.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r\n", "").replace("\r", "")

            if element_html:
                cost = re.findall(r'[\d\.\d]+', element_html)

            if cost and isinstance(cost, list):
                part = Part(name, ''.join(cost), supplier_name, type)
                parts.append(part)
                self.logger.info("Creating part object: {0}".format(json.dumps(part.__dict__)))

        return parts
