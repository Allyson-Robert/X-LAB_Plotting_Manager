from typing import Callable


class ScatterDataTest:
    def __init__(self):
        self.scatterdata = None

    def test_init(self, label, scatterdata: Callable):
        self.scatterdata = scatterdata(label)
        return True

    def test_readfile(self, path):
        self.scatterdata.read_file(path)
        return True

    def test_data(self, observables):
        for observable in observables:
            self.scatterdata.get_data(observable)

        return True

    def test_units(self, observables):
        for observable in observables:
            self.scatterdata.get_units(observable)

        return True
