from datetime import datetime


def isoformat_to_datetime(isoformat_string):
    return datetime.strptime(isoformat_string, "%Y-%m-%dT%H:%M:%S.%f")
