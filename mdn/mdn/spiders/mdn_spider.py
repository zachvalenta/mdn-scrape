import json
import os
import re

import bs4
from loguru import logger
import requests
import scrapy
from w3lib.html import remove_tags

from ..algolia_client import check_index_populated, push_to_index


def check_data_file_empty():
    return True if os.stat('data.json').st_size != 0 else False


def get_summary(link):
    # TODO: r&d Scrapy pipelines for this
    res = requests.get(link)
    if res.status_code != 200:
        return ''
    soup = bs4.BeautifulSoup(res.text, features="html.parser")
    try:
        return remove_tags(str(soup.select('#wikiArticle > p:first-of-type')[0]))
    except IndexError:
        return ''


class MDNSpider(scrapy.Spider):

    all_kw = list()
    mdn_base_url = 'https://developer.mozilla.org/en-US/docs/Web/CSS'
    name = 'mdn_spider'
    selector = '#Keyword_index + .blockIndicator + div a'
    strip_from_link = '/en-US/docs/Web/CSS'

    def start_requests(self):
        if check_index_populated():
            logger.debug('data already pushed to Algolia! ✅')
            return
        elif check_data_file_empty():
            logger.debug('data already scraped! ✅')
            push_to_index()
            return
        else:
            logger.debug('making request 🕷')
            urls = ['https://developer.mozilla.org/en-US/docs/Web/CSS/Reference']
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        logger.debug('parsing request 🕷')
        els = response.css(self.selector)
        for el in els:
            text_dirty = el.extract()
            text = remove_tags(text_dirty)
            link_dirty = re.findall(r'\"(.+?)\"', remove_tags(text_dirty, keep='a'))
            link = self.mdn_base_url + link_dirty[0].replace(self.strip_from_link, '')
            summary = get_summary(link=link)
            self.all_kw.append(dict(link=link, text=text, summary=summary))
        logger.debug('writing data to disk 💾')
        with open('data.json', 'w') as f:
            f.write(json.dumps(self.all_kw, indent=4))
        push_to_index()
