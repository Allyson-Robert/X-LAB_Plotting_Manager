from json import JSONEncoder


class FilesetJSONEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
