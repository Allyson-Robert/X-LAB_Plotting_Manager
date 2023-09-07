from plugins.data.data_types.scatter_data.absorbance_scatter import AbsorbanceData
from tests.datatype_tests.scatterdata_test import ScatterDataTest

path = "G:\\My Drive\\Data\\DW2000 - UVvis\\2022\\05-May\\2022-05-03_Aluminum_cuvettes_AB.csv"
label = "test label"
observables = ['label', 'wavelength', 'absorbance']

test = ScatterDataTest()
test.test_init(label, AbsorbanceData)
test.test_readfile(path)
test.test_data(observables)
test.test_units(observables)