#!/usr/bin/env python
import logging

from flask import Flask, session, escape, render_template, request, jsonify
from crochet import setup, run_in_reactor, retrieve_result, TimeoutError

setup()

app = Flask(__name__)

def get_summaries_collection():
    import pymongo
    from scraper.guardianukscraper import settings
    from scrapy.settings import Settings
    sets = Settings()
    sets.setmodule(settings, priority='project')
    connection = pymongo.MongoClient(
            sets['MONGODB_SERVER'],
            sets['MONGODB_PORT']
    )
    db = connection[sets['MONGODB_DB']]
    return db[sets['MONGODB_COLLECTION']]

def format_summary(summary):
    article_sentences_len = len(summary['article_sentences'])
    ranking = sorted(summary['links'], key=lambda commentInd: len(summary['links'][commentInd]), reverse=True)
    ranking = map(lambda ind: "s" + str(int(ind) + article_sentences_len), ranking)
    links = {}
    for commentInd in summary['links']:
        sentenceId = 's' + str(int(commentInd) + article_sentences_len)
        links[sentenceId] = []
        for link in summary['links'][commentInd]:
            links[sentenceId].append({ 'reply': 's' + str(link[0]), 'argument': link[2] })
    comments = {}
    i = 0
    for comment in summary['comments']:
        commentId = 'c' + str(i)
        comments[commentId] = { 'bloggerId': comment['author'][0] if len(comment['author']) > 0 else None, 'replyTo': comment['reply_to_author'][0] if len(comment['reply_to_author']) > 0 else None, 'sentences': [] }
        i = i + 1
    sentences = {}
    i = 0
    for sentence in summary['all_sentences_dicts']:
        sentenceId = 's' + str(i)
        sentences[sentenceId] = sentence['text']
        if (sentence['comment'] != -1):
            commentId = 'c' + str(sentence['comment'])
            comments[commentId]['sentences'].append(sentenceId)
        i = i + 1
    return { 'author': summary['author'], 'sentences': sentences, 'comments': comments, 'links': links, 'ranking': ranking[:10] }

@run_in_reactor
def crawl_guardian(job_id, url):
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
    return crawler.crawl(job_id=job_id, url=url)

@app.route("/summarize", methods=['POST'])
def summarize():
    from bson import json_util
    url = request.json["url"]
    job_id = url
    summaries = get_summaries_collection()
    article_summary = summaries.find_one({ 'job_id': job_id }, { '_id': 0, 'author': 1, 'title': 1, 'links': 1, 'comments': 1, 'all_sentences_dicts': 1, 'article_sentences': 1 })

    if article_summary:
        return jsonify(status='done', result=format_summary(article_summary))

    if 'scrape' not in session:
        result = crawl_guardian(job_id, url)
        session['scrape'] = result.stash()
        return jsonify(status='processing')

    result = retrieve_result(session.pop('scrape'))
    try:
        res = result.wait(timeout=0.1)
        article_summary = summaries.find_one({ 'job_id': job_id }, { '_id': 0, 'author': 1, 'title': 1, 'links': 1, 'comments': 1, 'all_sentences_dicts': 1 })
        return jsonify(status='done', result=format_summary(article_summary))
    except TimeoutError:
        session['scrape'] = result.stash()
        return jsonify(status='processing')
    except:
        return jsonify(status='failed', traceback=result.original_failure().getTraceback())

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    import os, sys
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    app.secret_key = os.urandom(24)
    app.run(port=5000)
