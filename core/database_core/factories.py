from schematics.models import Model
from schematics.types import (StringType, DecimalType, DateTimeType, IntType,
                              DictType, DateType, BooleanType)
from .database.schema import (Truck as AlchemyTruck, TruckLog as
                              AlchemyTruckLog)


class SQLAlchemyMixin:
    def to_alchemy(self):
        return self.alchemy_model(**self.to_native())

    @classmethod
    def from_alchemy(cls, alchemy_object):
        return cls(alchemy_object.to_dict(), strict=cls._strict)


class Base(Model):
    def __repr__(self):
        def filter_properties(obj):
            # this function decides which properties should be exposed through repr
            properties = obj.to_native().keys()
            for prop in properties:
                yield (prop, str(getattr(obj, prop)))
            return

        prop_tuples = filter_properties(self)
        prop_string_tuples = (": ".join(prop) for prop in prop_tuples)
        prop_output_string = " | ".join(prop_string_tuples)
        cls_name = self.__module__ + "." + self.__class__.__name__

        return "<%s('%s')>" % (cls_name, prop_output_string)


class Truck(Base, SQLAlchemyMixin):
    _strict = True
    alchemy_model = AlchemyTruck
    id = IntType()
    plate_number = StringType(required=True)


class TruckLog(Base, SQLAlchemyMixin):
    _strict = False
    alchemy_model = AlchemyTruckLog
    id = IntType()
    truck_id = IntType(required=True)
    latitude = DecimalType(required=True)
    longitude = DecimalType(required=True)
    log_time = DateTimeType(required=True)