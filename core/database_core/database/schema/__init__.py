# coding=utf-8

from sqlalchemy import (Column, Integer, DateTime, Numeric, ForeignKey, String,
                        DDL, FetchedValue, func, Date, UniqueConstraint)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy_utils import JSONType
from geoalchemy2 import Geometry


class Base(object):
    """
    a base class for all of our models, this defines:
    1) the table name to be the lower-cased version of the class name
    2) generic __init__ and __repr__ functions
    """
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __init__(self, **kwargs):
        for key in kwargs:
            if key not in self.attr_accessor:
                raise Exception(f'Invalid Prop: {key}')
            setattr(self, key, kwargs[key])

    def to_dict(self):
        return {
            k: v
            for k, v in self.__dict__.items() if not k.startswith('_')
        }

    def __repr__(self):
        def filter_properties(obj):
            # this function decides which properties should be exposed through repr
            properties = obj.__dict__.keys()
            for prop in properties:
                if prop[0] != "_" and not callable(prop):
                    yield (prop, str(getattr(obj, prop)))
            return

        prop_tuples = filter_properties(self)
        prop_string_tuples = (": ".join(prop) for prop in prop_tuples)
        prop_output_string = " | ".join(prop_string_tuples)
        cls_name = self.__module__ + "." + self.__class__.__name__

        return "<%s('%s')>" % (cls_name, prop_output_string)


Base = declarative_base(cls=Base)


class Truck(Base):
    __tablename__ = 'truck'
    id = Column(Integer, primary_key=True)
    plate_number = Column(String)


class TruckLog(Base):
    __tablename__ = 'truckLog'
    id = Column(Integer, primary_key=True)
    truck_id = Column(Integer,
                      ForeignKey("truck.id", ondelete='RESTRICT'),
                      nullable=False)
    latitude = Column(Numeric(30, 21))
    longitude = Column(Numeric(30, 21))
    geom = Column(Geometry('POINT'))
