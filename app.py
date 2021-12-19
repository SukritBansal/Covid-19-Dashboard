# Importing Libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output
from plotly.graph_objects import Layout
from plotly.validator_cache import ValidatorCache


app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE,'https://fonts.googleapis.com/css2?family=Fuzzy+Bubbles&display=swap'])
app.css.config.serve_locally = True

# -----------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)

confirmed = pd.read_csv("Confirmed.csv")
deaths = pd.read_csv("Deaths.csv")
recovered = pd.read_csv("Recovered.csv")

# Unpivoting the DataFrame
confirmed = confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date',
                           value_name='Confirmed')
deaths = deaths.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date',
                     value_name='Deaths')
recovered = recovered.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date',
                           value_name='Recovered')

# Making 1 DataFrame
covid = pd.merge(confirmed, deaths)
covid = pd.merge(covid, recovered)

covid['Date'] = pd.to_datetime(covid['Date'], errors='coerce')

# Calculating Active Cases
covid['Active'] = covid['Confirmed'] - covid['Deaths'] - covid['Recovered']

covid_data1 = covid.groupby(['Date'])[['Confirmed', 'Deaths', 'Recovered', 'Active']].sum().reset_index()
covid_data2 = covid.groupby(['Date', 'Country/Region'])[['Confirmed', 'Deaths', 'Recovered', 'Active']].sum().\
    reset_index()
