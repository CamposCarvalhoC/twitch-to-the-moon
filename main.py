from re import search
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.figure_factory as ff
from dash import Input, Output, dcc, html, State
import numpy as np
import plotly.graph_objects as go
from plotly.colors import n_colors
import plotly.express as px
from urllib.parse import unquote


DATA = pd.read_csv("https://cdn.opensource.faculty.ai/old-faithful/data.csv")

df_global = pd.read_csv("data processing/data/global_viewers.csv",index_col=0,parse_dates=True)
df_ridge = pd.read_csv("data processing/data/top_games_viewers.csv",index_col=0,parse_dates=True)
df_ridge.set_index("date", inplace=True)

# Dataframes radar
df_radar_avg_views = pd.read_csv("data processing/data/radar_avg_views.csv",squeeze=True,index_col=0)
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


app = dash.Dash(external_stylesheets=[dbc.themes.PULSE,dbc.icons.BOOTSTRAP])

############################################################
##                                                        ##
##                   Fig home page                        ##
##                                                        ##
############################################################

fig_home_page = go.Figure()
fig_home_page.add_trace(go.Scatter(x=df_global.index, y=df_global["Avg_viewers"], mode="lines+markers"))

fig_home_page.update_layout(
    title_text="Average viewers per month since 2016",
    xaxis_title="Date",
    yaxis_title="Average viewers",

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

button_layer_1_height = 1.15
fig_ridge.update_layout(
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
            x=0.1,
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
            x=0.45,
            xanchor="left",
            y=button_layer_1_height,
            yanchor="top"
        ),
    ]
)

fig_ridge.update_layout(
    annotations=[
        dict(text="Colorscale", x=0.02, xref="paper", y=1.12, yref="paper",
                             align="left", showarrow=False),
        dict(text="Lines and markers", x=0.3, xref="paper", y=1.12, yref="paper",
                             showarrow=False)
    ])



fig_global = px.line(df_global)

categories = ['Avg. views','Ratio watch', 'Ratio', 'Streamers','Views']
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
    
    ], color="primary", class_name="text-light ", 
)

home = dbc.Container(
    [
        dcc.Graph(figure=fig_home_page),
        html.Br(),
        dbc.Row(
            [
                
                dbc.Col(create_value_card("Total numbers of hours watched", "65'514'080'059")),
                dbc.Col(create_value_card("Total numbers of hours streamed", "2'158'669'079")),
            ]
        ),
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
    html.H2("Game Stats",className="text-center text-primary")
],id='game-stats')

def game_page(game):
    game_compare = dcc.Dropdown(
        id='dropwdown-game-compare',
        options=games,
        value=game,
        multi=True
    )
    return dbc.Container([
        html.H1(game,className="text-center text-primary mt-5"),
        dcc.Graph(figure=fig_global),# figure=fig_game_global
        dcc.Graph(figure=fig_global),# figure=fig_game_domination
        dbc.Row([
            dbc.Col([
                html.H2('Games to Add',className='text-center text-primary'),
                dbc.Row([
                    dbc.Col([game_compare]),
                ]),
                dcc.Graph(id='fig-radar')
            ]),
            dbc.Col([
                game_stats
            ])
        ])
    ])


############################################################
##                                                        ##
##                   Navbar&Layout                        ##
##                                                        ##
############################################################

game_dropwdown = dcc.Dropdown(
    id='dropwdown-game',
    options=games,
    value='Fortnite'
)

search_bar = dbc.Row(
    [
        game_dropwdown,
        dbc.Col(
            dcc.Link(
            dbc.Button(
                "Search", id="btn-search",color="info", className="ms-2"
            ),href=f'/game/{game_dropwdown.value}',refresh=True,id='link-search'),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        #dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Twitch to the Moon", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact")
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
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
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
            visible=True,
            )),
        showlegend=True
    )

    return fig_radar


def add_row_game(game):
    return html.Tr([
                html.Th(f"{game}",scope="row",className='text-center align-middle'),
                html.Td(f"{df_radar_avg_views[game]/1000:.2f}k",className='text-center align-middle'),
                html.Td(f"{df_radar_ratio_watch[game]:.2f}",className='text-center align-middle'),
                html.Td(f"{df_radar_ratio[game]:.2f}",className='text-center align-middle'),
                html.Td(f"{df_radar_total_streamers[game]/1000:.2f}k",className='text-center align-middle'),
                html.Td(f"{df_radar_total_views[game]/1000:.2f}k",className='text-center align-middle'),
            ])

def add_radar_trace(fig_radar,game):
    fig_radar.add_trace(go.Scatterpolar(
        r=[df_radar_avg_views[game]/1000,df_radar_ratio_watch[game],df_radar_ratio[game],df_radar_total_streamers[game]/1000,df_radar_total_views[game]/1000],
        theta=categories,
        fill='toself',
        name=game
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True,
            )),
        showlegend=False
    )


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
                    html.Th("Ratio watch",scope='col',className='text-center align-middle'),
                    html.Th("Ratio",scope='col',className='text-center align-middle'),
                    html.Th("Streamers",scope='col',className='text-center align-middle'),
                    html.Th("Views",scope='col',className='text-center align-middle')
            ])
            ],className='thead-light')]
    tbody = []
    children = [
        dbc.Row([
            dbc.Col([html.H2("Game Stats",className="text-center text-primary")])
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
    app.run_server(debug=True, port=8888, use_reloader=True)