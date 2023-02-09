from data.collections.scatter_collections.iv_scatter_collection import IVScatterCollection
from plotter.iv_plotter import IVPlotter
from plotter.pv_plotter import PVPlotter


def test_iv_plotter(test_collection):
    test_plot = IVPlotter(title="Test title", legend_title="Sample")
    test_plot.ready_plot()
    test_plot.draw_plot(test_collection)
    return True


def test_pv_plotter(test_collection):
    test_plot = PVPlotter(title="Test title", legend_title="Sample")
    test_plot.ready_plot()
    test_plot.draw_plot(test_collection)
    return True


test_data = {'test': 'G:\\My Drive\\Data\\Sunbrick\\2023\\01-January\\20_12_2022_Long-term_IV\\Position_1\\IV_2023_01_02_22_40_50.txt'}
test_collection = IVScatterCollection(test_data)
print(test_iv_plotter(test_collection))
print(test_pv_plotter(test_collection))
