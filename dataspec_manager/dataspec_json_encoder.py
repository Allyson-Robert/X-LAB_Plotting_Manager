from json import JSONEncoder
import datetime


class DataSpecJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y.%m.%d_%H.%M.%S")
        else:
            return o.__dict__
