from plugins.data.data_processors.scatter_data.iv_data_processor import IVScatterDataProcessor
from plugins.data.data_types.scatter_data.iv_scatter import IVData
import traceback


def test_init(iv_data: IVData):
    return IVScatterDataProcessor(iv_data)


def test_get_functions(iv_processor: IVScatterDataProcessor):
    return iv_processor.get_allowed_observables()


def test_get_data(iv_processor, observable):
    return iv_processor.get_data(observable)


path = "G:\\My Drive\\Data\\Sunbrick\\2023\\01-January\\20_12_2022_Long-term_IV\\Position_1\\IV_2023_01_02_22_40_50.txt"
label = "test curve"
test_data = IVData(label)
test_data.read_file(path)

processor = test_init(test_data)
errors = "\n"
outputs = {}
for function in test_get_functions(processor):
    try:
        outputs[function] = test_get_data(processor, function)
        print(f"get_data({function}) succesful")
    except Exception:
        errors += f"get_data({function}) failed. Error {traceback.format_exc()}\n"
print(errors)
