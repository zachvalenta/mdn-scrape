import json
import os
import re

from algoliasearch import algoliasearch
from dotenv import find_dotenv, load_dotenv
from loguru import logger
import scrapy
from w3lib.html import remove_tags


def get_algolia_client():
    load_dotenv(find_dotenv())
    app_id = os.getenv('APP_ID')
    api_key_admin = os.getenv('API_KEY_ADMIN')
    return algoliasearch.Client(app_id, api_key_admin)


def push_to_algolia():
    client = get_algolia_client()
    index = client.init_index('css')
    index.add_objects(json.load(open('data.json')))


class MDNSpider(scrapy.Spider):

    all_kw = list()
    mdn_base_url = 'https://developer.mozilla.org/en-US/docs/Web/CSS'
    name = 'mdn_spider'
    selector = '#Keyword_index + .blockIndicator + div a'
    strip_from_link = '/en-US/docs/Web/CSS'

    def start_requests(self):
        logger.debug('making request')
        urls = ['https://developer.mozilla.org/en-US/docs/Web/CSS/Reference']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        logger.debug('parsing request')
        els = response.css(self.selector)
        for el in els:
            text_dirty = el.extract()
            text = remove_tags(text_dirty)
            link_dirty = re.findall(r'\"(.+?)\"', remove_tags(text_dirty, keep='a'))
            link = self.mdn_base_url + link_dirty[0].replace(self.strip_from_link, '')
            self.all_kw.append(dict(link=link, text=text))
        logger.debug('writing data to disk')
        with open('data.json', 'w') as f:
            f.write(json.dumps(self.all_kw, indent=4))
        logger.debug('writing data to algolia')
        push_to_algolia()
