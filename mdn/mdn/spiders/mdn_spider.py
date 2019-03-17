from loguru import logger
import scrapy
from w3lib.html import remove_tags


class MDNSpider(scrapy.Spider):

    name = 'mdn_spider'
    selector = '#Keyword_index + .blockIndicator + div code'

    def start_requests(self):

        logger.debug('making request')
        urls = ['https://developer.mozilla.org/en-US/docs/Web/CSS/Reference']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        logger.debug('parsing request')
        css_kw = response.css(self.selector)
        for kw in css_kw:
            clean_kw = remove_tags(kw.extract())
            logger.debug('css kw {}', clean_kw)
