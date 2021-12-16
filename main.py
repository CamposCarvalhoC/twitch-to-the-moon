from re import search
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from pandas.io.formats.format import TextAdjustment
import plotly.figure_factory as ff
from dash import Input, Output, dcc, html, State
import numpy as np
import plotly.graph_objects as go
from plotly.colors import n_colors
import plotly.express as px
from urllib.parse import unquote
import math

############################################################
##                                                        ##
##                   Utils                                ##
##                                                        ##
############################################################

class symbols_gen():
    def __init__(self) -> None:
        symbols = ["circle", "square", "diamond", "cross", "x", "triangle-up", "triangle-down", "pentagon", "hexagram", "star", "diamond", "hourglass", "bowtie", "asterisk", "hash", "y", "line"]
        self.n = 0
        self.max = len(symbols)
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.n >= self.max:
            self.n = 0
        sym = symbols[self.n]
        self.n += 1
        return sym


DATA = pd.read_csv("https://cdn.opensource.faculty.ai/old-faithful/data.csv")

df_global = pd.read_csv("data processing/data/global_viewers.csv",index_col=0,parse_dates=True)
df_viewers = pd.read_csv("data processing/data/all_games_viewers.csv",index_col=0,parse_dates=True)
df_domination = pd.read_csv("data processing/data/all_games_domination.csv",index_col=0,parse_dates=True)

df_ridge = pd.read_csv("data processing/data/top_games_viewers.csv",index_col=0,parse_dates=True)
df_ridge.set_index("date", inplace=True)
df_viewers.set_index("date", inplace=True)
df_domination.set_index("date", inplace=True)

# Dataframes radar
df_radar_avg_views = pd.read_csv("data processing/data/radar_mean_views.csv",squeeze=True,index_col=0)
df_radar_ratio_watch = pd.read_csv("data processing/data/radar_ratio_watch.csv",squeeze=True,index_col=0)
df_radar_ratio = pd.read_csv("data processing/data/radar_ratio.csv",squeeze=True,index_col=0)
df_radar_total_streamers = pd.read_csv("data processing/data/radar_total_streamers.csv",squeeze=True,index_col=0)
df_radar_total_views = pd.read_csv("data processing/data/radar_total_views.csv",squeeze=True,index_col=0)

# Dataframes radar
df_radar_avg_views_n = df_radar_avg_views.copy()
df_radar_ratio_watch_n = df_radar_ratio_watch.copy()
df_radar_ratio_n = df_radar_ratio.copy()
df_radar_total_streamers_n = df_radar_total_streamers.copy()
df_radar_total_views_n = df_radar_total_views.copy()


def normalize(df_rdr):
    max_val = df_rdr.max()
    df_rdr = np.log((df_rdr / max_val)*100) / np.log(1.000001)
    return df_rdr

df_radar_avg_views_n = normalize(df_radar_avg_views_n)
df_radar_ratio_watch_n = normalize(df_radar_ratio_watch_n)
df_radar_ratio_n = normalize(df_radar_ratio_n)
df_radar_total_streamers_n = normalize(df_radar_total_streamers_n)
df_radar_total_views_n = normalize(df_radar_total_views_n)

app = dash.Dash(external_stylesheets=[dbc.themes.PULSE,dbc.icons.BOOTSTRAP])


############################################################
##                                                        ##
##                   Accessibility                        ##
##                                                        ##
############################################################

def add_dropdown_accessibility(fig):
    button_layer_1_height = 1.15
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=["colorway", None],
                        label="Default",
                        method="relayout"
                    ),
                    dict(
                        args=["colorway", px.colors.sequential.Viridis],
                        label="Viridis",
                        method="relayout"
                    ),
                    dict(
                        args=["colorway", px.colors.qualitative.D3],
                        label="D3",
                        method="relayout"
                    ),
                    dict(
                        args=["colorway", px.colors.sequential.Rainbow],
                        label="Rainbow",
                        method="relayout"
                    ),
                ]),
                direction="down",
                showactive=True,
                x=0.15,
                xanchor="left",
                y=button_layer_1_height,
                yanchor="top"
            ),
            dict(
                buttons=list([
                    dict(
                        args=["mode", "lines+markers"],
                        label="Lines+markers",
                        method="restyle"
                    ),
                    dict(
                        args=["mode", "lines"],
                        label="Lines",
                        method="restyle"
                    ),
                    dict(
                        args=["mode", "markers"],
                        label="Markers",
                        method="restyle"
                    ),
                ]),
                direction="down",
                showactive=True,
                x=0.55,
                xanchor="left",
                y=button_layer_1_height,
                yanchor="top"
            ),
        ],
        annotations=[
            dict(text="Colorscale", x=0.02, xref="paper", y=button_layer_1_height, yref="paper",
                                align="left", showarrow=False),
            dict(text="Lines and markers", x=0.3, xref="paper", y=button_layer_1_height, yref="paper",
                                showarrow=False)
        ]
    )


