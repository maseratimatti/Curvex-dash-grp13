import dash
from dash import dcc
from dash import html 
from dash.dependencies import Input, Output, State
import plotly.express as px

import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/maseratimatti/Curvex-dash-grp13/main/Curvexdashdata.csv") #måske brug sep=';'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Målings Rapport for bruger 113", style={"textAlign":"center"}),
    html.Hr(),
    html.P("Vælg hjernefrekvens data:"),
    html.Div(html.Div([
        dcc.Dropdown(id='type', clearable=False,
                     value="Gamma",
                     options=[{'label': x, 'value': x} for x in
                              df["type"].unique()]),
    ],className="two columns"),className="row"),

    html.Div(id="output-div", children=[]),
])


@app.callback(Output(component_id="output-div", component_property="children"),
              Input(component_id="type", component_property="value"),
)
def make_graphs(type_chosen):
    # HISTOGRAM
    df_hist = df[df["type"]==type_chosen]
    fig_hist = px.histogram(df_hist, x="Værdi")
    fig_hist.update_xaxes(categoryorder="total descending")

    return [
        html.Div([
            html.Div([dcc.Graph(figure=fig_hist)], className="six columns"),
        ], className="row"),
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
