from data.collections.scatter_collections.iv_scatter_collection import IVScatterCollection
from plotter.iv_plotter import IVPlotter

test_data = {'test': 'G:\\My Drive\\Data\\Sunbrick\\2023\\01-January\\20_12_2022_Long-term_IV\\Position_1\\IV_2023_01_05_14_41_07.txt'}
test_collection = IVScatterCollection(test_data)
test_plot = IVPlotter(title="Test title", legend_title="Sample")
test_plot.ready_plot()
test_plot.draw_plot(test_collection)