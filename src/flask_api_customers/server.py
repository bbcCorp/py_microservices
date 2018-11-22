import os
import sys
import json

from flask import Flask
from flask_restful import Resource, Api
from werkzeug.exceptions import NotFound

import settings as CONF
from customers import CustomerAPI

app = Flask(__name__)
api = Api(app)

api.add_resource(CustomerAPI, '/customers', '/customers/<int:id>')


@app.route("/", methods=['GET'])
def index():
    return json.dumps({
        "uri": "/",
        "subresource_uris": {
            "customers": "/customers/<custid>"
        }
    })

###############################################################################
if __name__ == "__main__":
    
    app.run(
        port=CONF.app_settings["port"], 
        debug=CONF.app_settings["debug_mode"]
    )    