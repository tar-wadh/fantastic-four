from datetime import datetime
from google.cloud import datastore
from flask import jsonify
import utility
import json

class Capital:

    def __init__(self):
        self.ds = datastore.Client(project=utility.project_id())
        self.kind = "Capital"

    def insert_capital(self, data):
        key = self.ds.key(self.kind)
        entity = datastore.Entity(key)
        entity["name"] = data["name"]
        entity["countryCode"] = data["countryCode"]
        entity["country"] = data["country"]
        entity["id"] = data["id"]
        entity["location"]["latitude"] = data["location"]["latitude"]
        #entity["location"]["longitude"] = data["location"]["longitude"]
        entity["continent"] = data["continent"]
        return self.ds.put(entity)

    def fetch_capitals(self):
        query = self.ds.query(kind=self.kind)
        query.order = ['id']
        city = []
        for ent in list(query.fetch(limit=5)):
          city.append(dict(ent))
        return jsonify (city)

    def get_capital(self,id):
        query = self.ds.query(kind=self.kind)
        query.add_filter('id','=',id)
        city = []
        for ent in list(query.fetch()):
          city.append(dict(ent))
        return jsonify (city)

    def get_query_results(self, query):
        results = list()
        for entity in list(query.fetch()):
            results.append(dict(entity))
        return results


def parse_captals_time(note):
    """converts a greeting to an object"""
    return {
        'text': note['text'],
        'timestamp': note['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    }
