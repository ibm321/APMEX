# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class ApmexSpider(scrapy.Spider):
    name = 'apmex'
    allowed_domains = [
        'www.apmex.com']
    start_urls = [
        'https://www.apmex.com/category/24100/mexican-silver-libertads/all?f_metalname=silver&f_productoz=5+oz%2c2+oz%2c1+oz%2c1%2f2+oz%2c1%2f4+oz%2c1%2f10+oz%2c1%2f20+oz&f_grade=brilliant+uncirculated%2cproof&ipp=120']

    def parse(self, response):
        products = response.xpath(
            '//div[@class="page-container"]/div[3]/div[4]/div[2]/div/div/a/@href').extract()

        # yield{'products': products}

        # url = "https://www.apmex.com" + products[0]
        # self.logger.info('Parse function called on %s', url)
        for product in products:
            url = "https://www.apmex.com" + product
            # self.logger.info('Parse function called on %s', url)
            yield Request(url, callback=self.parse_product)

        ibm = response.xpath('//ul[@class="pagination"]/li')[-1]
        relative_next_page = ibm.xpath('a/@href').extract()
        obslute_next_page = "https://www.apmex.com" + relative_next_page[0]
        yield Request(obslute_next_page)

    def parse_product(self, response):
        product_title = response.xpath(
            '//h1[@class="product-title "]/text()').extract()
        product_spec_left = response.xpath(
            '//ul[@class="product-table left"]/li/span/text()').extract()
        product_spec_right = response.xpath(
            '//ul[@class="product-table right"]/li/span/text()').extract()

        Product_id = product_spec_left[0]
        Product_Year = product_spec_left[1]
        Product_Grade = product_spec_left[2]
        Product_Grade_Service = product_spec_left[3]
        Product_Denomination = product_spec_left[4]
        Product_Mint_Mark = product_spec_left[5]
        Product_Metal_Mark = product_spec_left[6]

        Product_Purity = product_spec_right[0]
        Product_thinkness = product_spec_right[1]
        Product_Diameter = product_spec_right[2]
        Product_Price = response.xpath('//p[@class="price"]/text()').extract()

        # images_URL = response.xpath(
        #     '//div[@id="additional-images-carousel"]/div/div/a[1]/@href')
        first_image = response.xpath(
            '//div[@id="additional-images-carousel"]/div/div/a[1]/@href').extract()
        second_image = response.xpath(
            '//div[@id="additional-images-carousel"]/div/div/a[2]/@href').extract()
        third_image = response.xpath(
            '//div[@id="additional-images-carousel"]/div/div/a[3]/@href').extract()

        stock = response.xpath(
            '//section[@class="item-overview"]/div[@class="item-right"]/div[@class="price-line"]/div[@class="left"]/p[1]/text()').extract()
        if stock[0] == "Currently Out of Stock":
            state = 0
        else:
            state = 1
        yield{
            'product_title': product_title,
            'product_id': Product_id,
            'Product_Price': Product_Price,
            'product_year': Product_Year,
            'product_grade': Product_Grade,
            'Product_Grade_Service': Product_Grade_Service,
            'Product_Denomination': Product_Denomination,
            'Product_Mint_Mark': Product_Mint_Mark,
            'Product_Metal_Mark': Product_Metal_Mark,
            'product_purity': Product_Purity,
            'Product_thinkness':  Product_thinkness,
            'Product_Diameter': Product_Diameter,
            'First_Image': first_image,
            'Second_Image': second_image,
            'Third_Image': third_image,
            'Stock': state

        }