############################################################
##                                                        ##
##                   Fig home page                        ##
##                                                        ##
############################################################

fig_home_page = go.Figure()
fig_home_page.add_trace(go.Scatter(x=df_global.index, y=df_global["Avg_viewers"], mode="lines+markers", fill="tozeroy"))

add_dropdown_accessibility(fig_home_page)

fig_home_page.update_layout(
    xaxis_title="Date",
    yaxis_title="Average viewers",
    font=dict(color="RebeccaPurple",size=18)

)

############################################################
##                                                        ##
##                   Ridge plot                           ##
##                                                        ##
############################################################

fig_ridge = go.Figure()

symbols = ["circle", "square", "diamond", "cross", "x", "triangle-up", "triangle-down", "pentagon", "hexagram", "star", "diamond", "hourglass", "bowtie", "asterisk", "hash", "y", "line"]

for df_col, sym in zip(df_ridge.columns, symbols):
    fig_ridge.add_trace(go.Scatter(y=df_ridge[df_col], x=df_ridge.index, marker_symbol=sym, marker_size=8,name=df_col, mode="lines+markers"))

add_dropdown_accessibility(fig_ridge)

fig_ridge.update_layout(
    xaxis_title="Date",
    yaxis_title="Average viewers",
    legend_title="Games",
    font=dict(color="RebeccaPurple",size=18)
)


############################################################
##                                                        ##
##                   Home page                            ##
##                                                        ##
############################################################

def create_value_card(title, value):
    return dbc.Card(
    [
        dbc.CardBody(
            [
                html.H5(title, className="card-title text-center"),
                html.H1(value, className="card-text text-center")
            ]            
        )
    
    ], color="primary", class_name="text-light rounded-pill", 
)

home = dbc.Container(
    [
        html.H2('Total average viewers per month since 2016',className='text-center text-primary mt-5'),
        dcc.Graph(figure=fig_home_page),
        dbc.Row(
            [
                
                dbc.Col(create_value_card("Total numbers of hours watched", "65'514'080'059")),
                dbc.Col(create_value_card("Total numbers of hours streamed", "2'158'669'079")),
            ]
        , class_name="mb-2"),
        dbc.Row(
            [
                
                dbc.Col(create_value_card("Total numbers of days watched", "2'729'753'335")),
                dbc.Col(create_value_card("Total numbers of days streamed", "89'944'544")),
            ]
        , class_name="mb-2"),
        dbc.Row(
            [
                
                dbc.Col(create_value_card("Total numbers of years watched", "7'478'776")),
                dbc.Col(create_value_card("Total numbers of years streamed", "246'423")),
            ]
        , class_name="mb-2"),
        html.H2('Top games average viewer since 2016',className='text-center text-primary mt-5'),
        dcc.Graph(figure=fig_ridge)
    ]
)


############################################################
##                                                        ##
##                   Game page                            ##
##                                                        ##
############################################################
games=[{'label':game,'value':game}for game in df_radar_avg_views.index]

game_stats = dbc.Row([
    html.H2("Table of game statistics",className="text-center text-primary")
],id='game-stats')

def game_page(game):
    game_compare = dcc.Dropdown(
        id='dropwdown-game-compare',
        options=games,
        value=game,
        multi=True
    )
    return dbc.Container([
        # html.H1(game,className="text-center text-primary mt-5"),
        html.H2('Games to Add',className='text-center text-primary mt-5'),
        game_compare,
        html.H2('Average viewers by game',className='text-center text-primary mt-5'),
        dcc.Graph(id='game-avg-viewers'),
        html.H2('Domination by game',className='text-center text-primary mt-5'),
        dcc.Graph(id='game-domination'),
        html.H2('Game statistics',className='text-center text-primary mt-5'),
        dcc.Graph(id='fig-radar'),
        game_stats
    ])

