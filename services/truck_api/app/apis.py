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