# ------------------------------------------------------------------------------
# App layout
app.layout = dbc.Container([


    dbc.Row([
#       Logo
        dbc.Col([
            html.Div([
                html.Img(src=app.get_asset_url('covid-logo.png'), id="Corona Image",
                         style={"height": "100px",
                                "width": "auto"
                                }
                         ),
            ], className="mt-2 ml-1"),

            html.Div([
                html.H3("CoTrack",
                        style={"color": "White", "font-weight": "bold"}
                        )
            ])
        ], width='auto'),

#       Selecting Countries
        dbc.Col([
            html.Div([
                html.Div(["Select Country"], style={'color': 'White'}),
                dcc.Dropdown(
                    value="India",
                    options=[{'label': c, 'value': c} for c in (covid['Country/Region'].unique())],
                    id="countries",
                    multi=False,
                    placeholder="Select Country",
                    clearable=True, className="mt-1")
            ], className="mt-4"),
            html.P('New Cases : '+' '+' '+str(covid_data2['Date'].iloc[-1].strftime('%B %d %Y')) +
                   ' ', style={'color': 'white', 'text-align': 'center'})
        ], width=2, style={"margin-left": 30}),

#       Daily Delta Analysis Countrywise

        dbc.Col([
            dcc.Graph(id='confirmed', config={'displayModeBar': False},
                      style={'margin-top':'37px'}, className='border rounded-3'
                      )
        ],width=2),

        dbc.Col([
            dcc.Graph(id='death', config={'displayModeBar': False},
                      style={'margin-top':'37px'}, className='border rounded-3'
                      )
        ],width=2),

        dbc.Col([
                dcc.Graph(id='recovered', config={'displayModeBar': False},
                        style={'margin-top':'37px'}, className='border rounded-3'
                )
        ],width=2),

        dbc.Col([
                dcc.Graph(id='active', config={'displayModeBar': False},
                        style={'margin-top':'37px'}, className='border rounded-3'
                )
        ],width=2)
    ]),

    #   4 stats of global cases,recoveries,deaths,active
    dbc.Row([
        #   Global Cases
        dbc.Col([
            html.Div(id="container1", children=[
                    html.H2('Global Confirmed', style={'text-align': 'center', 'color': 'white',
                                                       'margin-top': 8, 'fontsize': 30,}),
                    html.P(f"{covid_data1['Confirmed'].iloc[-1]:,.0f}", style={'text-align':'center', 'color':'#FFEF78', 'font-size':25}),
                    html.P("New Confirmed: "+f"{covid_data1['Confirmed'].iloc[-1]-covid_data1['Confirmed'].iloc[-2]:,.0f}"+" "+"%Change" '('
                            +str(round(((covid_data1['Confirmed'].iloc[-1]-covid_data1['Confirmed'].iloc[-2])/covid_data1['Confirmed'].iloc[-1])*100,2))+'%)'
                            ,style={'text-align':'center','color':'white'})

                    ],style={'backgroundColor': '#D08504', 'height': 'auto', 'width': 'auto', 'margin-left': 15,
                             'margin-top': 20},className='border rounded-3')
        ],width=3),

        #Global Deaths
        dbc.Col([
            html.Div(id="container2",children=[
                    html.H2('Global Deaths',style={'text-align':'center', 'color':'white','margin-top':8,
                                                   'fontsize':30}),
                    html.P(f"{covid_data1['Deaths'].iloc[-1]:,.0f}",style={'text-align':'center',
                                                                           'color':'#FFEF78','font-size':25}),
                    html.P("New Deaths: "+f"{covid_data1['Deaths'].iloc[-1]-covid_data1['Deaths'].iloc[-2]:,.0f}"
                           + " " + "%Change" '('
                            +str(round(((covid_data1['Deaths'].iloc[-1]-covid_data1['Deaths'].iloc[-2])/covid_data1['Deaths'].iloc[-1])*100,2))+'%)'
                            ,style={'text-align':'center','color':'white'})

                    ],style={'backgroundColor':'#660000','height': 'auto','width':'auto','margin-left':15,'margin-top':20},className='border rounded-3')
        ],width=3),

        #Global Recoveries
        dbc.Col([
            html.Div(id="container3",children=[
                    html.H2('Global Recovered',style={'text-align':'center','color':'white','margin-top':8,'fontsize':30}),
                    html.P(f"{covid_data1['Recovered'].iloc[-1]:,.0f}",style={'text-align':'center','color':'#FFEF78','font-size':25}),
                    html.P("New Recoveries: "+f"{covid_data1['Recovered'].iloc[-1]-covid_data1['Recovered'].iloc[-2]:,.0f}" +"    " +"%Change" '('
                            +str(round(((covid_data1['Recovered'].iloc[-1]-covid_data1['Recovered'].iloc[-2])/covid_data1['Recovered'].iloc[-1])*100,2))+'%)'
                                ,style={'text-align':'center','color':'white'})

                    ],style={'backgroundColor':'#183C28','height': 'auto','width':'auto','margin-left':15,'margin-top':20},className='border rounded-3')
        ],width=3),

        #Global Active
        dbc.Col([
            html.Div(id="container5",children=[
                    html.H2('Global Active',style={'text-align':'center','color':'white','margin-top':8,'fontsize':30}),
                    html.P(f"{covid_data1['Active'].iloc[-1]:,.0f}",style={'text-align':'center','color':'#FFEF78','font-size':25}),
                    html.P("New Active: "+f"{covid_data1['Active'].iloc[-1]-covid_data1['Active'].iloc[-2]:,.0f}" +"     " +"%Change" '('
                            +str(round(((covid_data1['Active'].iloc[-1]-covid_data1['Active'].iloc[-2])/covid_data1['Active'].iloc[-1])*100,2))+'%)'
                                ,style={'text-align':'center','color':'white'})

                    ],style={'backgroundColor':'#29407C','height': 'auto','width':'auto','margin-left':15,'margin-top':20,'margin-right':15},className='border rounded-3')
        ],width=3),
    ]),

    dbc.Row([

#       Pie Chart
        dbc.Col([
            html.Div([
                dcc.Graph(id='pie_chart',
                          config={'displayModeBar': 'hover'})
            ])
        ],className='mt-3',width='auto',style={'margin-left':35}),

#       Confirmed Cases Graph
        dbc.Col([
            html.Div([
                dcc.Graph(id='line_chart_1')
            ])
        ],className='mt-3',width=4),

#       Deaths Graph
        dbc.Col([
            html.Div([
                dcc.Graph(id='line_chart_2')
            ])
        ],className='mt-3',width=4)
    ]),

    dbc.Row([

#       Daily Recoveries graph
        dbc.Col([
            html.Div([
                dcc.Graph(id='line_chart_3')
            ])
        ],className='mt-3',width=6),

#       Active cases Graph
        dbc.Col([
            html.Div([
                dcc.Graph(id='line_chart_4')
            ])
        ],className='mt-3',width=6)
    ]),

    dbc.Row([

#       Spread Analysis
        dbc.Col([
            html.Div([
                dcc.Graph(id='map')
            ])
        ],width=12, className='mt-3')
    ]),
],fluid=True)


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='confirmed', component_property='figure'),
    Input(component_id='countries', component_property='value')
)
def update_confirmed(countries):
    covid_data_2 = covid_data2.copy()
    value_confirm = covid_data_2[covid_data_2['Country/Region'] == countries]['Confirmed'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == countries]['Confirmed'].iloc[-2]
    delta_confirm = covid_data_2[covid_data_2['Country/Region'] == countries]['Confirmed'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == countries]['Confirmed'].iloc[-3]

    return {
            'data': [ go.Indicator(
                    mode='number+delta',
                    value=value_confirm,
                    delta={'reference': delta_confirm,
                           'position': 'right',
                           'valueformat': ',g',
                           'relative': False,
                           'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20}},
                    domain={'y':[0,1], 'x':[0,1]})],
            'layout': go.Layout(
                    title={'text': 'New Confirmed:',
                           'y': 0.9,
                           'x': 0.5,
                           'xanchor': 'center',
                           'yanchor': 'top'},
                    font=dict(color='#D08504',
                              family='Fuzzy Bubbles'),
                    paper_bgcolor='#F7F7F7',
                    plot_bgcolor='#F7F7F7',
                    height=50)
    }

@app.callback(
    Output(component_id='death', component_property='figure'),
    Input(component_id='countries', component_property='value')
)
def update_deaths(countries):
    covid_data_2 = covid_data2.copy()
    value_confirm = covid_data_2[covid_data_2['Country/Region'] == countries]['Deaths'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == countries]['Deaths'].iloc[-2]
    delta_confirm = covid_data_2[covid_data_2['Country/Region'] == countries]['Deaths'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == countries]['Deaths'].iloc[-3]
    return {
            'data': [ go.Indicator(
                    mode='number+delta',
                    value=value_confirm,
                    delta={'reference': delta_confirm,
                           'position': 'right',
                           'valueformat': ',g',
                           'relative': False,
                           'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20}},
                    domain={'y':[0,1], 'x':[0,1]})],
            'layout': go.Layout(
                    title={'text': 'New Deaths:',
                           'y': 0.9,
                           'x': 0.5,
                           'xanchor': 'center',
                           'yanchor': 'top'},
                    font=dict(color='#660000',
                              family='Fuzzy Bubbles'),
                    paper_bgcolor='#F7F7F7',
                    plot_bgcolor='#F7F7F7',
                    height=50)
    }
@app.callback(
    Output(component_id='recovered', component_property='figure'),
    Input(component_id='countries', component_property='value')
)
def update_recovered(countries):
    covid_data_2 = covid_data2.copy()
    value_confirm = covid_data_2[covid_data_2['Country/Region'] == countries]['Recovered'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == countries]['Recovered'].iloc[-2]
    delta_confirm = covid_data_2[covid_data_2['Country/Region'] == countries]['Recovered'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == countries]['Recovered'].iloc[-3]
    return {
            'data': [ go.Indicator(
                    mode='number+delta',
                    value=value_confirm,
                    delta={'reference': delta_confirm,
                           'position': 'right',
                           'valueformat': ',g',
                           'relative': False,
                           'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20}},
                    domain={'y':[0,1], 'x':[0,1]})],
            'layout': go.Layout(
                    title={'text': 'New Recoveries:',
                           'y': 0.9,
                           'x': 0.5,
                           'xanchor': 'center',
                           'yanchor': 'top'},
                    font=dict(color='#183C28',
                              family='Fuzzy Bubbles'),
                    paper_bgcolor='#F7F7F7',
                    plot_bgcolor='#F7F7F7',
                    height=50)
    }
@app.callback(
    Output(component_id='active', component_property='figure'),
    Input(component_id='countries', component_property='value')
)
def update_active(countries):
    covid_data_2 = covid_data2.copy()
    value_confirm = covid_data_2[covid_data_2['Country/Region'] == countries]['Active'].iloc[-1] - covid_data_2[covid_data_2['Country/Region'] == countries]['Active'].iloc[-2]
    delta_confirm = covid_data_2[covid_data_2['Country/Region'] == countries]['Active'].iloc[-2] - covid_data_2[covid_data_2['Country/Region'] == countries]['Active'].iloc[-3]
    return {
            'data': [ go.Indicator(
                    mode='number+delta',
                    value=value_confirm,
                    delta={'reference': delta_confirm,
                           'position': 'right',
                           'valueformat': ',g',
                           'relative': False,
                           'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20}},
                    domain={'y':[0,1], 'x':[0,1]})],
            'layout': go.Layout(
                    title={'text': 'New Active:',
                           'y': 0.9,
                           'x': 0.5,
                           'xanchor': 'center',
                           'yanchor': 'top',
                           },
                    font=dict(color='#29407C',
                              family='Fuzzy Bubbles'),
                    paper_bgcolor='#F7F7F7',
                    plot_bgcolor='#F7F7F7',
                    height=50)
    }
@app.callback(
    Output(component_id='pie_chart', component_property='figure'),
    Input(component_id='countries', component_property='value')
)
def update_graph(countries):
    covid_data_2 = covid_data2.copy()
    new_confirmed = covid_data_2[covid_data_2['Country/Region'] == countries]['Confirmed'].iloc[-1]
    new_death = covid_data_2[covid_data_2['Country/Region'] == countries]['Deaths'].iloc[-1]
    new_recovered = covid_data_2[covid_data_2['Country/Region'] == countries]['Recovered'].iloc[-1]
    new_active = covid_data_2[covid_data_2['Country/Region'] == countries]['Active'].iloc[-1]
    colors = ['orange','red','green','blue']

    return{
        'data': [go.Pie(
                        labels=['Confirmed', 'Death', 'Recovered', 'Active'],
                        values=[new_confirmed,new_death,new_recovered,new_active],
                        marker=dict(colors=colors),
                        hoverinfo='label+value+percent',
                        textinfo='label+value',
                        textfont=dict(size=13),
                        hole=0.8,
                        rotation=45)],
        'layout': go.Layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            hovermode='closest',
            title={'text':'Total Cases : ' + (countries),
                   'y':0.93,
                   'x':0.5,
                   'xanchor':'center',
                   'yanchor':'top'},
            titlefont={'color':'white',
                       'size':20},
            legend={'orientation': 'h',
                    'bgcolor': 'black',
                    'xanchor': 'center',
                    'x':0.5,
                    'y':-0.07},
            font=dict(
                family='Fuzzy Bubbles',
                size=12,
                color='white'
            ),
            width=400
        )
    }

@app.callback(
    Output(component_id='line_chart_1', component_property='figure'),
    Input(component_id='countries', component_property='value')
)
def update_graph(countries):
    covid_data_2 = covid_data2.copy()
    covid_data_3 = covid_data_2[covid_data_2['Country/Region'] == countries][['Country/Region','Date','Confirmed']].reset_index()
    covid_data_3['Daily_Confirmed'] = covid_data_3['Confirmed'] - covid_data_3['Confirmed'].shift(1)

    return {
        'data':[go.Scatter(x=covid_data_3[covid_data_3['Country/Region'] == countries]['Date'],
                           y=covid_data_3[covid_data_3['Country/Region'] == countries]['Daily_Confirmed'],
                           mode='lines',
                           name='Daily Confirmed',
                           marker=dict(color='orange'),
                           hoverinfo='text',
                           hovertext=
                           '<b>Date</b>: ' + covid_data_3[covid_data_3['Country/Region'] == countries]['Date'].astype(str) + '<br>' +
                           '<b>Daily Confirmed</b>: ' + [f'{x:,.0f}' for x in covid_data_3[covid_data_3['Country/Region'] == countries]['Daily_Confirmed']] + '<br>')],
        'layout': go.Layout(plot_bgcolor='black',
                            paper_bgcolor='black',
                            title={
                                'text': 'Daily Confirmed Cases : ' + (countries),
                                'y': 0.93,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'},
                            titlefont={
                                'size':20,
                                'color':'white'
                            },
                            hovermode='x',
                            xaxis=dict(title='<b>Date</b>',
                                       color='white',
                                       showline=True,
                                       showgrid=True,
                                       showticklabels=True,
                                       linecolor='white',
                                       linewidth=2,
                                       ticks='outside',
                                       tickfont=dict(
                                           family='Fuzzy Bubbles',
                                           size=12,
                                           color='white'
                                       )
                            ),
                            yaxis=dict(title='<b>Daily Cases</b>',
                                       color='white',
                                       showline=True,
                                       showgrid=True,
                                       showticklabels=True,
                                       linecolor='white',
                                       linewidth=2,
                                       ticks='outside',
                                       tickfont=dict(
                                           family='Fuzzy Bubbles',
                                           size=12,
                                           color='white'
                                       )
                            ),
                            font=dict(
                                family='Fuzzy Bubbles',
                            )
                            )
    }
@app.callback(
    Output(component_id='line_chart_2', component_property='figure'),
    Input(component_id='countries', component_property='value')
)
def update_graph(countries):
    covid_data_2 = covid_data2.copy()
    covid_data_3 = covid_data_2[covid_data_2['Country/Region'] == countries][['Country/Region', 'Date', 'Deaths']].reset_index()
    covid_data_3['Daily_Deaths'] = covid_data_3['Deaths'] - covid_data_3['Deaths'].shift(1)
    return {
        'data': [go.Scatter(x=covid_data_3[covid_data_3['Country/Region'] == countries]['Date'],
                            y=covid_data_3[covid_data_3['Country/Region'] == countries]['Daily_Deaths'],
                            mode='lines',
                            name='Daily Deaths',
                            marker=dict(color='red'),
                            hoverinfo='text',
                            hovertext=
                            '<b>Date</b>: ' + covid_data_3[covid_data_3['Country/Region'] == countries]['Date'].astype(
                                str) + '<br>' +
                            '<b>Daily Deaths</b>: ' + [f'{x:,.0f}' for x in
                                                          covid_data_3[covid_data_3['Country/Region'] == countries][
                                                              'Daily_Deaths']] + '<br>')],
        'layout': go.Layout(plot_bgcolor='black',
                            paper_bgcolor='black',
                            title={
                                'text': 'Daily Deaths : ' + (countries),
                                'y': 0.93,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'},
                            titlefont={
                                'size': 20,
                                'color': 'white'
                            },
                            hovermode='x',
                            xaxis=dict(title='<b>Date</b>',
                                       color='white',
                                       showline=True,
                                       showgrid=True,
                                       showticklabels=True,
                                       linecolor='white',
                                       linewidth=2,
                                       ticks='outside',
                                       tickfont=dict(
                                           family='Fuzzy Bubbles',
                                           size=12,
                                           color='white'
                                       )
                                       ),
                            yaxis=dict(title='<b>Daily Deaths</b>',
                                       color='white',
                                       showline=True,
                                       showgrid=True,
                                       showticklabels=True,
                                       linecolor='white',
                                       linewidth=2,
                                       ticks='outside',
                                       tickfont=dict(
                                           family='Fuzzy Bubbles',
                                           size=12,
                                           color='white'
                                       )
                                       ),
                            font=dict(
                                family='Fuzzy Bubbles',
                            )
                            )
    }

@app.callback(
    Output(component_id='line_chart_3', component_property='figure'),
    Input(component_id='countries', component_property='value')
)
def update_graph(countries):
    covid_data_2 = covid_data2.copy()
    covid_data_3 = covid_data_2[covid_data_2['Country/Region'] == countries][['Country/Region', 'Date', 'Recovered']].reset_index()
    covid_data_3['Daily_Recoveries'] = covid_data_3['Recovered'] - covid_data_3['Recovered'].shift(1)
    return {
        'data': [go.Scatter(x=covid_data_3[covid_data_3['Country/Region'] == countries]['Date'],
                            y=covid_data_3[covid_data_3['Country/Region'] == countries]['Daily_Recoveries'],
                            mode='lines',
                            name='Daily Recoveries',
                            marker=dict(color='green'),
                            hoverinfo='text',
                            hovertext=
                            '<b>Date</b>: ' + covid_data_3[covid_data_3['Country/Region'] == countries]['Date'].astype(
                                str) + '<br>' +
                            '<b>Daily Recoveries</b>: ' + [f'{x:,.0f}' for x in
                                                          covid_data_3[covid_data_3['Country/Region'] == countries][
                                                              'Daily_Recoveries']] + '<br>')],
        'layout': go.Layout(plot_bgcolor='black',
                            paper_bgcolor='black',
                            title={
                                'text': 'Daily Recoveries : ' + (countries),
                                'y': 0.93,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'},
                            titlefont={
                                'size': 20,
                                'color': 'white'
                            },
                            hovermode='x',
                            xaxis=dict(title='<b>Date</b>',
                                       color='white',
                                       showline=True,
                                       showgrid=True,
                                       showticklabels=True,
                                       linecolor='white',
                                       linewidth=2,
                                       ticks='outside',
                                       tickfont=dict(
                                           family='Fuzzy Bubbles',
                                           size=12,
                                           color='white'
                                       )
                                       ),
                            yaxis=dict(title='<b>Daily Recoveries</b>',
                                       color='white',
                                       showline=True,
                                       showgrid=True,
                                       showticklabels=True,
                                       linecolor='white',
                                       linewidth=2,
                                       ticks='outside',
                                       tickfont=dict(
                                           family='Fuzzy Bubbles',
                                           size=12,
                                           color='white'
                                       )
                                       ),
                            font=dict(
                                family='Fuzzy Bubbles',
                            )
                            )
    }

@app.callback(
    Output(component_id='line_chart_4', component_property='figure'),
    Input(component_id='countries', component_property='value')
)
def update_graph(countries):
    covid_data_2 = covid_data2.copy()
    covid_data_3 = covid_data_2[covid_data_2['Country/Region'] == countries][['Country/Region', 'Date', 'Active']].reset_index()
    return {
        'data': [go.Scatter(x=covid_data_3[covid_data_3['Country/Region'] == countries]['Date'],
                            y=covid_data_3[covid_data_3['Country/Region'] == countries]['Active'],
                            mode='lines',
                            name='Daily Active',
                            marker=dict(color='blue'),
                            hoverinfo='text',
                            hovertext=
                            '<b>Date</b>: ' + covid_data_3[covid_data_3['Country/Region'] == countries]['Date'].astype(
                                str) + '<br>' +
                            '<b>Active Cases</b>: ' + [f'{x:,.0f}' for x in
                                                          covid_data_3[covid_data_3['Country/Region'] == countries][
                                                              'Active']] + '<br>')],
        'layout': go.Layout(plot_bgcolor='black',
                            paper_bgcolor='black',
                            title={
                                'text': 'Active Cases : ' + (countries),
                                'y': 0.93,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'},
                            titlefont={
                                'size': 20,
                                'color': 'white'
                            },
                            hovermode='x',
                            xaxis=dict(title='<b>Date</b>',
                                       color='white',
                                       showline=True,
                                       showgrid=True,
                                       showticklabels=True,
                                       linecolor='white',
                                       linewidth=2,
                                       ticks='outside',
                                       tickfont=dict(
                                           family='Fuzzy Bubbles',
                                           size=12,
                                           color='white'
                                       )
                                       ),
                            yaxis=dict(title='<b>Active Cases</b>',
                                       color='white',
                                       showline=True,
                                       showgrid=True,
                                       showticklabels=True,
                                       linecolor='white',
                                       linewidth=2,
                                       ticks='outside',
                                       tickfont=dict(
                                           family='Fuzzy Bubbles',
                                           size=12,
                                           color='white'
                                       )
                                       ),
                            font=dict(
                                family='Fuzzy Bubbles',
                            )
                            )
    }

@app.callback(
    Output(component_id='map', component_property='figure'),
    Input(component_id='countries', component_property='value')
)
def update_graph(countries):

    covid_data_2 = covid.groupby(['Lat', 'Long', 'Country/Region'])[['Confirmed', 'Deaths', 'Recovered', 'Active']].max().reset_index()
    return{
        'data':[
            go.Scattermapbox(
                lat=covid_data_2['Lat'],
                lon=covid_data_2['Long'],
                mode='markers',
                marker=go.scattermapbox.Marker(size=covid_data_2['Confirmed']/1500,
                                               color=covid_data_2['Confirmed'],
                                               colorscale='hsv',
                                               showscale=False,
                                               sizemode='area',
                                                opacity=0.3),
                hoverinfo='text',
                hovertext=
                '<b>Country</b>: ' + covid_data_2['Country/Region'].astype(str) + '<br>' +
                '<b>Confirmed</b>: ' + [f'{x:,.0f}' for x in covid_data_2['Confirmed']] + '<br>' +
                '<b>Death</b>: ' + [f'{x:,.0f}' for x in covid_data_2['Deaths']] + '<br>' +
                '<b>Recovered</b>: ' + [f'{x:,.0f}' for x in covid_data_2['Recovered']] + '<br>' +
                '<b>Active</b>: ' + [f'{x:,.0f}' for x in covid_data_2['Active']] + '<br>'
            )
        ],

        'layout': go.Layout(
            title={
                'text': 'Corona Affected Countries : ',
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            margin={'r':0,'t':0,'l':0,'b':0},
            hovermode='closest',
            mapbox=dict(accesstoken='pk.eyJ1Ijoic3Vrcml0YmFuc2FsIiwiYSI6ImNrd3A2amswbTA5dm0ydmwwOTF2ZjlhaXQifQ.J2BH8WNsbLoJ4fsvCcTNzw',
                        center=go.layout.mapbox.Center(lat=36, lon=-5.4),
                        style='dark',
                        zoom=1.2),
            font={
                'color':'white'
            },
            autosize=True,
        )
    }


# ------------------------------------------------------------------------------
if __name__ == '__main__' :
    app.run_server(debug=True)