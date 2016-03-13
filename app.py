#!/usr/bin/env python
from flask import Flask
import scrapy
from scrapy.crawler import CrawlerProcess
from scraper.guardianukscraper.spiders.guardian_spider import GuardianSpider
app = Flask(__name__)

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
@app.route("/")
def hello():
    process.crawl (GuardianSpider)
    process.start()
    return "Hello World!"

if __name__ == "__main__":
    app.run(port=2000)
