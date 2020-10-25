from flask import g, jsonify, redirect, request, Response, abort
import pandas as pd
import json
from dateutil.parser import parse, ParserError

from .models import StationMap
from . import app

@app.errorhandler(400)
def custom400(error):
    response = jsonify({'message': error.description['message']})
    response.status_code = 400
    return response

@app.route("/healthz")
def healthz():
    return jsonify(success=True)

@app.route("/v1/locations")
def list_location():
    """Endpoint returning a list of Station
    ---
    responses:
      200:
        examples:
          ["Jurong East","Bukit Batok","Bukit Gombak","Choa Chu Kang"]
    """
    return jsonify(app.config['station_map'].get_location_list())


@app.route("/v1/route",methods=['POST'])
def find_route():
    """Endpoint returning route from source to destination
    ---
    parameters:
      - name: source
        in: formData
        type: string
        required: true
      - name: destination
        in: formData
        type: string
        required: true
    responses:
      200:
        description: route from source to destination
    """
    source = request.form.get('source')
    destination = request.form.get('destination')
    if not source or not destination:
        abort(400, {'message': 'Missing variables'})
    if len(app.config['station_map'].filter_by_station_name(source))==0:
        abort(404)
    if len(app.config['station_map'].filter_by_station_name(destination))==0:
        abort(404)
    route = app.config['station_map'].find_route_by_station_name(source, destination)
    result = {'number_station':len(route), 'route':route,'instruction':app.config['station_map'].get_instruction_from_route(route)}
    return jsonify(result)

@app.route("/v1/route/time",methods=['POST'])
def find_route_time_constraint():
    """Endpoint returning route from source to destination with time constraint
    ---
    parameters:
      - name: source
        in: formData
        type: string
        required: true
      - name: destination
        in: formData
        type: string
        required: true
      - name: start_time
        in: formData
        type: string
        required: true
    responses:
      200:
        description: route from source to destination
    """
    source = request.form.get('source')
    destination = request.form.get('destination')
    start_time = request.form.get('start_time')
    if not source or not destination or not start_time:
        abort(400, {'message': 'Missing variables'})
    if len(app.config['station_map'].filter_by_station_name(source))==0:
        abort(404)
    if len(app.config['station_map'].filter_by_station_name(destination))==0:
        abort(404)
    try:
      time_obj = parse(start_time)
    except (ParserError, TypeError, OverflowError) as e:
      abort(400, {'message': 'Startime: Wrong datetime format. It should be yyyy-mm-ddTHH:MM:SS+TZ or yyyy-mm-ddTHH:MM'})
    route, time = app.config['station_map'].find_route_with_time_constraint(source, destination, time_obj)
    if route is None:
      return jsonify({'time':time, 'route':[], 
        'instruction':['Cannot find any path from given source and destination, some stations are not operation now']})
    result = {'time':time, 'number_station':len(route), 'route':route,'instruction':app.config['station_map'].get_instruction_from_route(route)}
    return jsonify(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=8050)