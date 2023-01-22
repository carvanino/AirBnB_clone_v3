#!/usr/bin/python3
"""app v1"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_session(exception):
    """closes storage"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ Page not found error handler """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    if getenv('HBNB_API_HOST'):
        HOST = getenv('HBNB_API_HOST')
    else:
        HOST = '0.0.0.0'

    if getenv('HBNB_API_PORT'):
        PORT = getenv('HBNB_API_PORT')
    else:
        PORT = '5000'
    app.run(host=HOST, port=PORT, threaded=True)
