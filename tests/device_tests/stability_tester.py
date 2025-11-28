from device.stability import Stability
from dataset_manager.dataset import DataSet

print("Building dataset_manager")
test_fileset = DataSet("2023-02-07")
test_fileset.construct_structured_filepaths('G:\\Shared drives\\X-LAB - Team Drive\\X-members\\Jeroen Hustings\\'
                                            'Data\\Sunbrick\\Data\\20220710')
test_fileset.set_device('Sunbrick')
test_fileset.set_name('Sunbrick IV test')

print("Initialising stability")
test_stability = Stability()

print("Setting stability data to dataset_manager")
test_stability.set_data(test_fileset)

print("Making stability four-parameter plot")
test_stability.plot_four(title="Test title", legend="Test legend")
