import re
import validators
import logging
import json

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from src.Entity.Part import Part
from typing import List, Dict, Union


class PriceChecker:
    def __init__(self, parts_list: Dict[str, Union[str, float]], logger: logging):
        self.parts_list = parts_list
        self.logger = logger

    def check_prices(self) -> Union[List[Part], None]:
        if not self.parts_list:
            return None

        parts = []
        name = self.parts_list['name']
        suppliers = self.parts_list['suppliers']
        type = self.parts_list['type']

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
        }

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

            self.logger.info("Trying to open a page with url: " + url)
            req = Request(url=url, headers=headers)

            try:
                page = urlopen(req)
                soup = BeautifulSoup(page, 'html.parser')
                content = soup.select_one(element)
            except Exception as e:
                self.logger.error("Exception occurred while trying to parse page: {0}".format(e))
                continue

            if content:
                element_html = content.text.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r\n", "").replace("\r", "")

            if element_html:
                cost = re.findall(r'[\d\.\d]+', element_html)

            if cost and isinstance(cost, list):
                part = Part(name, cost[0], supplier_name, type)
                parts.append(part)
                self.logger.info("Creating part object: {0}".format(json.dumps(part.__dict__)))

        return parts
