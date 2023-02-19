from data.datatypes.scatter_data.absorbance_scatter import AbsorbanceScatterData
from tests.datatype_tests.scatterdata_test import ScatterDataTest

path = "G:\\My Drive\\Data\\DW2000 - UVvis\\2022\\05-May\\2022-05-03_Aluminum_cuvettes_AB.csv"
label = "test label"
observables = ['label', 'wavelength', 'absorbance']

test = ScatterDataTest()
test.test_init(label, AbsorbanceScatterData)
test.test_readfile(path)
test.test_data(observables)
test.test_units(observables)