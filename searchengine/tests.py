#!/usr/bin/env python

import os
import time
import unittest
import urllib

from main import SearchEngine, searchengine
from scraper import HTMLScraper, TagSelector
from search import SearchIndex

def dummy_search_index():
    search_index = SearchIndex(
        index_path="index_test",
        log=Logging(log_file_name="test.log"),
    )
    search_index.add(
        date= time.strptime("1 Jan 11", "%d %b %y"),
        title='Testing ABC',
        url='http://www.google.com',
        feed='http://www.google.com',
        commit=True,
    )
    search_index.add(
        date= time.strptime("1 Jan 11", "%d %b %y"),
        title='Testing DEF',
        url='http://www.google2.com',
        feed='http://www.google2.com',
        commit=True,
    )
    return search_index

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
        self.assertEqual(self.url, content['url'])
    
    def tearDown(self):
        pass

class SearchTestCase(unittest.TestCase):
    def setUp(self):
        self.search_index = dummy_search_index()
        
    def test_get(self):
        id = md5("http://www.google.com").hexdigest()
        result = self.search_index.get(id)
        
        # test that an obj is returned by id
        self.assertTrue(isinstance(result, dict))
        
        # test that only one obj is returned
        self.assertEqual(result['title'], "Testing ABC")
        
    def test_search(self):
        
        # test that the output is not empty
        results = self.search_index.search("ABC")
        self.assertTrue(len(results) > 0)
        self.assertTrue(len(results) <= 1)
        
        # test that the output is empty
        results = self.search_index.search("CBA")
        self.assertEqual(len(results), 0)
        
        # test that the output doesn't contain more than one result
        results = self.search_index.search("ABC")
        self.assertEqual(len(results), 1)
        
        # test that the output contains two results
        results = self.search_index.search("Testing")
        self.assertEqual(len(results), 2)
        
        # test that exclusions are ommit the correct results
        results = self.search_index.search("Testing -ABC")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], "Testing DEF")
        
    def tearDown(self):
        shutil.rmtree(self.search_index.index_path)
        self.search_index.close()

if __name__ == '__main__':
    unittest.main()
