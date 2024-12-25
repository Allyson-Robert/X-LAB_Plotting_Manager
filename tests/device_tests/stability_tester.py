from device.stability import Stability
from dataspec_manager.dataspec import DataSpec

print("Building dataspec_manager")
test_fileset = DataSpec("2023-02-07")
test_fileset.construct_structured_filepaths('G:\\Shared drives\\X-LAB - Team Drive\\X-members\\Jeroen Hustings\\'
                                            'Data\\Sunbrick\\Data\\20220710')
test_fileset.set_device('Sunbrick')
test_fileset.set_name('Sunbrick IV test')

print("Initialising stability")
test_stability = Stability()

print("Setting stability data to dataspec_manager")
test_stability.set_data(test_fileset)

print("Making stability four-parameter plot")
test_stability.plot_four(title="Test title", legend="Test legend")
