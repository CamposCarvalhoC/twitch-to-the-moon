import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.figure_factory as ff
from dash import Input, Output, dcc, html, State
import numpy as np
import plotly.graph_objects as go
from plotly.colors import n_colors

DATA = pd.read_csv("https://cdn.opensource.faculty.ai/old-faithful/data.csv")

app = dash.Dash(external_stylesheets=[dbc.themes.PULSE])

data = (np.linspace(1, 2, 12)[:, np.newaxis] * np.random.randn(12, 200) +
            (np.arange(12) + 2 * np.random.random(12))[:, np.newaxis])

colors = n_colors('rgb(5, 200, 200)', 'rgb(200, 10, 10)', 12, colortype='rgb')

fig_ridge = go.Figure()
for data_line, color in zip(data, colors):
    fig_ridge.add_trace(go.Violin(x=data_line, line_color=color))

fig_ridge.update_traces(orientation='h', side='positive', width=3, points=False)
fig_ridge.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)

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

checklist = html.Div(
    [
        dbc.Label("Extras:"),
        dbc.Checklist(
            id="checklist",
            options=[
                {"label": "Show Sdsdsdsindividual observations", "value": "show_ind"},
                {"label": "Show density estimate", "value": "show_dens"},
            ],
            value=[],
            inline=True,
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





@app.callback(
    Output("graph", "figure"),
    [Input("dropdown", "value"), Input("checklist", "value")],
)
def make_graph(dropdown_value, checklist_value):
    bin_size = (DATA.eruptions.max() - DATA.eruptions.min()) / dropdown_value
    fig = ff.create_distplot(
        [DATA.eruptions],
        ["Eruption duration"],
        bin_size=bin_size,
        show_curve="show_dens" in checklist_value,
        show_rug="show_ind" in checklist_value,
    )
    fig["layout"].update(
        {
            "title": "Geyser eruption duration",
            "showlegend": False,
            "xaxis": {"title": "Duration (minutes)"},
            "yaxis": {"title": "Density"},
        }
    )
    return fig


PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="info", className="ms-2", n_clicks=0
            ),
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
                        dbc.Col(dbc.NavbarBrand("Navbar", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("Page 1", href="/page-1", active="exact"),
                    dbc.NavLink("Page 2", href="/page-2", active="exact"),
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
        dcc.Graph(id="graph"),
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
    if pathname == "/":
        return home
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



if __name__ == "__main__":
    app.run_server(debug=True, port=8888, use_reloader=True)