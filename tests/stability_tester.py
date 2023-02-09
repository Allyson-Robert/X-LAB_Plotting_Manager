from experiment.stability import Stability
from fileset.fileset import Fileset

test_fileset = Fileset("2023-02-07")
test_fileset.construct_structured_filepaths('G:\\Shared drives\\X-LAB - Team Drive\\X-members\\Jeroen Hustings\\'
                                            'Data\\Sunbrick\\Data\\20220710')
test_fileset.set_device('Sunbrick')
test_fileset.set_name('Sunbrick IV test')

test_stability = Stability()
test_stability.set_data(test_fileset)
test_stability.plot_four(title="Test title", legend="Test legend")
