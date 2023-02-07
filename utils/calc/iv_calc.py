from data.datatypes.scatter_data.iv_scatter import IVScatterData


def calc_iv_power(iv_data: IVScatterData) -> list:
    assert isinstance(iv_data, IVScatterData)
    current = iv_data.get_data("current")
    voltage = iv_data.get_data("voltage")
    power = []
    for i, v in zip(current, voltage):
        power.append(i*v)
    return power
