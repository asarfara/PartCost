import unittest
from unittest.mock import patch, Mock

from src.Entity.Part import Part
from src.Service.PriceChecker.PriceChecker import PriceChecker


class PriceCheckerTest(unittest.TestCase):
    def test_collection_of_parts_returns_none_if_no_suppliers_are_found(self):

        mock_logger = Mock(name='logger')
        mock_web_scraper = Mock(name='WebScraper')

        parts_list = {
            'name': 'Test',
            'type': 'case'
        }

        price_checker = PriceChecker(parts_list, mock_logger, mock_web_scraper)
        self.assertEqual(price_checker.check_prices(), None, 'Suppliers should be in the collection')

    def test_collection_of_parts_created_correctly(self):

        mock_logger = Mock(name='logger')
        mock_web_scraper = Mock(name='WebScraper')
        mock_web_scraper.scrape_page.return_value = '$339.00'

        parts_list = {
            'name': 'Test',
            'type': 'case',
            'suppliers': [
                {
                    'name': 'Test Supplier 1',
                    'element': '.divPriceNormal div',
                    'url': 'https://test1.com'
                },
                {
                    'name': 'Test Supplier 2',
                    'element': '.divPriceNormal div',
                    'url': 'https://test2.com'
                }
            ]
        }

        price_checker = PriceChecker(parts_list, mock_logger, mock_web_scraper)
        parts = price_checker.check_prices()

        self.assertIsInstance(parts[0], Part, 'Instance of part should be returned')
        self.assertEqual(parts[0].name, 'Test')
        self.assertEqual(parts[0].price, '339.00')

if __name__ == '__main__':
    unittest.main()
