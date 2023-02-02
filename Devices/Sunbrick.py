from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import json
import csv


class Stability:
    """ Responsible for plotting stability datasets extracted from IV curves"""
    def __init__(self):
        pass

    def plot_stability(self, title, params=None):
        pass


class Sunbrick:
    """
        A class to read in data from the sunbrick setup. The plots can be of a single measurement of multiple cells or can
        show the time evolution of cell properties.
        Single measurement plot types:
            - IV curves (complete data or truncated)
            - PV curves
        Time evolution plot for stability measurements:
            - FF
            - PCE
            - Isc/Jsc
            - Voc
        Data sets should be dictionaries containing file paths as values. Dicts are allowed to be nested 1 level deep.
    """
    def __init__(self, files):
        self.data = {}

        # Check all files/dirs
        for key in files:
            self.data[key] = {}

            # If item is a dictionary (directory) unpack it
            if type(files[key]) == dict:
                for filename in files[key]:

                    # If a string (file) is found in the subdir, try reading it
                    if type(files[key][filename]) == str:
                        try:
                            self.data[key][filename] = self.read_data(files[key][filename])
                        except Exception as e:
                            print(files[key][filename])
                            print(f"Reading file {filename} failed: {e}")

            # If item is a string (file) try reading it
            elif type(files[key]) == str:
                try:
                    self.data[key] = self.read_data(files[key])
                except Exception as e:
                    print(files[key])
                    print(f"Reading file {files[key]} failed: {e}")

    def read_data(self, filepath):
        filename = filepath.split("/")[-2] + "/" + filepath.split("/")[-1]
        datadict = {
            'label': filename,
            'xdata': [],
            'ydata': [],
            'voltage': [],
            'current': [],
            'Isc': 0,
            'Voc': 0,
            'maxpwr': {},
            'mpp': [],
            'FF': 0,
            'Rsh': 0,
            'Rs': 0
        }

        with open(filepath) as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            voltage = []
            current = []
            for [i, j] in reader:
                if i and j:
                    voltage.append(float(i))
                    current.append(float(j))

        datadict['xdata'] = voltage
        datadict['ydata'] = current
        try:
            self.determine_crossings(datadict)
            self.determine_mpp(datadict)
        except Exception as e:
            print("Could not determine crossings or mpp")

        return datadict

    def determine_crossings(self, dataset):
        size = len(dataset['xdata'])
        isc_found = False
        isc = min(dataset['ydata'])
        voc_found = False
        voc = max(dataset['xdata'])
        rsh = 0
        rs = 0

        # Crop the curves as well
        start_idx = 0
        end_idx = size

        # Search for Voc and Isc
        for i in range(1, size):
            if isc_found and voc_found:
                break

            prev_voltage = dataset['xdata'][i-1]
            voltage = dataset['xdata'][i]

            prev_current = dataset['ydata'][i-1]
            current = dataset['ydata'][i]

            xp = [prev_voltage, voltage]
            yp = [prev_current, current]

            # Isc located at the y crossing, voltage will turn positive there
            if (prev_voltage < 0) and (voltage > 0):
                isc_found = True
                start_idx = i-1
                # Find zero-crossing by interpolating and setting voltage to zero
                isc = abs(np.interp(0, xp, yp))
                rsh = (voltage-prev_voltage)/(current - prev_current)

            # Voc located at the x crossing, current will turn positive there
            if (prev_current < 0) and (current > 0):
                voc_found = True
                end_idx = i + 1
                # Swap x-, and y-axes and find zero-crossing by interpolating and setting current to zero
                voc = np.interp(0, yp, xp)
                rs = (voltage-prev_voltage)/(current - prev_current)

        dataset['Voc'] = voc
        dataset['Isc'] = isc

        dataset['voltage'] = dataset['xdata'][start_idx:end_idx]
        dataset['current'] = dataset['ydata'][start_idx:end_idx]

        dataset['Rsh'] = rsh
        dataset['Rs'] = rs

        return 0

    def determine_mpp(self, dataset):
        # Compute pwr from V and I, shorten the range to exclude the boundaries,
        #     as the PMM is between Voc and Isc. Add leading and ending zeroes
        #     to make the length of voltage and power data match
        pwrdata = [0]
        for i in range(1, len(dataset['voltage'])-1):
            pwrdata.append(abs(dataset['voltage'][i] * dataset['current'][i]))
        dataset['power'] = pwrdata
        pwrdata.append(0)

        # Find maximum power, corresponding index and save to the dataset
        maxpwr = max(pwrdata)
        maxpwridx = pwrdata.index(maxpwr)
        dataset['maxpwr'] = [maxpwridx, maxpwr]
        dataset['mpp'] = {
            'v': dataset['voltage'][maxpwridx],
            'i': dataset['current'][maxpwridx],
            'p': maxpwr,
            'r': abs(dataset['voltage'][maxpwridx]/dataset['current'][maxpwridx])
        }
        # Compute fill factor
        dataset['FF'] = maxpwr/(dataset['Voc']*dataset['Isc'])

        return 0

    def prep(self, title, type='iv'):
        fig = go.Figure()
        fig.update_layout(
            title={
                'text': title,
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            legend_title="Sample",
            font=dict(
                family="Open Sans",
                size=18,
                color="RebeccaPurple"
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        if type == 'iv':
            fig.update_layout(
                xaxis_title="Voltage (V)",
                yaxis_title="Current (A)",
            )
        elif type == 'pv':
            fig.update_layout(
                xaxis_title="Voltage (V)",
                yaxis_title="Power (W)",
            )

        fig.update_xaxes(
            showline=True,
            linewidth=2,
            linecolor='black',
            ticks="outside"
        )

        fig.update_yaxes(
            showline=True,
            linewidth=2,
            linecolor='black',
            ticks="outside"
        )

        return fig

    def plot_fulliv(self, title):
        fig = self.prep(title)
        for dataset in self.data:
            fig.add_trace(go.Scatter(
                x=self.data[dataset]['xdata'],
                y=self.data[dataset]['ydata'],
                mode='lines',
                name=self.data[dataset]['label']
            ))
        fig.show()
        return "Full IV curve opened in browser"

    def plot_iv(self, title, presentation=False):
        fig = self.prep(title, presentation)

        if presentation:
            line = go.scatter.Line(width=5)
            fig.update_xaxes(linewidth=4)
            fig.update_yaxes(linewidth=4)
            fig.update_xaxes(gridwidth=2)
        else:
            line = None

        # TODO: This is incompatible with the new data structure
        for lbl in self.data:
            dataset = self.data[lbl]
            fig.add_trace(go.Scatter(
                x=dataset['voltage'],
                y=dataset['current'],
                mode='lines',
                name=dataset['label'],
                line=line
            ))
            fig.add_trace(go.Scatter(
                x=[dataset['voltage'][dataset['maxpwr'][0]]],
                y=[dataset['current'][dataset['maxpwr'][0]]],
                mode='markers',
                marker_color='black',
                name="MPP",
            ))
            fig.add_trace(go.Scatter(
                x=[0],
                y=[-dataset['Isc']],
                mode='markers',
                marker_color='red',
                name="Isc"
            ))
            fig.add_trace(go.Scatter(
                x=[dataset['Voc']],
                y=[0],
                mode='markers',
                marker_color='blue',
                name="Voc"
            ))
        fig.show()
        return "Truncated IV curve opened in browser"

    def four_param_plot_area(self, title):
        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=("A", "B", "C", "D")
        )

        # edit axis labels
        fig['layout']['xaxis']['title'] = '$Time ~(hrs)$'
        fig['layout']['yaxis']['title'] = '$I_{sc} ~(A)$'

        fig['layout']['xaxis2']['title'] = '$Time ~(hrs)$'
        fig['layout']['yaxis2']['title'] = '$V_{oc} ~(V)$'

        fig['layout']['xaxis3']['title'] = '$Time ~(hrs)$'
        fig['layout']['yaxis3']['title'] = '$Fill Factor$'

        fig['layout']['xaxis4']['title'] = '$Time ~(hrs)$'
        fig['layout']['yaxis4']['title'] = '$P_{max}$'

        fig.update_layout(title_text=title)
        fig.update_layout(legend_tracegroupgap=0)

        colours = px.colors.qualitative.Plotly

        return fig, colours

    def plot_stability(self, title):
        # Prep the plotting area
        fig, colours = self.four_param_plot_area(title)

        # Grab the values for Isc, Voc, FF and eff from the data
        currents = {}
        voltages = {}
        fills = {}
        max_power = {}
        times = {}
        for index, series in enumerate(self.data):
            currents[series] = []
            voltages[series] = []
            fills[series] = []
            max_power[series] = []
            times[series] = [0]
            for point in self.data[series]:
                currents[series].append(self.data[series][point]["Isc"])
                voltages[series].append(self.data[series][point]["Voc"])
                fills[series].append(self.data[series][point]["FF"])
                max_power[series].append(self.data[series][point]["maxpwr"][1])
                times[series].append(times[series][-1]+1)

            fig.add_trace(
                go.Scatter(
                    x=times[series],
                    y=currents[series],
                    legendgroup=series,
                    name=series,
                    marker=dict(color=colours[index % len(colours)])
                ),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(
                    x=times[series],
                    y=voltages[series],
                    legendgroup=series,
                    name=series,
                    showlegend=False,
                    marker=dict(color=colours[index % len(colours)])
                ),
                row=1, col=2
            )
            fig.add_trace(
                go.Scatter(
                    x=times[series],
                    y=fills[series],
                    legendgroup=series,
                    name=series,
                    showlegend=False,
                    marker=dict(color=colours[index % len(colours)])
                ),
                row=2, col=1
            )
            fig.add_trace(
                go.Scatter(
                    x=times[series],
                    y=max_power[series],
                    legendgroup=series,
                    name=series,
                    showlegend=False,
                    marker=dict(color=colours[index % len(colours)])
                ),
                row=2, col=2
            )
        fig.show()

        # Proceed with plotting
        return "Cell properties opened in browser"

    def plot_pv(self, title):
        fig = self.prep(title, type='pv')

        for lbl in self.data:
            dataset = self.data[lbl]
            fig.add_trace(go.Scatter(
                x=dataset['voltage'],
                y=dataset['power'],
                mode='lines',
                name=dataset['label']
            ))
            fig.add_trace(go.Scatter(
                x=[dataset['voltage'][dataset['maxpwr'][0]]],
                y=[dataset['power'][dataset['maxpwr'][0]]],
                mode='markers',
                marker_color='black',
                showlegend=False
            ))
        fig.show()
        return "Power curve opened in browser"

    def print(self):
        for set in self.data:
            prunedset = {k: self.data[set][k] for k in self.data[set].keys() - {'xdata', 'ydata', 'voltage', 'current', 'power'}}
            print(json.dumps(prunedset, sort_keys=True, indent=4, separators=(',', ': ')))
        return "Printed to pycharm"

    def generate_stability_file(self):
        pass