from datetime import datetime
from google.cloud import datastore
from google.cloud import pubsub
from flask import jsonify, make_response
import utility
import json

class Capital_Service:

    def __init__(self):
        self.ds = datastore.Client(project=utility.project_id())
        self.kind = "Capital"

    def insert_capital(self, id, data):
        empty_city = {}
        empty_city["code"] = 0
        empty_city["message"] = "string"
        try:
            key = self.ds.key(self.kind, id)
            entity = datastore.Entity(key)
            entity["name"] = data["name"]
            entity["countryCode"] = data["countryCode"]
            entity["country"] = data["country"]
            entity["id"] = id
            entity["latitude"] = data["location"]["latitude"]
            entity["longitude"] = data["location"]["longitude"]
            entity["continent"] = data["continent"]
            self.ds.put(entity)        
            return jsonify("Successfully stored the capital"),200 
        except Exception as e:
            return jsonify (empty_city)

    def fetch_capitals(self):
        empty_city = {}
        empty_city["code"] = 0
        empty_city["message"] = "string"
        try:
            query = self.ds.query(kind=self.kind)
            query.order = ['id']
            city = []
            for ent in list(query.fetch(limit=5)):
                city.append(dict(ent))
            results = []
            for c in city:
              results.append(self.good_json(c))
            if len(city) != 0:
                return jsonify(results),200
            else:
                return jsonify (empty_city),404
        except Exception as e:
            return jsonify (empty_city)

    def get_capital(self,id):
        try:
            query = self.ds.query(kind=self.kind)
            query.add_filter('id','=',id)
            city = []
            for ent in list(query.fetch()):
		            city.append(dict(ent))
            if len(city) != 0:
                return make_response(jsonify(self.good_json(city[0])),200)
            else:
                return make_response("Capital record not found", 404)
        except Exception as e:
            return make_response("Capital record not found", 404)
        
    def delete_capital(self,id):
        empty_city = {}
        empty_city["code"] = 0
        empty_city["message"] = "string"
        #try:
        query = self.ds.query(kind=self.kind)
        query.add_filter('id','=',id)
        entity_list = list(query.fetch())
        
        if len(entity_list) == 0:
            return make_response("Capital record not found", 404)
        
        for ent in entity_list:
            self.ds.delete(ent.key)
            
        return make_response ("Capital object delete status",200)
    

    def get_query_results(self, query):
        results = list()
        for entity in list(query.fetch()):
            results.append(dict(entity))
        return results

    def good_json (self,obj):
        good_obj = {}
        location = {}
        good_obj["name"] = obj["name"]
        good_obj["countryCode"] = obj["countryCode"]
        good_obj["country"] = obj["country"]
        good_obj["id"] = obj["id"]
        location["latitude"] = obj["latitude"]
        location["longitude"] = obj["longitude"]
        good_obj["location"] = location
        good_obj["continent"] = obj["continent"]
        return good_obj

    def publish_capital(self,id,ob):
        try:
            resp = self.get_capital(id)
            if resp.status_code == 200:
                ps_client = pubsub.Client()
                topic = ps_client.topic(ob["topic"])
                city = resp.data
                data = city.encode ('utf-8')
                message_id = topic.publish (data)
                res = {}
                res["messageId"] = message_id
                return make_response (jsonify (res),200)
            elif resp.status_code == 404: 
                return make_response("Capital record not found", 404)
        except Exception as e:
            return make_response("Unexpected error", 400)


        
