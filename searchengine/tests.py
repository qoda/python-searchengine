#!/usr/bin/env python

import os
import time
import unittest
import urllib

from main import SearchEngine, searchengine
from scraper import HTMLScraper, TagSelector
from search import SearchIndex

class MainTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_search_engine(self):
        pass
    
    def tearDown(self):
        pass

class ScraperTestCase(unittest.TestCase):
    def setUp(self):
        self.html = """
            <html>
            <head>
                <title>title</title>
            </head>
            <body>
                <div>div<a href="http://www.google.com">link</a></div>
            </body>
            </html>
        """
        self.url = "http://www.google.com"
        self.selector = TagSelector()
        self.scraper = HTMLScraper(url=self.url)
        
    def test_attr_dict(self):
        self.assertEqual(self.selector.attr_dict([]), {})
        self.assertEqual(self.selector.attr_dict([('class', 'test_class')]), {'class': 'test_class'})
    
    def test_tag_selector_handle_starttag(self):
        current_tag = "div"
        current_attrs = [('class', 'test_class')]
        self.selector.handle_starttag(current_tag, current_attrs)
        
        # test the current attrs and tag has been set correctly
        self.assertEqual(self.selector.current_tag, current_tag)
        self.assertEqual(self.selector.current_attrs, self.selector.attr_dict(current_attrs))
        
    def test_tag_selector_get_data(self):
        self.selector.feed(self.html)
        data = self.selector.get_data()
        self.assertEqual(data, {'content': ['title', 'div', 'link'], 'links': [('link', 'http://www.google.com')], 'title': 'title'})
    
    def test_html_scraper_get_url_content(self):
        self.assertNotEqual(self.scraper.get_url_content(), "")
        
    def test_html_scraper_get_content(self):
        content = self.scraper.get_content()
        self.assertNotEqual(content, {})
        self.assertTrue("Google" in content['content'])
        self.assertTrue("Google" in content['title'])
    
    def tearDown(self):
        pass
        
class SearchIndex(object):
    def setUp(self):
        pass
    
    def test_add(self):
        pass
    
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
