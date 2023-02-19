from experiment.dw2000 import DW2000
from fileset.fileset import Fileset

test_fileset = Fileset("2023.02.07_11.09.12", "2023.02.07_11.09.12")
test_fileset.add_filepath(
    path="G:\\My Drive\\Data\\DW2000 - UVvis\\2022\\05-May\\2022-05-03_Aluminum_cuvettes_BA.csv",
    label='test BA'
)
test_fileset.add_filepath(
    path = "G:\\My Drive\\Data\\DW2000 - UVvis\\2022\\05-May\\2022-05-03_Aluminum_cuvettes_AB.csv",
    label='test AB'
)
test_fileset.set_device('DW2000')
test_fileset.set_name('DW2000 Absorbance test')
test_fileset.set_structure_type("flat")

test_dw2000 = DW2000()
test_dw2000.set_data(test_fileset)
test_dw2000.normal_plot(title="Test title", legend="Test legend")

