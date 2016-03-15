# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scraper.guardianukscraper import settings
from scrapy.settings import Settings
import logging

from summarizer.summarizer import summarize
import collections

class MongoDBPipeline(object):

    def __init__(self):
        sets = Settings()
        sets.setmodule(settings, priority='project')
        connection = pymongo.MongoClient(
                sets['MONGODB_SERVER'],
                sets['MONGODB_PORT']
        )
        db = connection[sets['MONGODB_DB']]
        self.collection = db[sets['MONGODB_COLLECTION']]

    def convert_keys_to_string(self, dictionary):
        """Recursively converts dictionary keys to strings."""
        if not isinstance(dictionary, dict):
            return dictionary

        return dict((str(k), self.convert_keys_to_string(v))
            for k, v in dictionary.items())

    def process_item(self, item, spider):
        valid = True
        if item:
            summary = summarize(dict(item))
            str_key_summary = self.convert_keys_to_string(summary)
            self.collection.insert_one(str_key_summary)
            logging.log(logging.INFO, "Summary added.")
        return item
