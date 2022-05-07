import dash
from dash import dcc
from dash import html 
from dash.dependencies import Input, Output, State

import dash_auth

import plotly.express as px

import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/maseratimatti/Curvex-dash-grp13/main/Curvexdashdata.csv", sep=';') 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

auth = dash_auth.BasicAuth(
    app,
    {'113': 'KEA'}
)

app.layout = html.Div([
    html.H1("Curvex Rapport For Bruger: 113", style={"textAlign":"center"}),
    html.Hr(),
    html.P("Vælg hjernefrekvens data:"),
    html.Div(html.Div([
        dcc.Dropdown(id='Frekvens', clearable=False,
                     value="Gamma",
                     options=[{'label': x, 'value': x} for x in
                              df["Frekvens"].unique()]),
    ],className="two columns"),className="row"),

    html.Div(id="output-div", children=[]),
])


@app.callback(Output(component_id="output-div", component_property="children"),
              Input(component_id="Frekvens", component_property="value"),
)
def make_graphs(Frekvens_chosen):

    df_hist = df[df["Frekvens"]==Frekvens_chosen]
    fig_hist = px.histogram(df_hist, x="Værdi")
    fig_hist.update_xaxes(categoryorder="total descending")

    df_line = df[df["Frekvens"]==Frekvens_chosen]
    fig_line = px.line(df_line,
        x="Tidspunkt", y="Måling", color='Frekvens', markers=True)

    return [
        html.Div([
            html.Div([dcc.Graph(figure=fig_hist)], className="six columns"),
        ], className="row"),
        html.H2("Tidspunkter", style={"textAlign":"center"}),
        html.Hr(),
        html.Div([
            html.Div([dcc.Graph(figure=fig_line)], className="twelve columns"),
        ], className="row"),
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