############################################################
##                                                        ##
##                      Source                            ##
##                                                        ##
############################################################

source = html.Div(
    dbc.Container(
        [
            html.H1("Source", className="display-3"),
            html.Hr(className="my-2"),
            html.P([
                "Source of the dataset we have used can be find ",
                html.A("here", href="https://www.kaggle.com/rankirsh/evolution-of-top-games-on-twitch"),
                " on kaggle."
            ]),           
            html.P(
                [
                    "The creator of the dataset used the website API of ",
                    html.A("Sullygnome", href="https://sullygnome.com/"),
                ]
            ),
            html.P(
                [
                    "Sullygnome use the ",  
                    html.A("Twitch API", href="https://dev.twitch.tv/"),
                    " to gather all their data",
                ]
            ),
            html.P(
                [
                    "We have used Plotly and Dash to make this webapp. You can find the plotly website ",  
                    html.A("here", href="https://plotly.com/"),
                ]
            ),

            html.P(
                [
                    "The logo was made by Antoine \"Edarsel\" Lestrade, you can find his instagram and follow him at ",  
                    html.A("@e.stradel", href="https://www.instagram.com/e.stradel/?utm_medium=copy_link"),
                ]
            ),

        ],
        fluid=True,
        className="py-3 text-center",
    ),
    className="p-3 bg-light rounded-3",
)

############################################################
##                                                        ##
##                   Game page                            ##
##                                                        ##
############################################################

def add_game_line(fig,game, symbols):
    fig.add_trace(go.Scatter(y=df_viewers[game], x=df_viewers.index,marker_size=8,name=game, mode="lines+markers", marker_symbol=next(symbols)))
    add_dropdown_accessibility(fig)

def add_game_domination_line(fig,game, symbols):
    fig.add_trace(go.Scatter(y=df_domination[game], x=df_domination.index,marker_size=8,name=game, mode="lines+markers", marker_symbol=next(symbols)))
    add_dropdown_accessibility(fig)

def add_row_game(game):
    return html.Tr([
                html.Th(f"{game}",scope="row",className='text-center align-middle'),
                html.Td(f"{df_radar_avg_views[game]/1000:.2f}k" if df_radar_avg_views[game] > 1000 else f"{df_radar_avg_views[game] :.2f}",className='text-center align-middle'),
                html.Td(f"{df_radar_ratio_watch[game]:.2f}",className='text-center align-middle'),
                html.Td(f"{df_radar_ratio[game]:.2f}",className='text-center align-middle'),
                html.Td(f"{df_radar_total_streamers[game]/1000:.2f}k" if df_radar_total_streamers[game] > 1000 else f"{df_radar_total_streamers[game]:.2f}",className='text-center align-middle'),
                html.Td(f"{df_radar_total_views[game]/1000:.2f}k" if df_radar_total_views[game] > 1000 else f"{df_radar_total_views[game]:.2f}",className='text-center align-middle'),
            ])

categories = ['Avg. views','Ratio views/streamed', 'Ratio viewer/channel', 'Streamers','Views']

def add_radar_trace(fig_radar,game):
    fig_radar.add_trace(go.Scatterpolar(
        r=[df_radar_avg_views_n[game],df_radar_ratio_watch_n[game],df_radar_ratio_n[game],df_radar_total_streamers_n[game],df_radar_total_views_n[game]],
        theta=categories,
        fill='toself',
        name=game,
        hoverinfo='skip'
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True,
            )),
        showlegend=False,
        dragmode=False,
        modebar_remove=["zoom", "pan", "select", "lasso"]
    )


############################################################
##                                                        ##
##                   Navbar&Layout                        ##
##                                                        ##
############################################################

game_dropwdown = dcc.Dropdown(
    id='dropwdown-game',
    options=games,
    value='Fortnite',
)

