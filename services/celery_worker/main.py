from datetime import datetime
from dateutil import tz
from datetime import timedelta
from math import cos, asin, sqrt
from database_core.database.gateway import DBGateway
from database_core.factories import Truck, TruckLog
from database_core.repositories import TruckRepository, TruckLogRepository

truck_repository = TruckRepository()
truck_log_repository = TruckLogRepository()


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295  #Pi/180
    a = 0.5 - cos(
        (lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos(
            (lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))  #2*R*asin...


def get_total_distance():

    trucks = truck_repository.get_all(DBGateway)
    for truck in trucks:
        today = datetime.utcnow().date()
        start_of_day = datetime(today.year,
                                today.month,
                                today.day,
                                tzinfo=tz.tzutc())
        end_of_day = start_of_day + timedelta(1)
        truck_logs = truck_log_repository.get_truck_log_in_range(
            DBGateway, truck.id, start_of_day, end_of_day)

        total_distance = 0
        total_active_time = 0
        for i in range(1, len(truck_logs)):
            total_distance += distance(float(truck_logs[i - 1].latitude),
                                       float(truck_logs[i - 1].longitude),
                                       float(truck_logs[i].latitude),
                                       float(truck_logs[i].longitude))
            active_time = (truck_logs[i].log_time -
                           truck_logs[i - 1].log_time).total_seconds()
            if active_time <= 30:
                total_active_time += active_time
        print(
            f'truck_id: {truck.id}, total_distance: {total_distance}, total_active_time: {total_active_time}'
        )
