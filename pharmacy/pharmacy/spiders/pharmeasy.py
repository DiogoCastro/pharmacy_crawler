import json
import csv
import scrapy
from scrapy.crawler import CrawlerProcess


class PharmeasySpider(scrapy.Spider):
    name = 'pharmeasy'
    base_url = 'https://pharmeasy.in/api/otc/getCategoryProducts?categoryId=87&page='
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
        'page': 0,
    }
    pages = [1]

    def __init__(self):
        with open('pharmeasy.csv', 'w') as csv_file:
            csv_file.write(
                'name,slug,manufacturer,type,price before,sale price,discount decimal,discount percent,category id,availability,images,images string\n'
            )

    def start_requests(self):
        # Scrape from infinite scroll
        for page in self.pages:
            next_page = self.base_url + str(page)
        yield scrapy.Request(url=next_page, headers=self.headers, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)

        # Data extraction logic
        for product in data['data']['products']:
            items = {
                'name': product['name'],
                'slug': product['slug'],
                'manufacturer': product['manufacturer'],
                'product_type': product['productType'],
                'price_before': product['mrpDecimal'],
                'sale_price': product['salePriceDecimal'],
                'discount_decimal': product['discountDecimal'],
                'discount_percent': product['discountPercent'],
                'category_id': product['categoryId'],
                'availability': product['isAvailable'],
                'images': product['images'],
                'images_string': ', '.join(product['images']),
            }
            # Appending results to csv
            with open('pharmeasy.csv', 'a') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=items.keys())
                writer.writerow(items)


process = CrawlerProcess()
process.crawl(PharmeasySpider)
process.start()

# Debugging data straction
# PharmeasySpider.parse(PharmeasySpider, '')
