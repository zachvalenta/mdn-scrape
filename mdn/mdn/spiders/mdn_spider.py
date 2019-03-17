import json
import re

from loguru import logger
import scrapy
from w3lib.html import remove_tags


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
            el_dirty = el.extract()
            text = remove_tags(el_dirty)
            link_dirty = re.findall(r'\"(.+?)\"', remove_tags(el_dirty, keep='a'))
            link = self.mdn_base_url + link_dirty[0].replace(self.strip_from_link, '')
            self.all_kw.append(dict(link=link, text=text))
        data = open('data.json', 'w')
        data.write(json.dumps(self.all_kw, indent=4))
        data.close()
