from data.datatypes.scatter_data.scatter import ScatterData


def get_data(scatter_data: ScatterData, observable: str) -> list:
    assert isinstance(scatter_data, ScatterData)

    if scatter_data.raw_data[observable] is not None:
        if observable in scatter_data._allowed_observables:
            return scatter_data.raw_data[observable]['data']
        else:
            raise ValueError(f"AbsorbanceScatterData does not contain {observable} data")
    else:
        raise ValueError(f"Data has not been read from file for {self}")


def get_units(scatter_data: ScatterData, observable: str) -> str:
    get_data(observable)
    return scatter_data.raw_data[observable]['units']