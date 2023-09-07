from plugins.plotter import ScatterDataPlotter


def test_iv_plotter(test_collection):
    test_plot = ScatterDataPlotter("Test title", "voltage", "current")
    test_plot.ready_plot(test_collection, legend_title="Sample")
    test_plot.draw_plot()
    return True


def test_pv_plotter(test_collection):
    test_plot = ScatterDataPlotter("Test title", "voltage", "power")
    test_plot.ready_plot(test_collection, legend_title="Sample")
    test_plot.draw_plot()
    return True


test_data = {'test': 'G:\\My Drive\\Data\\Sunbrick\\2023\\01-January\\20_12_2022_Long-term_IV\\Position_1\\IV_2023_01_02_22_40_50.txt'}
# TODO: Update, tester broken
test_collection = IVScatterCollection(test_data)
print(test_iv_plotter(test_collection))
print(test_pv_plotter(test_collection))
