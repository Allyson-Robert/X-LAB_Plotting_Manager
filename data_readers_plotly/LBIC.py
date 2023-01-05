import csv
import numpy as np
import plotly.graph_objects as go


class LBIC:
    """ A class to read in data from the pti setup"""

    def __init__(self, title):
        self.fig = go.Figure()
        self.title = title
        self.x = []
        self.y = []
        self.z = []

    def style_image(self, profiles=None):
        self.fig.update_layout(
            yaxis_scaleanchor="x",
            width=800,
            height=800,
            title={
                'text': self.title,
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            yaxis_title="Size (mm)",
            font=dict(
                family="Open Sans",
                size=18,
                color="RebeccaPurple"
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        if profiles is not None:
            self.fig.update_yaxes(
                showspikes=True,
                spikemode="across",
                # spikesnap="cursor",
                spikethickness=0.5
            )
            self.fig.update_xaxes(
                showspikes=True,
                spikemode="across",
                # spikesnap="cursor",
                spikethickness=0.5
            )
        self.fig.update_xaxes(visible=False)
        self.fig['layout']['yaxis']['autorange'] = "reversed"

    def style_distribution(self):
        self.fig.update_layout(
            title={
                'text': self.title,
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Current (A)",
            yaxis_title="Counts (a.u.)",
            font=dict(
                family="Open Sans",
                size=18,
                color="RebeccaPurple"
            ),
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
        )

    def style_profile(self):
        self.fig.update_layout(
            title={
                'text': self.title,
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Position (mm)",
            yaxis_title="Current (A)",
            font=dict(
                family="Open Sans",
                size=18,
                color="RebeccaPurple"
            ),
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
        )

    def read_data(self, filename):
        if self.x and self.y and self.z:
            self.fig = go.Figure()
            return True

        with open(filename) as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            self.x = [float(intensity.replace(',', '.')) for intensity in next(reader)][1:] # Skip first line for now

            self.y = []
            self.z = []
            for line in reader:
                self.y.append(float(line[0].replace(',', '.')))
                row = [float(intensity.replace(',', '.')) for intensity in line[1:]]
                if np.count_nonzero(row):
                    self.z.append(row)
        return True

    def show_image(self, file, range=None, color='turbid', profiles=None):
        # Only one image can be shown
        if len(file) != 1:
            return "Err: Exactly one image can be generated at a time"

        # Grab filename
        filename = next(iter(file.values()))
        self.style_image(profiles)
        self.read_data(filename)

        # Set range
        if range is None:
            range = [0, 0]
            zauto = True
        else:
            zauto = False

        # Generate image as heatmap including the colorscale
        self.fig.add_trace(
            go.Heatmap(
                x=self.x,
                y=self.y,
                z=self.z,
                zauto=zauto,
                zmin=range[0],
                zmax=range[1],
                colorscale=color,
                reversescale=True,
                colorbar=dict(title='I (A)'),
                hovertemplate='x (mm): %{x}<br>y (mm): %{y}<br>I (A): %{z}<extra></extra>'
            )
        )
        self.fig.show()
        return "Image opened in browser"

    def plot_intensities(self, file):
        # Only one dataset can be parsed
        if len(file) != 1:
            return "Err: Exactly one dataset can be parsed at a time"

        # Grab filename
        filename = next(iter(file.values()))
        self.read_data(filename)
        self.style_distribution()

        # Compute intensity histogram
        data = [zval for zrow in self.z for zval in zrow]
        self.fig.add_trace(
            go.Histogram(x=data, histnorm='probability')
        )
        self.fig.show()
        return "Plot opened in browser"

    def plot_horiz_profile(self, file, ycoord=None):
        # Only one dataset can be parsed
        if len(file) != 1:
            return "Err: Exactly one profile can be produced at a time"

        # Grab filename
        filename = next(iter(file.values()))
        self.read_data(filename)
        self.style_profile()

        # Find nearest to given y value
        profile_index = np.abs([yval - ycoord for yval in self.y]).argmin()
        data = self.z[profile_index]

        # Plot the horizontal profile
        self.fig.add_trace(go.Scatter(
            x=self.x,
            y=data,
            mode='lines'
        ))
        self.fig.show()
        return "Profile opened in browser"