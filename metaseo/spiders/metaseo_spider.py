import scrapy
import re
from bs4 import BeautifulSoup
import html2text

class MetaseoSpiderSpider(scrapy.Spider):
    name = 'metaseo_spider'
    # allowed_domains = ['www.google.com']
    #start_urls = ['https://www.verizon.com/info/low-income-internet/',
    #             'https://www.highspeedinternet.com/resources/are-there-government-programs-to-help-me-get-internet-service',
    #             'https://www.att.com/internet/access/',
    #             'https://www.cabletv.com/blog/low-income-internet',
    #             'https://www.spectrum.com/browse/content/spectrum-internet-assist',
    #             'https://www.internetessentials.com/']

    with open("urls.txt", "rt") as f:
        start_urls = [url.strip() for url in f.readlines()]

    #start_urls = ['https://www.internetessentials.com/']

    def parse(self, response):

        url = response.request.url
        title = response.xpath('//title/text()').extract_first()
        title = re.sub(r'[^\w\s]',' ',title)
        title = re.sub(' +', ' ', title)
        description = response.xpath('//*[@name="description"]/@content').extract_first()
        description = re.sub(r'[^\w\s]',' ',description)
        description = re.sub(' +', ' ', description)    
        html = ' '.join(response.xpath('//body').extract())
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        body = converter.handle(html)
        #body = ' '.join(response.xpath('//body//text()').re('(\w+)'))
        #body = ' '.join(response.xpath('//body//div//p//text()').extract())
        #body2 = ' '.join(response.xpath('//body//p//text()').extract())
        #body = body + ' ' + body2
        body = body.replace('\r',' ').replace('\n',' ').replace('\t',' ')
        body = re.sub(r'[^\w\s]',' ',body)
        body = re.sub(' +', ' ', body)
        h1 = ' '.join(response.xpath('//body//h1//text()').extract())
        h1p = ' '.join(response.xpath('//body//h1//p//text()').extract())
        h1pc = ' '.join(response.xpath('//body//h1//p//span//text()').extract())
        h2 = ' '.join(response.xpath('//body//h2//text()').extract())
        h2p = ' '.join(response.xpath('//body//h2//p//text()').extract())
        h3 = ' '.join(response.xpath('//body//h3//text()').extract())
        h3p = ' '.join(response.xpath('//body//h3//p//text()').extract())
        h = h1 + ' ' + h2 + ' ' + h3 + ' ' + h1p + ' ' + h2p + ' ' + h3p
        h = h.replace('\r',' ').replace('\n',' ').replace('\t',' ')
        h = re.sub(r'[^\w\s]',' ',h)
        h = re.sub(' +', ' ', h)

        yield{'url': url,
              'TITLE TAG': title,
              'META DESCRIPTION': description,
              'HEADER TAGS': h,
              'BODY': body}

