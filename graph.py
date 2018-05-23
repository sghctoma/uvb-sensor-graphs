#!/usr/bin/env python3

import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import plotly
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State


colors = [
    "#1f77b4",
    "#7f7f7f",
    "#17becf",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#bcbd22"
]


app = dash.Dash(__name__)
app.layout = html.Div([
])


def main():
    data = []
    i = 0
    for datafile in os.listdir('data'):
        with open('data/' + datafile) as f:
            lines = f.readlines()
        # read wavelength/responsivity values
        x = [float(x.split(' ')[0]) for x in lines]
        y = [float(x.split(' ')[1]) for x in lines]
        
        # find wavelengths between 280 and 330
        tmp = [i for i,v in enumerate(x) if v>=280 and v<=330]

        # reduce data set to said wavelengths
        x = x[tmp[0]:tmp[-1]+1]
        y = y[tmp[0]:tmp[-1]+1]

        # normalize responsivity
        rmax = max(y)
        if rmax != 1.0:
            y = list(map(lambda x: x*1/rmax, y))

        data.append(go.Scatter(
            x = x,
            y = y,
            name = datafile.split('.')[0],
            mode = 'lines',
            line = dict(color=colors[i%len(colors)])
        ))
        i = i + 1
        
    layout = go.Layout(
        title = 'UVB sensor spectral responses',
        width = 1000,
        height = 1000,
        margin = dict(l=60, r=60, b=30, t=30),
        legend = dict(xanchor='right', yanchor='top'),
        yaxis = dict(fixedrange = True)
    )

    figure = go.Figure(layout=layout, data=data)
    app.layout.children.append(
        dcc.Graph(id='uvb-spectral-responses', figure=figure)
    )

    app.run_server(port=8060, debug=True)


if __name__ == '__main__':
    main()