search_bar = dbc.Row(
    [
        dbc.Col([game_dropwdown],width=9),
        dbc.Col(
            dcc.Link(
            dbc.Button(
                "Search", id="btn-search",color="info", className="ms-2"
            ),href=f'/game/{game_dropwdown.value}',refresh=True,id='link-search'),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0 w-50",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="https://cdn.discordapp.com/attachments/893500177493684244/921040901965500416/twitch_moon_logo.png", height="50px")),
                        dbc.Col(dbc.NavbarBrand("to the Moon", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("Source", href="/source", active="exact")
                ],
                pills=True,
            ),

            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="primary",
    dark=True,
)


content = html.Div(id="page-content")

app.layout = html.Div([dcc.Location(id="url"), navbar, content])

############################################################
##                                                        ##
##                      Callback                          ##
##                                                        ##
############################################################


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    link = pathname.split("/")
    if pathname == "/":
        return home
    elif link[1]=="game":
        return game_page(unquote(link[2]))
    elif pathname == "/source":
        return source
    # If the user tries to reach a different page, return a 404 message
    return dbc.Container(
        [
            html.H1("404: Not found", className="text-danger display-3"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ], 
        fluid=True,
        className="py-3 text-center p-3 bg-light rounded-3"
    )

@app.callback(
    Output('link-search', 'href'),
    Input('dropwdown-game', 'value')
)
def update_href_search(value):
    return f"/game/{value}"

@app.callback(
    Output('fig-radar', 'figure'),
    Input('dropwdown-game-compare', 'value')
)
def update_fig_radar(value):
    fig_radar = go.Figure()
    if isinstance(value,list):
        for game in value:
            add_radar_trace(fig_radar,game)
    elif isinstance(value, str):
        add_radar_trace(fig_radar,value)
    
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=False,
            )),
        showlegend=True,
        legend_title="Games",
        font=dict(color="RebeccaPurple",size=18)
    )

    return fig_radar

@app.callback(
    Output('game-domination', 'figure'),
    Input('dropwdown-game-compare', 'value')
)
def update_game_avg_viewers(value):
    fig_domination = go.Figure()
    symbols = symbols_gen()
    if isinstance(value,list):
        for game in value:
            add_game_domination_line(fig_domination,game, symbols)
    elif isinstance(value, str):
        add_game_domination_line(fig_domination,value, symbols)
    
    fig_domination.update_layout(
        #plot_bgcolor ='thistle',
        xaxis_title="Date",
        yaxis_title="Domination",
        legend_title="Games",
        font=dict(color="RebeccaPurple",size=18)
    )
    return fig_domination

@app.callback(
    Output('game-avg-viewers', 'figure'),
    Input('dropwdown-game-compare', 'value')
)
def update_game_avg_viewers(value):
    fig_game_avg = go.Figure()
    symbols = symbols_gen()
    if isinstance(value,list):
        for game in value:
            add_game_line(fig_game_avg,game, symbols)
    elif isinstance(value, str):
        add_game_line(fig_game_avg,value, symbols)
    
    fig_game_avg.update_layout(
        #plot_bgcolor ='thistle',
        xaxis_title="Date",
        yaxis_title="Average viewers",
        legend_title="Games",
        font=dict(color="RebeccaPurple",size=18)
    )
    return fig_game_avg

@app.callback(
    Output('game-stats', 'children'),
    [Input('dropwdown-game-compare', 'value')],
    [State('game-stats', 'children')],
)
def update_dropdown_compare(value,children):
    thead = [html.Thead([
                html.Tr([
                    html.Th("Game",scope='col',className='text-center align-middle'),
                    html.Th("Avg. views",scope='col',className='text-center align-middle'),
                    html.Th("Ratio views/streamed",scope='col',className='text-center align-middle'),
                    html.Th("Ratio viewer/channel",scope='col',className='text-center align-middle'),
                    html.Th("Streamers",scope='col',className='text-center align-middle'),
                    html.Th("Views",scope='col',className='text-center align-middle')
            ])
            ],className='thead-light')]
    tbody = []
    children = [
        dbc.Row([
            dbc.Col([html.H2("Table of game statistics",className="text-center text-primary")])
        ]),
        dbc.Row([
            dbc.Table(thead + [html.Tbody(tbody)],bordered=True,dark=False,hover=True,responsive=True,striped=True,color='secondary')
        ])
    ]
    if isinstance(value,list):
        for game in value:
            row = add_row_game(game)
            tbody.append(row)
    elif isinstance(value, str):
        row = add_row_game(value)
        tbody.append(row)

    return children

############################################################
##                                                        ##
##                        Main                            ##
##                                                        ##
############################################################

if __name__ == "__main__":
    app.run_server(port=8888, use_reloader=True)