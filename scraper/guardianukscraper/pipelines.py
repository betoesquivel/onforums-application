# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scraper.guardianukscraper import settings
from scrapy.settings import Settings
import logging


#class GuardianukscraperPipeline(object):
    #def process_item(self, item, spider):
        #return item

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

    def process_item(self, item, spider):
        valid = True
        #for data in item:
            #if not data:
                #valid = False
                #raise DropItem("Missing {0}!".format(data))
        if item:
            self.collection.insert(dict(item))
            logging.log(logging.INFO, "Article added.")
        return item
