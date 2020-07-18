# -*- coding: utf-8 -*-
import scrapy
import datetime


class Geelong22750Spider(scrapy.Spider):
    name = 'Geelong_22750'
    allowed_domains = ['geelongaustralia.com.au']
    start_urls = [
        'https://www.geelongaustralia.com.au/advertisedplanning/default.aspx']

    def parse(self, response):
        # for tables
        print("tables")
        ids = ['ctl00_ContentBody_GV_FINISHED',
               'ctl00_ContentBody_GV_CURRENT'
               ]
        base_url = 'https://www.geelongaustralia.com.au/advertisedplanning/'
        tables = response.xpath('//table')
        print(tables)
        for table in tables:
            trs = table.xpath("./tr")
            print(trs)
            for tr in trs:
                if tr.xpath('./td') and table.xpath('./@id').extract()[0] == ids[1]:
                    name = tr.xpath('./td')[1]
                    url = tr.xpath("./td")[0]
                    code = tr.xpath("./td")[2]
                    date = tr.xpath("./td")[3]
                    end_date = tr.xpath("./td")[4]
                    data = {
                        'name': name.xpath('./text()').get().strip(),
                        'url': url.xpath('./a/@href').get().strip(),
                        'property': url.xpath('./a/text()').get().strip(),
                        'code': code.xpath('./text()').get().strip(),
                        'date': date.xpath('./text()').get().strip(),
                        'end_date': end_date.xpath('./text()').get().strip(),
                        'link_visit': base_url + url.xpath('./a/@href').get().strip()
                    }
                    yield scrapy.Request(url=data['link_visit'], meta={"data": data}, callback=self.parse2)

                if tr.xpath('./td') and table.xpath('./@id').extract()[0] == ids[0]:
                    name = tr.xpath('./td')[1]
                    url = tr.xpath("./td")[0]
                    code = tr.xpath("./td")[2]
                    end_date = tr.xpath("./td")[3]
                    data = {
                        'name': name.xpath('./text()').get().strip(),
                        'url': url.xpath('./a/@href').get().strip(),
                        'code': code.xpath('./text()').get().strip(),
                        'property': url.xpath('./a/text()').get().strip(),
                        'date': "None",
                        'end_date': end_date.xpath('./text()').get().strip(),
                        'link_visit': base_url + url.xpath('./a/@href').get().strip()
                    }
                    yield scrapy.Request(url=data['link_visit'], meta={"data": data}, callback=self.parse2)

    def parse2(self, response):
        data = response.meta['data']
        # print("data is printed")
        # print(data)
        paragraph = response.xpath(
            '//div[@id="readcontent"]/p/text()')
        activitiy = paragraph[0].get().strip()
        date = data['date']
        try:
            date = datetime.datetime.strptime(date, r"%d %b %Y")
        except ValueError:
            date = response.xpath(
                "//strong[contains(text(),'Advertised:')]/ancestor::p/text()")[0].get().strip()
            date = datetime.datetime.strptime(date, r"%d %b %Y")

        yield{
            'appNum': data['code'],
            'nameLGA': 'Geelong',
            'codeLGA': '22750',
            'address': data['property'] + " " + data['name'],
            'activity': activitiy,
            'applicant': '',
            'lodgeDate': date,
            'decisionDate': None,
            'status': None,
            'url': response.url
        }
