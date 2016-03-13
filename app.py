#!/usr/bin/env python
import logging

from flask import Flask, session, escape
from crochet import setup, run_in_reactor, retrieve_result, TimeoutError

setup()

app = Flask(__name__)

@run_in_reactor
def crawl_guardian():
    import scrapy
    from scrapy.crawler import CrawlerProcess, CrawlerRunner
    from scrapy.settings import Settings
    from scrapy.utils.project import get_project_settings
    from scrapy.utils.log import configure_logging
    from scraper.guardianukscraper.spiders.guardian_spider import GuardianSpider
    from scraper.guardianukscraper import settings
    import os

    os.environ['SCRAPY_SETTINGS_MODULE'] = 'scraper.guardianukscraper.settings'
    settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
    settings = Settings()
    settings.setmodule(settings_module_path, priority='project')

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

    crawler = scrapy.crawler.Crawler(GuardianSpider,settings)
    crawler.crawl()

    return "Done"

@app.route("/")
def hello():
    if 'scrape' not in session:
        result = crawl_guardian()
        session['scrape'] = result.stash()
        return "Starting scraping, refresh to track."

    result =  retrieve_result(session.pop('scrape'))
    try:
        res = result.wait(timeout=0.1)
        return "Output: {0}".format(res)
    except TimeoutError:
        session['scrape'] = result.stash()
        return "Scrape in progress.."
    except:
        return "Scrape failed:\n" + result.original_failure().getTraceback()

if __name__ == "__main__":
    import os, sys
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    app.secret_key = os.urandom(24)
    app.run(port=5000)
