from Data import Data


class IVData(Data):
    def __init__(self, current, voltage, label):
        self.label = label
        self.current = current
        self.voltage = voltage

    def get_label(self):
        return self.label

    def get_data(self, observable):
        if observable == "current":
            return self.current
        elif observable == "voltage":
            return self.voltage
        else:
            raise ValueError()

    @classmethod
    def read_from_file(cls, filename):
        with open(filename) as file:
            current = [0]
            voltage = [1]
        return cls.__init__(current, voltage)