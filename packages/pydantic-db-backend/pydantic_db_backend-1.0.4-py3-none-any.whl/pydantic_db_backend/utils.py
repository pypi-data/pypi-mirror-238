from __future__ import annotations

import datetime
import json

from pydantic_db_backend_common.utils import str_to_datetime_if_parseable


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        match obj:
            case datetime.date() | datetime.datetime():
                return obj.isoformat()


class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.try_datetime, *args, **kwargs)

    @staticmethod
    def try_datetime(d: dict):
        ret = {}
        for key, value in d.items():
            match value:
                case str():
                    ret[key] = str_to_datetime_if_parseable(value)
                case _:
                    ret[key] = value
        return ret
