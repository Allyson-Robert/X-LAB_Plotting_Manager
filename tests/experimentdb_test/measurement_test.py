from experimentdb.measurement import Measurement


def test_measurement(filepath: str, label: str, colour: str):
    m = Measurement(filepath, label)
    m.set_colour(colour)

    print(m.get_label())
    print(m.get_location())
    print(m.get_datetime())
    print(m.get_colour())

test_measurement(
    "G:/My Drive/Data/Sunbrick/2023/01-January/test/Position_1/IV_2022_12_20_09_29_06.txt",
    "test label",
    "white"
)
