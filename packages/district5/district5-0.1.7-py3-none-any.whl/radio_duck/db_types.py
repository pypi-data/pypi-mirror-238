import datetime
import time

# ----------------------------------------------------------
# Types

#: The type for date values.
Date = datetime.date
#: The type for time values.
Time = datetime.time
#: The type for timestamp values.
Timestamp = datetime.datetime


def Binary(string):
    return str(string)


def DateFromTicks(ticks: int) -> Date:
    """Construct a date value from a count of seconds."""
    # Standard implementations from PEP 249 itself
    return Date(*time.localtime(ticks)[:3])


def TimeFromTicks(ticks: int) -> Time:
    """Construct a time value from a count of seconds."""
    return Time(*time.localtime(ticks)[3:6])


def TimestampFromTicks(ticks: int) -> Timestamp:
    """Construct a timestamp value from a count of seconds."""
    return Timestamp(*time.localtime(ticks)[:6])


class Type(object):
    def __init__(self, type_code: int):
        self._type_code = type_code

    def get_type_code(self):
        return self._type_code


# use the 5 ducks
# from https://disney.fandom.com/wiki/District_5_Ducks
# using jersey numbers :)
STRING = Type(96)  # one of 5 ducks in flying v -charlie convay.
BINARY = Type(4)  # one of 5 ducks in flying v -averman
NUMBER = Type(9)  # one of 5 ducks in flying v -jesse hall.
DATETIME = Type(1)  # one of 5 ducks in flying v -Terry Hall
ROWID = Type(0)  # one of 5 ducks in flying v -Guy Germaine
UNKNOWN = Type(-1)  # one of 5 ducks in flying v -Guy Germaine

__types = {
    "STRING": STRING,
    "BINARY": BINARY,
    "NUMBER": NUMBER,
    "DATETIME": DATETIME,
    "ROWID": ROWID,
    "UNKNOWN": UNKNOWN,
}


def get_type_code(col_type: str) -> int:
    return __types.get(col_type, UNKNOWN).get_type_code()


def get_type(col_type: str) -> Type:
    return __types.get(col_type, UNKNOWN)



# ----------------------------------------------------------

# https://github.com/preset-io/elasticsearch-dbapi/blob/master/es/baseapi.py
# def get_type(data_type) -> int:
#     type_map = {
#         "text": Type.STRING,
#         "keyword": Type.STRING,
#         "integer": Type.NUMBER,
#         "half_float": Type.NUMBER,
#         "scaled_float": Type.NUMBER,
#         "geo_point": Type.STRING,
#         # TODO get a solution for nested type
#         "nested": Type.STRING,
#         "object": Type.STRING,
#         "date": Type.DATETIME,
#         "datetime": Type.DATETIME,
#         "timestamp": Type.DATETIME,
#         "short": Type.NUMBER,
#         "long": Type.NUMBER,
#         "float": Type.NUMBER,
#         "double": Type.NUMBER,
#         "bytes": Type.NUMBER,
#         "boolean": Type.BOOLEAN,
#         "ip": Type.STRING,
#         "interval_minute_to_second": Type.STRING,
#         "interval_hour_to_second": Type.STRING,
#         "interval_hour_to_minute": Type.STRING,
#         "interval_day_to_second": Type.STRING,
#         "interval_day_to_minute": Type.STRING,
#         "interval_day_to_hour": Type.STRING,
#         "interval_year_to_month": Type.STRING,
#         "interval_second": Type.STRING,
#         "interval_minute": Type.STRING,
#         "interval_day": Type.STRING,
#         "interval_month": Type.STRING,
#         "interval_year": Type.STRING,
#         "time": Type.STRING,
#     }
#     return type_map[data_type.lower()]
