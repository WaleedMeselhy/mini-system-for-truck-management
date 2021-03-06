import datetime
from datetime import timedelta
from database_core.factories import Truck, TruckLog
from decimal import Decimal
from sqlalchemy import or_, and_, desc, func
from sqlalchemy.sql import tuple_


class DefaultRepository(object):
    model = None
    model_id_field = None

    def __init__(self, model=None, model_id_field=None):
        if model:
            self.model = model
        if model_id_field:
            self.model_id_field = model_id_field

    def get_or_create(self, gateway, defaults=None, **kwargs):
        with gateway.session_scope() as session:
            obj, created = gateway.get_or_create(session,
                                                 self.model.alchemy_model,
                                                 defaults=defaults,
                                                 **kwargs)
            obj = self.model.from_alchemy(obj) if obj else None
        return obj, created

    def get_by_id(self, gateway, ident):
        with gateway.session_scope() as session:
            obj = gateway.get_by_id(session,
                                    self.model.alchemy_model,
                                    ident=ident)
            obj = self.model.from_alchemy(obj) if obj else None
        return obj

    def get(self, gateway, **kwargs):
        with gateway.session_scope() as session:
            obj = gateway.get(session, self.model.alchemy_model, **kwargs)
            obj = self.model.from_alchemy(obj) if obj else None
        return obj

    def filter(self, gateway, **kwargs):
        with gateway.session_scope() as session:
            objs = gateway.filter(session, self.model.alchemy_model, **kwargs)
            objs = list(map(lambda obj: self.model.from_alchemy(obj), objs))
        return objs

    def get_all(self, gateway):
        with gateway.session_scope() as session:
            objs = gateway.get_all(session, self.model.alchemy_model)
            objs = list(map(lambda obj: self.model.from_alchemy(obj), objs))
        return objs

    def update(self, gateway, obj, **kwargs):
        with gateway.session_scope() as session:
            obj = gateway.update(session, self.model.alchemy_model,
                                 getattr(obj, self.model_id_field), **kwargs)
            obj = self.model.from_alchemy(obj) if obj else None
        return obj

    def update_all(self, gateway, criterion, **kwargs):
        with gateway.session_scope() as session:
            ids = gateway.update_all(session, self.model.alchemy_model,
                                     criterion, **kwargs)
            # objs = list(map(lambda obj: self.model.from_alchemy(obj), objs))
        return ids

    def create(self, gateway, **kwargs):
        with gateway.session_scope() as session:
            obj = gateway.create(session, self.model.alchemy_model, **kwargs)
            session.refresh(obj)
            obj = self.model.from_alchemy(obj)
        return obj


class TruckRepository(DefaultRepository):
    model = Truck
    model_id_field = 'id'

    def get_active_trucks(self, gateway):
        current_time = datetime.datetime.now()
        five_mints_ago = current_time - datetime.timedelta(minutes=5)
        model = self.model.alchemy_model
        with gateway.session_scope() as session:
            objs = session.query(model).join(TruckLog.alchemy_model).filter(
                TruckLog.alchemy_model.log_time > five_mints_ago).order_by(
                    TruckLog.alchemy_model.log_time.desc())
            objs = list(map(lambda obj: self.model.from_alchemy(obj), objs))
        return objs


class TruckLogRepository(DefaultRepository):
    model = TruckLog
    model_id_field = 'id'

    def create(self, gateway, **kwargs):
        kwargs['geom'] = func.ST_Point(kwargs['longitude'], kwargs['latitude'])
        obj = super().create(gateway, **kwargs)
        return obj

    def get_truck_log_in_range(self, gateway, truck_id, start_time, end_time):
        model = self.model.alchemy_model
        with gateway.session_scope() as session:
            objs = session.query(model).filter(
                model.truck_id == truck_id,
                and_(model.log_time >= start_time,
                     model.log_time < end_time)).order_by(
                         model.log_time.asc())
            objs = list(map(lambda obj: self.model.from_alchemy(obj), objs))
            return objs