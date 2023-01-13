import plotly.graph_objects as go
import pandas as pd
import csv


class Generic:
    """ A class to read in data from the pti setup"""

    def __init__(self,
                 title,
                 x_title="Horizontal Axis (a.u.)",
                 y_title="Vertical axis (a.u.)",
                 l_title="Sample"
                 ):

        # Prepare figure
        self.fig = go.Figure()
        self.fig.update_layout(
            title={
                'text': title,
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
        )
        self.fig.update_layout(
            xaxis_title=x_title,
            yaxis_title=y_title,
            legend_title=l_title,
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

        # Axes format
        self.fig.update_xaxes(
            showline=True,
            linewidth=2,
            linecolor='black',
            ticks="outside"
        )
        self.fig.update_yaxes(
            showline=True,
            linewidth=2,
            linecolor='black',
            ticks="outside"
        )

        # No Grid
        self.fig.update_xaxes(showgrid=False)
        self.fig.update_yaxes(showgrid=False)

    def read_data(self, filename):
        if 'xls' in filename.split('.')[-1]:
            return pd.read_excel(filename)
        return self.read_csv(filename)

    def read_csv(self, filename):
        # Retrieve the delimiter
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            sniffer = csv.Sniffer()
            sample = reader.__next__()[0]
            dialect = sniffer.sniff(sample)
            sep = dialect.delimiter

        # Actually start reading the file
        with open(filename) as csvfile:
            reader = csv.reader(csvfile, delimiter=sep)
            data = [[], []]
            for [x, y] in reader:
                if x and y:
                    data[0].append(float(x.replace(',', '.')))
                    data[1].append(float(y.replace(',', '.')))
        return data

    def plot(self, files, normalised=False, presentation=False):
        if len(files) == 0:
            return "Err: Must select file"
        for label in files:
            filename = files[label]
            data = self.read_data(filename)

            x_data = data[0]
            if normalised:
                norm = max(data[1])
                print(norm)
                y_data = [y/norm for y in data[1]]
            else:
                y_data = data[1]

            # Hacky way to remove title row
            self.fig.add_trace(go.Scatter(
                x=x_data[1:],
                y=y_data[1:],
                mode='lines',
                name=label
            ))

        self.fig.show()
        return "Generic plot opened in browser"
