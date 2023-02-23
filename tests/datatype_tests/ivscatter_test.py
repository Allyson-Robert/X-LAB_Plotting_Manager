from data.datatypes.scatter_data.iv_scatter import IVData
from tests.datatype_tests.scatterdata_test import ScatterDataTest


path = "G:\\My Drive\\Data\\Sunbrick\\2023\\01-January\\20_12_2022_Long-term_IV\\Position_1\\IV_2023_01_02_22_40_50.txt"
label = "test label"
observables = ['label', 'wavelength', 'absorbance']

test = ScatterDataTest()
test.test_init(label, IVData)
test.test_readfile(path)
test.test_data(observables)
test.test_units(observables)