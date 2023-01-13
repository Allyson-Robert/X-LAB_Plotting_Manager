from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import json
import csv


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
        for key in files:
            self.data[key] = {}
            if type(files[key]) == dict:
                for filename in files[key]:
                    if type(files[key][filename]) == str:
                        try:
                            self.data[key][filename] = self.read_data(files[key][filename])
                        except Exception as e:
                            print(f"Reading file {filename} failed: {e}")
            elif type(files[key]) == str:
                try:
                    self.data[key] = self.read_data(files[key])
                except Exception as e:
                    print(f"Reading file {filename} failed: {e}")

    def read_data(self, filename):
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

        with open(filename) as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            voltage = []
            current = []
            for [i, j] in reader:
                if i and j:
                    voltage.append(float(i))
                    current.append(float(j))

        datadict['xdata'] = voltage
        datadict['ydata'] = current

        self.determine_crossings(datadict)
        self.determine_mpp(datadict)

        return datadict

    def determine_crossings(self, dataset):
        size = len(dataset['xdata'])
        isc_found = False
        isc = 0
        voc_found = False
        voc = 0
        rsh = 0
        rs = 0

        # Crop the curves as well
        start_idx = 0
        end_idx = 0

        # Search for Voc and Isc
        for i in range(1, size):
            if isc_found and voc_found:
                dataset['Voc'] = voc
                dataset['Isc'] = isc

                dataset['voltage'] = dataset['xdata'][start_idx:end_idx]
                dataset['current'] = dataset['ydata'][start_idx:end_idx]

                dataset['Rsh'] = rsh
                dataset['Rs'] = rs

                return 0

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
                isc = np.interp(0, xp, yp)
                rsh = (voltage-prev_voltage)/(current - prev_current)

            # Voc located at the x crossing, current will turn positive there
            if (prev_current < 0) and (current > 0):
                voc_found = True
                end_idx = i + 1
                voc = np.interp(0, yp, xp)
                rs = (voltage-prev_voltage)/(current - prev_current)

    def determine_mpp(self, dataset):
        # Determine MPP within the Isc - Voc range of the power curve, save MPP and index
        pwrdata = [abs(dataset['voltage'][i] * dataset['current'][i]) for i in range(len(dataset['voltage']))]
        dataset['power'] = pwrdata
        maxpwr = max(pwrdata)
        maxpwridx = pwrdata.index(maxpwr)
        dataset['maxpwr'] = [maxpwridx, maxpwr]
        dataset['mpp'] = {
            'v': dataset['voltage'][maxpwridx],
            'i': dataset['current'][maxpwridx],
            'p': maxpwr,
            'r': abs(dataset['voltage'][maxpwridx]/dataset['current'][maxpwridx])
        }

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
                x=dataset['xdata'],
                y=dataset['ydata'],
                mode='lines',
                name=dataset['label']
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
                showlegend=False
            ))
            fig.add_trace(go.Scatter(
                x=[0],
                y=[dataset['Isc']],
                mode='markers',
                marker_color='red',
                # symbol_sequence=['x-thin'],
                showlegend=False
            ))
            fig.add_trace(go.Scatter(
                x=[dataset['Voc']],
                y=[0],
                mode='markers',
                marker_color='blue',
                # marker_symbol='x-thin',
                showlegend=False
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
        fig['layout']['xaxis']['title'] = 'Time (hrs)'
        fig['layout']['yaxis']['title'] = 'I_sc (A)'

        fig['layout']['xaxis2']['title'] = 'Time (in hrs)'
        fig['layout']['yaxis2']['title'] = 'V_oc (V)'

        fig['layout']['xaxis3']['title'] = 'Time (in hrs)'
        fig['layout']['yaxis3']['title'] = 'Fill Factor'

        fig['layout']['xaxis4']['title'] = 'Time (hrs)'
        fig['layout']['yaxis4']['title'] = 'Efficiency'

        fig.update_layout(title_text=title)
        return fig

    def plot_stability(self, title):
        # Prep the plotting area
        fig = self.four_param_plot_area(title)

        # Grab the values for Isc, Voc, FF and eff from the data
        currents = {}
        voltages = {}
        fills = {}
        efficiencies = {}
        times = {}
        for series in self.data:
            currents[series] = []
            voltages[series] = []
            fills[series] = []
            efficiencies[series] = []
            times[series] = [0]
            for point in self.data[series]:
                currents[series].append(self.data[series][point]["Isc"])
                voltages[series].append(self.data[series][point]["Voc"])
                fills[series].append(self.data[series][point]["FF"])
                # efficiencies[series].append(self.data[series][point]["eff"])
                efficiencies[series].append(0)
                times[series].append(times[series][-1]+1)

            fig.add_trace(
                go.Scatter(x=times[series], y=currents[series]),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=times[series], y=voltages[series]),
                row=1, col=2
            )
            fig.add_trace(
                go.Scatter(x=times[series], y=fills[series]),
                row=2, col=1
            )
            fig.add_trace(
                go.Scatter(x=times[series], y=efficiencies[series]),
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
            prunedset =  {k: self.data[set][k] for k in self.data[set].keys() - {'xdata', 'ydata', 'voltage', 'current', 'power'}}
            return json.dumps(prunedset,
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            )