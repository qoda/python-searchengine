#!/usr/bin/env python

from HTMLParser import HTMLParser, HTMLParseError
import optparse
from urllib2 import urlopen, URLError

from searchengine.logger import Logging

class TagSelector(HTMLParser):
    """
    Strip all HTML tags from a string.
    """
    def __init__(self, *args, **kwargs):
        self.reset()
        self.content_dict = {
            'title': "",
            'content': [],
            'links': [],
        }
        self.current_tag = None
        self.current_attrs = None
        self.visible_tags = kwargs.get('visible_tags', [
            'body', 'title', 'p', 'div', 'td',
            'span', 'blockquote', 'li', 'a',
        ])
        
    def attr_dict(self, attrs):
        """
        Iterate through the attrs and convert to a dict.
        """
        attrs_dict = {}
        if attrs:
            for a in attrs:
                attrs_dict.update({a[0]: a[1]})
        return attrs_dict
        
    def handle_starttag(self, tag, attrs):
        """
        Set the current tag the parser has reached.
        TODO: add css support
        """
        self.current_tag = tag
        self.current_attrs = self.attr_dict(attrs)
    
    def handle_data(self, data):
        """
        Append visible data to the list.
        """
        data = data.strip()
        
        # find visible data and update to the content_dict
        if self.current_tag in self.visible_tags and data:
            if self.current_tag == 'title':
                self.content_dict['title'] = data
            if self.current_tag == 'a' and self.current_attrs.has_key('href'):
                link = self.current_attrs['href']
                self.content_dict['links'].append((data, link))
            self.content_dict['content'].append(data)
    
    def get_data(self):
        return self.content_dict

class HTMLScraper(object):
    """
    A simple HTML Scraper class to get visable text from a given URL.
    """
    def __init__(self, url, *args, **kwargs):
        self.log = kwargs.get('log', Logging())
        self.url = url
        
    def get_url_content(self):
        """
        Open and read the content of a URL.
        """
        try:
            url_handler = urlopen(self.url)
        except URLError, e:
            self.log.warning("HTMLScraper", "get_url_content", e)
            return ""
        
        html_content = url_handler.read()
        url_handler.close()
        
        return html_content
        
    def get_content(self):
        """
        Parse the visable content of a url into plain text.
        """
        html_content = self.get_url_content()
        html_parser = TagSelector()
        
        try:
            html_parser.feed(unicode(html_content, errors='replace'))
        except HTMLParseError, e:
            self.log.warning("HTMLScraper", "get_content", e)
            return {}
        
        # get the content and update with the url scraped
        parsed_content = html_parser.get_data()
        parsed_content.update({'url': self.url})
        
        return parsed_content
