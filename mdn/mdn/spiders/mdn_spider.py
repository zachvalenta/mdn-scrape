import scrapy
from w3lib.html import remove_tags


class MDNSPider(scrapy.Spider):

    name = 'mdn_spider'

    def start_requests(self):

        urls = ['https://developer.mozilla.org/en-US/docs/Web/CSS/Reference']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = response.css('#Keyword_index + .blockIndicator + div code')
        for item in items:
            print(remove_tags(item.extract()))
