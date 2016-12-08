"""Main Entrypoint for the Application"""

import logging
import json
import base64

from flask import Flask, request, g
from flask import jsonify, make_response

import capital
import utility
import cloudstorage

app = Flask(__name__)


@app.route('/')
def hello_world():
    """hello world"""
    return 'Hello World!'

@app.route('/api/status', methods=['GET'])
def status():
    api_status = {}
    api_status["insert"] = True
    api_status["fetch"] = True
    api_status["delete"] = True
    api_status["list"] = True
    api_status["pubsub"] = True
    api_status["storage"] = False

    return jsonify(api_status), 200

#@app.route('/pubsub/receive', methods=['POST'])
#def pubsub_receive():
#    """dumps a received pubsub message to the log"""
#
#    data = {}
#    try:
#        obj = request.get_json()
#        utility.log_info(json.dumps(obj))
#
#        data = base64.b64decode(obj['message']['data'])
#        utility.log_info(data)
#
#    except Exception as e:
#        # swallow up exceptions
#        logging.exception('Oops!')
#
#    return jsonify(data), 200
#
#
#@app.route('/api/capitals/<id>/', methods=['PUT'])

@app.route('/api/capitals/<id>', methods=['GET','PUT', 'DELETE'])
def get_put_capital(id):
    if request.method == 'GET':
      return get_capital (int(id))
    elif request.method == 'PUT':
      return put_capital (int(id))
    elif request.method == 'DELETE':
      return delete_capital (int(id))
      
def put_capital(id):
   """inserts capital from datastore"""
   cap_service = capital.Capital_Service()
   text = request.get_json()
   result = cap_service.insert_capital(id, text)
   return result

def get_capital(id):
    cap = capital.Capital_Service()
    result = cap.get_capital(id)
    return result

def delete_capital(id):
    cap = capital.Capital_Service()
    result = cap.delete_capital(id)
    return result

@app.route('/api/capitals', methods=['GET'])
def get_all_capitals():
    cap = capital.Capital_Service()
    result = cap.fetch_capitals()
    return result

@app.route('/api/capitals/<id>/publish', methods=['POST'])
def publish(id):
    cap = capital.Capital_Service()
    ob = request.get_json()
    result = cap.publish_capital(int(id),ob)
    return result

@app.route('/api/capitals/<id>/store', methods=['POST'])
def store_capitals_gcs(id):
    gcs = cloudstorage.Storage()  
    content = request.get_json()
    bucket_name = content["bucket"]
    gcs.create_bucket(bucket_name)
   
    cap = capital.Capital_Service()
    empty_city = {}
    empty_city["code"] = 0
    empty_city["message"] = "string"
    try:
        query = cap.ds.query(kind=cap.kind)
        query.add_filter('id','=',int(id))
        city = []
        for ent in list(query.fetch()):
    	    city.append(dict(ent))
        if len(city) != 0:
            cap_json = cap.good_json(city[0])
        else:
            return make_response("Capital record not found", 404)
    except Exception as e:
        return make_response("Unexpected error", 404)
    
    with open(id +'.txt', 'w') as outfile:
        json.dump(cap_json, outfile) 
   
    if gcs.store_file_to_gcs(bucket_name, id+'.txt'):
        return make_response("Successfully stored in GCS", 200)
    else:
        return make_response("Unexpected error", 404)

@app.errorhandler(500)
def server_error(err):
    """Error handler"""
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(err), 500


if __name__ == '__main__':
    # Used for running locally
    app.run(host='127.0.0.1', port=8080, debug=True)
