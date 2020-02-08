from flask import Blueprint
from .apis import create_truck, log_datapoint, get_trucks

rest_api = Blueprint('rest api', __name__)
# TODO: authentication
rest_api.route('/v1/truck/', methods=('POST', ))(create_truck)
rest_api.route('/v1/truck/<truck_id>/log', methods=('POST', ))(log_datapoint)
rest_api.route('/v1/trucks', methods=('GET', ))(get_trucks)
