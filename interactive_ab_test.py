import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy  as np
import plotly.offline as pyo
import plotly.figure_factory as ff
import dash_table
from scipy import stats
import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd


app=dash.Dash()

# groups randomly distributed
group_a = np.random.randn(100)
group_b = np.random.randn(100)+2

# mu interval:
mu=np.arange(0,5.5, 0.5)
# n sample size
n=[10, 30, 50, 100, 150]
# create distplot with initial size
colors = ['#3A4750', '#660066']
hist_data = [group_a, group_b]
group_labels = ['Group A', 'Group B']
fig = ff.create_distplot(hist_data, group_labels, bin_size=[0.2,0.2], colors=colors)
# statistics calculation
t_stat, p_value = stats.ttest_ind(group_a, group_b)

app.layout=html.Div([
          html.H1('Group distribution'),
          html.Div([
          html.H3('Choose N sample size:', style={'paddingRight':'30px'}),
          dcc.Dropdown(
          id='n_values',
          options=[{'label':i, 'value':i} for i in n],
          searchable=False
          )],style={'width':'48%', 'display': 'inline-block'}),
          html.Div([
           html.H3('Enter mean difference:', style={'paddingRight':'30px'}),
          dcc.Dropdown(
          id='mu_values',
          options=[{'label':j, 'value':j} for j in mu],
          searchable=False
          )],style={'width':'48%', 'display': 'inline-block'}),
          html.Div([

          dcc.Graph(id='distplots', figure=fig),
          # plotting table
          dcc.Graph(id='table',
          figure={'data':[go.Table(
           header=dict(values=['P-value', 't-statistic'],
                 line = dict(color='#7D7F80'),
                  font = dict(color = 'white', size = 10),
                 fill = dict(color='#660066'),
                 align = ['center'] * 3),
           cells=dict(values=[format(p_value, '.8f'),
                              format(t_stat, '.6f')],
                 line = dict(color='#7D7F80'),
                 fill = dict(color='#EDFAFF'),
                 align = ['center'] * 3))],
                 'layout': {'width':400, 'height':500}},
                  config={'displayModeBar': False},
                style={"margin-left": 750,
                       "margin-right": 10,
                       'marginTop': -450,
                       'marginBottom':1300})]
                       )],
          style={'width':'60%', 'padding':10})

@app.callback(
    Output('distplots', 'figure'),
    [Input('mu_values', 'value'),
    Input('n_values', 'value')]
)
# distplots update
def update_graph(mu_values, n_values):
    group_a = np.random.randn(n_values)
    group_b = np.random.randn(n_values)+mu_values
    colors = ['#3A4750', '#660066']
    hist_data = [group_a, group_b]

    hist_data = [group_a, group_b]
    group_labels = ['Group A', 'Group B']
    fig = ff.create_distplot(hist_data, group_labels, bin_size=[0.2,0.2], colors=colors)
    return fig

@app.callback(
    Output('table', 'figure'),
    [Input('mu_values', 'value'),
    Input('n_values', 'value')]
)

# update table values
def update_table(mu_values, n_values):
    group_a = np.random.randn(n_values)
    group_b = np.random.randn(n_values)+mu_values
    t_stat, p_value = stats.ttest_ind(group_a, group_b)
    # addingg values to dictionary
    figure={'data':[go.Table(
     header=dict(values=['P-value', 't-statistic'],
           line = dict(color='#7D7F80'),
            font = dict(color = 'white', size = 10),
           fill = dict(color='#993399'),
           align = ['center'] * 3),
     cells=dict(values=[format(p_value, '.8f'),
                        format(t_stat, '.6f')],
           line = dict(color='#7D7F80'),
           fill = dict(color='#EDFAFF'),
           align = ['center'] * 3))],
           'layout': {'width':400, 'height':500}}
    return figure

if __name__ == '__main__':
    app.run_server(port=4000)
