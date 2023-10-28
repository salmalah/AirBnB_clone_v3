#!/usr/bin/python3
""" Flask Application """
from models import storage
from flask_cors import CORS
from os import environ
from api.v1.views import app_views
from flask import Flask, jsonify


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, origins="0.0.0.0")


@app.teardown_appcontext
def close_storage(error):
    """ Closes the database connection  """
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """
    Handles 404 errors by returning a JSON-formatted response
    content : {"error": "Not found"}
    """
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    """ Run the Flask server """
    app = create_app()
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
