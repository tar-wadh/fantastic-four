"""Main Entrypoint for the Application"""

import logging
import json
import base64

from flask import Flask, request
from flask import jsonify

import capital
import utility


app = Flask(__name__)


@app.route('/')
def hello_world():
    """hello world"""
    return 'Hello World!'

@app.route('/api/status', methods=['GET'])
def status():
    api_status = {}
    api_status["insert"] = False
    api_status["fetch"] = False
    api_status["delete"] = False
    api_status["list"] = False

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
@app.route('/api/capitals', methods=['PUT'])
def put_capital():
    """inserts capital from datastore"""
    cap = capital.Capital()
    text = request.get_json()
    cap.insert_capital(text)
    return "done"

@app.route('/api/capitals/<id>', methods=['GET'])
def get_capital(id):
    cap = capital.Capital()
    result = cap.get_capital(id)
    return result

@app.route('/api/capitals', methods=['GET'])
def get_all_capitals():
    cap = capital.Capital()
    result = cap.fetch_capitals()
    return result



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
