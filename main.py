import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.figure_factory as ff
from dash import Input, Output, dcc, html, State
import numpy as np
import plotly.graph_objects as go
from plotly.colors import n_colors
import plotly.express as px

DATA = pd.read_csv("https://cdn.opensource.faculty.ai/old-faithful/data.csv")

df_global = pd.read_csv("data processing/data/global_viewers.csv",index_col=0,parse_dates=True)

app = dash.Dash(external_stylesheets=[dbc.themes.PULSE])

data = (np.linspace(1, 2, 12)[:, np.newaxis] * np.random.randn(12, 200) +
            (np.arange(12) + 2 * np.random.random(12))[:, np.newaxis])

colors = n_colors('rgb(5, 200, 200)', 'rgb(200, 10, 10)', 12, colortype='rgb')

fig_ridge = go.Figure()
for data_line, color in zip(data, colors):
    fig_ridge.add_trace(go.Violin(x=data_line, line_color=color))

fig_ridge.update_traces(orientation='h', side='positive', width=3, points=False)
fig_ridge.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)


fig_global = px.line(df_global)


dropdown = html.Div(
    [
        dbc.Label("Number of bins in histogram (approximate):"),
        dcc.Dropdown(
            id="dropdown",
            options=[{"label": n, "value": n} for n in [10, 20, 35, 50]],
            value=20,
        ),
    ]
)


hours_watched = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Total numbers of hours watched", className="card-title text-center"),
                html.H1("123213", className="card-text text-center")
            ]
            
        )
    
    ]
)




PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

game_dropwdown = dcc.Dropdown(
            id='dropwdown-game',
            options=[
                {'label': 'Game1', 'value': 'Game1'},
                {'label': 'Game2', 'value': 'Game2'},
                {'label': 'Game3', 'value': 'Game3'}
            ],
            value='Game1'
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
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Twitch to the Moon", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
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


home = dbc.Container(
    [
        dcc.Graph(figure=fig_global),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(hours_watched),
                dbc.Col(hours_watched, align="center"),
                # dbc.Col(dropdown),
                # dbc.Col(checklist, width="auto", align="center"),
            ]
        ),
        dcc.Graph(figure=fig_ridge)

    ]
)

def game_page(game):
    return dbc.Container([
        html.H1(game,className="text-center mt-5"),
        dcc.Graph(figure=fig_global),# figure=fig_game_global
        dcc.Graph(figure=fig_global)# figure=fig_game_domination
    ])

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

content = html.Div(id="page-content")

app.layout = html.Div([dcc.Location(id="url"), navbar, content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    link = pathname.split("/")
    print(link)
    if pathname == "/":
        return home
    elif link[1]=="game":
        return game_page(link[2])
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

if __name__ == "__main__":
    app.run_server(debug=True, port=8888, use_reloader=True)