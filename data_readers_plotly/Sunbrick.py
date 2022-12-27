import numpy as np
import csv
import json
import plotly.graph_objects as go


class Sunbrick:
    """
    A class to read in data from the sunbrick setup. The plots can be of a single measurement of multiple cells or can
    show the time evolution of cell properties.
    Single measurement plot types:
        - IV curves
        - PV curves
    Time evolution plot types:
        - FF
        - MPP
        - PCE
        - Isc/Jsc
        - Voc
    """
    def __init__(self, files):
        self.data = []
        for file in files:
            voltage, current = self.read_data(file[0])

            self.data.append({
                'label': '',
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
            })
            self.data[-1]['label'] = file[1]
            self.data[-1]['xdata'] = voltage
            self.data[-1]['ydata'] = current

            self.determine_crossings(self.data[-1])
            self.determine_mpp(self.data[-1])

    def read_data(self, filename):
        with open(filename) as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            voltage = []
            current = []
            power = []
            for [i, j] in reader:
                if i and j:
                    voltage.append(float(i))
                    current.append(float(j))
        return voltage, current

    def determine_crossings(self, set):
        size = len(set['xdata'])
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
                set['Voc'] = voc
                set['Isc'] = isc

                set['voltage'] = set['xdata'][start_idx:end_idx]
                set['current'] = set['ydata'][start_idx:end_idx]

                set['Rsh'] = rsh
                set['Rs'] = rs

                return 0

            prev_voltage = set['xdata'][i-1]
            voltage = set['xdata'][i]

            prev_current = set['ydata'][i-1]
            current = set['ydata'][i]

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

    def determine_mpp(self, set):
        # Determine MPP within the Isc - Voc range of the power curve, save MPP and index
        pwrdata = [abs(set['voltage'][i] * set['current'][i]) for i in range(len(set['voltage']))]
        # print(pwrdata)
        set['power'] = pwrdata
        maxpwr = max(pwrdata)
        maxpwridx = pwrdata.index(maxpwr)
        set['maxpwr'] = [maxpwridx, maxpwr]
        set['mpp'] = {
            'v': set['voltage'][maxpwridx],
            'i': set['current'][maxpwridx],
            'p': maxpwr,
            'r': abs(set['voltage'][maxpwridx]/set['current'][maxpwridx])
        }

        set['FF'] = maxpwr/(set['Voc']*set['Isc'])

        return 0

    def plot_fulliv(self, title):
        fig = go.Figure()
        fig.update_layout(
            title={
                'text': title,
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Voltage (V)",
            yaxis_title="Current (A)",
            legend_title="Sample",
            font=dict(
                family="Open Sans",
                size=18,
                color="RebeccaPurple"
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
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

        for set in self.data:
            fig.add_trace(go.Scatter(
                x=set['xdata'],
                y=set['ydata'],
                mode='lines',
                name=set['label']
            ))
        fig.show()
        return "Full IV curve opened in browser"

    def plot_iv(self, title, presentation=False):
        fig = go.Figure()
        fig.update_layout(
            title={
                'text': title,
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Voltage (V)",
            yaxis_title="Current (A)",
            legend_title="Sample",
            font=dict(
                family="Open Sans",
                size=18,
                color="RebeccaPurple"
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
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
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        if presentation:
            line = go.scatter.Line(width=5)
            fig.update_xaxes(linewidth=4)
            fig.update_yaxes(linewidth=4)
            fig.update_xaxes(gridwidth=2)
        else:
            line = None

        for set in self.data:
            fig.add_trace(go.Scatter(
                x=set['voltage'],
                y=set['current'],
                mode='lines',
                name=set['label'],
                line=line
            ))
            fig.add_trace(go.Scatter(
                x=[set['voltage'][set['maxpwr'][0]]],
                y=[set['current'][set['maxpwr'][0]]],
                mode='markers',
                marker_color='black',
                showlegend=False
            ))
            fig.add_trace(go.Scatter(
                x=[0],
                y=[set['Isc']],
                mode='markers',
                marker_color='red',
                # symbol_sequence=['x-thin'],
                showlegend=False
            ))
            fig.add_trace(go.Scatter(
                x=[set['Voc']],
                y=[0],
                mode='markers',
                marker_color='blue',
                # marker_symbol='x-thin',
                showlegend=False
            ))
        fig.show()
        return "Truncated IV curve opened in browser"

    def plot_pv(self, title):
        fig = go.Figure()
        fig.update_layout(
            title={
                'text': title,
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Voltage (V)",
            yaxis_title="Power (W)",
            legend_title="Sample",
            font=dict(
                family="Open Sans",
                size=18,
                color="RebeccaPurple"
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
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

        for set in self.data:
            fig.add_trace(go.Scatter(
                x=set['voltage'],
                y=set['power'],
                mode='lines',
                name=set['label']
            ))
            fig.add_trace(go.Scatter(
                x=[set['voltage'][set['maxpwr'][0]]],
                y=[set['power'][set['maxpwr'][0]]],
                mode='markers',
                marker_color='black',
                showlegend=False
            ))
        fig.show()
        return "Power curve opened in browser"

    def print(self):
        for set in self.data:
            prunedset =  {k: set[k] for k in set.keys() - {'xdata', 'ydata', 'voltage', 'current', 'power'}}
            print(json.dumps(prunedset,
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            ))