import csv
import pandas as pd
import plotly.graph_objects as go


class DW2000:
    """
    A class to read in data from the dw2000 setup. It can read both excel and csv files regardless of the delimiter
    """

    def __init__(self, title):
        self.fig = go.Figure()
        self.fig.update_layout(
            title={
                'text': title,
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
        )
        self.fig.update_layout(
            xaxis_title="Wavelength (nm)",
            yaxis_title="Optical Density",
            legend_title="Sample",
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
            ticks="outside"
        )

        self.fig.update_yaxes(
            showline=True,
            linewidth=2,
            linecolor='black',
            ticks="outside"
        )

        self.fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='black'
        )

        self.fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='black'
        )

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

    def plot(self, files, normalised=False):
        if len(files) == 0:
            return "Err: Must select file"
        for file in files:
            filename = file[0]
            label = file[1]
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
        return "Plot opened in browser"

    def plot_rainbow(self, files):
        if len(files) == 0:
            return "Err: Must select file"
        elif len(files) != 1:
            return "Err: Rainbow plot only available for single plot"

        filename = files[0][0]
        data = self.read_data(filename)
        self.fig.add_trace(go.Scatter(
            x=data[0],
            y=data[1],
            mode='markers',
            marker={
                'color': data[0],
                'cmin': 400,
                'cmax': 700,
                'colorscale': 'Rainbow',
                'showscale': True,
                'size': 6
            }
        ))
        self.fig.show()
        return "Plot opened in browser"
