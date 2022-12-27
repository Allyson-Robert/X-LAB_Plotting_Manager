import csv
import plotly.graph_objects as go
import re

class PtiText:
    """ A class to read in data from the pti setup"""

    def __init__(self, title):
        self.fig = go.Figure()
        self.fig.update_layout(
            xaxis_title="Wavelength (nm)",
            yaxis_title="Fluorescence (a.u.)",
            legend_title="Sample",
            title={
                'text': title,
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
        )
        self.fig.update_layout(
            font=dict(
                family="Open Sans",
                size=18,
                color="RebeccaPurple"
            )
        )

        self.fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        self.fig.update_xaxes(
            showline=True,
            linewidth=2,
            linecolor='black',
            ticks="outside",
            showgrid=True,
            gridwidth=1,
            gridcolor='black'
        )

        self.fig.update_yaxes(
            showline=True,
            linewidth=2,
            linecolor='black',
            ticks="outside",
            showgrid=True,
            gridwidth=1,
            gridcolor='black',
            showticklabels=False
        )

    # def set_title(self, title_string):
    #     print(title_string)
    #     [det_nr, ex, em_scan_lower, em_scan_upper] = re.findall(r'\d+', title_string)
    #     self.fig.update_layout(
    #         title={
    #             'text': f'{self.title} (excited at {ex} nm)',
    #             'y': 0.9,
    #             'x': 0.5,
    #             'xanchor': 'center',
    #             'yanchor': 'top'
    #         },
    #     )

    def read_data(self, filename):
        # Two options for the contents of the file
        # Either two columns with straight up data
        # Or four with additional metadata in the first column
        with open(filename) as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            line = next(reader)
            if len(line) == 2:
                return self.read_2c_data(filename)
            elif len(line) == 4:
                return self.read_4c_data(filename)
            else:
                return None

    def read_2c_data(self, filename):
        data = [[], []]
        with open(filename) as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for [x, y] in reader:
                if x and y:
                    x = float(x.replace(',', '.'))
                    y = float(y.replace(',', '.'))
                    if x > 0 and y > 0:
                        data[0].append(x)
                        data[1].append(y)
        return data

    def read_4c_data(self, filename):
        data = [[], []]
        with open(filename) as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for [x, y, z, w] in reader:
                if 'D1' not in x:
                    continue
                if z and w:
                    z = float(z.replace(',', '.'))
                    w = float(w.replace(',', '.'))
                    if z > 0 and w > 0:
                        data[0].append(z)
                        data[1].append(w)
        return data

    def plot(self, files):
        for file in files:
            data = file[0]
            label = file[1]

            data = self.read_data(data)
            if data != None:
                self.fig.add_trace(go.Scatter(
                    x=data[0],
                    y=data[1],
                    mode='lines',
                    name=label
                ))

        self.fig.show()
        return "Fluorescence spectra opened in browser"
