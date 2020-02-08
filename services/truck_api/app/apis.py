from math import cos, asin, sqrt
from database_core.database.gateway import DBGateway
from database_core.factories import Truck, TruckLog
from database_core.repositories import TruckRepository, TruckLogRepository
from datetime import datetime
from flask import jsonify, request, abort, make_response
from schematics.exceptions import ValidationError, DataError
from sqlalchemy.exc import IntegrityError

truck_repository = TruckRepository()
truck_log_repository = TruckLogRepository()


def create_truck():
    try:
        truck = Truck(request.json)
        truck.validate()
        obj = truck_repository.create(DBGateway, **truck.to_native())
        return jsonify(obj.to_native()), 201
    except IntegrityError as e:
        abort(make_response(jsonify(message="truck already exist"), 409))
    except (ValidationError, DataError) as e:
        abort(make_response(jsonify(e.to_primitive()), 400))


def log_datapoint(truck_id):
    try:
        truck_log = TruckLog(request.json)
        truck_log.truck_id = truck_id
        truck_log.log_time = datetime.now()
        truck_log.validate()
        obj = truck_log_repository.create(DBGateway, **truck_log.to_native())
        return jsonify(obj.to_native()), 201
    except IntegrityError as e:
        abort(make_response(jsonify(message="truck_log already exist"), 409))
    except (ValidationError, DataError) as e:
        abort(make_response(jsonify(e.to_primitive()), 400))


def get_trucks():
    active_trucks = truck_repository.get_active_trucks(DBGateway)
    return jsonify([obj.to_native() for obj in active_trucks]), 200


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295  #Pi/180
    a = 0.5 - cos(
        (lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos(
            (lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))  #2*R*asin...


def get_distance(truck_id):
    start_time = datetime.fromtimestamp(int(request.args.get('start_time')))
    end_time = datetime.fromtimestamp(int(request.args.get('end_time')))
    truck_logs = truck_log_repository.get_truck_log_in_range(
        DBGateway, truck_id, start_time, end_time)

    total_distance = 0
    for i in range(1, len(truck_logs)):
        total_distance += distance(float(truck_logs[i - 1].latitude),
                                   float(truck_logs[i - 1].longitude),
                                   float(truck_logs[i].latitude),
                                   float(truck_logs[i].longitude))
    return jsonify({'total_distance': total_distance}), 200
