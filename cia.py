import scrapy

class Spider(scrapy.Spider):

    name = "cia"
    start_urls =[
        'https://www.cia.gov/readingroom/historical-collections'
    ]
    custom_settings = {
        'FEED_URI': 'cia.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['carlosdamian05329@gmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'Caliche',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def parse(self, response):
        links_desclasified = response.xpath('//a[starts-with(@href, "collection") and (parent::h3 or parent::h2)]/@href').getall()

        for link in links_desclasified:
            # response.urljoin(link) une el link absoluto con el relativo
            # relativo: collection/new/
            # absoluto: https://cia.gov/colelction/new
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})

    def parse_link(self, response, **kwargs):

        link = kwargs['url']
        title = response.xpath("//h1[@class='documentFirstHeading']/text()").get()
        paragraph = response.xpath("//div[@class='field-item even']/p[not(@class)]/text()").getall()

        yield {
            'url': link,
            'title': title,
            'body': " ".join(paragraph)
        }