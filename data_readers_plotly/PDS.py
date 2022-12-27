import csv
import plotly.graph_objects as go


class DataPoint:
    def __init__(self, data):
        self.time = data[0]
        self.energy = float(data[1])
        self.wavelength = float(data[2])

        self.b_sig = float(data[3])
        self.b_sig_err = float(data[4])
        self.b_deg = float(data[5])
        self.b_deg_error = float(data[6])

        self.a_sig = float(data[7])
        self.a_sig_err = float(data[8])
        self.a_deg = float(data[9])
        self.a_deg_error = float(data[11])

        self.signal = self.b_sig/self.a_sig
        self.signal_error = self.signal*(self.b_sig_err/self.b_sig + self.a_sig_err/self.a_sig)

        self.result = {
            "energy": self.energy,
            "wavelength": self.wavelength,
            "signal": self.signal,
            "error": self.signal_error
        }

    def __str__(self):
            return f"DataPoint(time:{self.time}, wavelength:{self.wavelength}, input:{self.b_sig}, reference:{self.a_sig}, signal:{self.signal})"

class PDS:
    """ A class to read in data from the pti setup"""

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
            yaxis_title="Absorbance (a.u.)",
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

        # self.fig.update_xaxes(
        #     showgrid=True,
        #     gridwidth=1,
        #     gridcolor='black'
        # )
        #
        # self.fig.update_yaxes(
        #     showgrid=True,
        #     gridwidth=1,
        #     gridcolor='black'
        # )

    def read_data(self, filename):
        with open(filename) as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            data = [[], [], []]

            # The first 10 lines are headers
            for i in range(10):
                next(reader)

            for line in reader:
                dp = DataPoint(line)
                data[0].append(dp.result["wavelength"])
                data[1].append(dp.result["signal"])
                data[2].append(dp.result['error'])
        return data

    def plot(self, files, normalised=False, presentation=False):
        if presentation:
            line = go.scatter.Line(width=5)
            self.fig.update_xaxes(linewidth=4)
            self.fig.update_yaxes(linewidth=4)
            self.fig.update_xaxes(gridwidth=2)
        else:
            line = None

        for file in files:
            filename = file[0]
            label = file[1]

            data = self.read_data(filename)
            x_data = data[0]
            if normalised:
                norm = max(data[1])
                y_data = [y/norm for y in data[1]]
            else:
                y_data = data[1]

            dy_data = data[2]
            y_upper = []
            y_lower = []
            for i in range(len(y_data)):
                y_upper.append(y_data[i] + dy_data[i])
                y_lower.append(y_data[i] - dy_data[i])

            # Hacky way to remove title row
            self.fig.add_trace(go.Scatter(
                x=x_data,
                y=y_data,
                error_y=dict(
                    type='data',
                    array=dy_data,
                    visible=True),
                mode='lines',
                name=label,
                line=line
            ))
        # Set marker line color to same color as marker for each trace
        self.fig.show()
        return "PDS Spectra opened in browser"
