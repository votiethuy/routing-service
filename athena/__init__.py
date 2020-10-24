from flask import Flask, g
from flasgger import Swagger
app = Flask(__name__)
swagger = Swagger(app)


import athena.models
import athena.views

app.config['station_map'] = athena.models.StationMap()