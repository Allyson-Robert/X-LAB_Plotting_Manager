from device.sunbrick import Sunbrick
from dataspec_manager.dataspec import DataSpec

test_fileset = DataSpec("2023-02-07")
test_fileset.add_filepath(
    path='G:\\My Drive\\Data\\Sunbrick\\2023\\01-January\\20_12_2022_Long-term_IV\\Position_1\\'
         'IV_2023_01_05_14_41_07.txt',
    label='test data'
)
test_fileset.add_filepath(
    path='G:\\My Drive\\Data\\Sunbrick\\2023\\01-January\\20_12_2022_Long-term_IV\\Position_1\\'
         'IV_2023_01_05_13_41_07.txt',
    label='test data 2'
)
test_fileset.set_device('Sunbrick')
test_fileset.set_name('Sunbrick IV test')

test_sunbrick = Sunbrick()
test_sunbrick.set_data(test_fileset)
test_sunbrick.plot_fulliv(title="Test title", legend="Test legend")
test_sunbrick.print_parameters()
