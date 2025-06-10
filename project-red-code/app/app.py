import os
import dash
import dash_bootstrap_components as dbc
import redis
import time

# connect to redis
client = redis.Redis(host='redis', port=6379, health_check_interval=30, decode_responses=True)

# set a key
client.set('test-key', 'MAKINON')

# get a value
value = client.get('test-key')
print(value)

debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
server = app.server
from pages.logReader import dataDict
app.layout = dash.html.Div([
    dbc.Navbar([
                dash.html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(dash.html.Img(src="assets/fsb_round_logo.png", height="50px")),
                            dbc.Col(dbc.NavbarBrand("Formula Student Bizkaia", className="ms-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="https://fsbizkaia.com",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.NavItem(dbc.NavLink(dbc.NavItem(dbc.NavLink("TEAM PAGE", href="https://fsbizkaia.com"))),style={'color':'#ffffff'}),
                dbc.NavItem(dbc.NavLink(dbc.NavItem(dbc.NavLink("SharePoint", href="https://fsbizkaia.sharepoint.com/_layouts/15/sharepoint.aspx"))),style={'color':'#12c3de'}),
                dbc.NavItem(dbc.NavLink(dbc.NavItem(dbc.NavLink("OVERALL", href=dash.page_registry['pages.telemetry']['path']))), style={'color':'red'}),
                dbc.NavItem(dbc.NavLink(dbc.NavItem(dbc.NavLink("ELECTRONICS", href=dash.page_registry['pages.electronics']['path']))), style={'color':'red'}),
                dbc.NavItem(dbc.NavLink(dbc.NavItem(dbc.NavLink("POWERTRAIN", href=dash.page_registry['pages.powertrain']['path']))), style={'color':'red'}),
                dbc.NavItem(dbc.NavLink(dbc.NavItem(dbc.NavLink("CHECKS", href=dash.page_registry['pages.electronics']['path']))), style={'color':'red'}),
                dbc.NavItem(dbc.NavLink(dbc.NavItem(dbc.NavLink("SIMULATION", href=dash.page_registry['pages.electronics']['path']))), style={'color':'red'}),
                dbc.NavItem(dbc.NavLink(dbc.NavItem(dbc.NavLink("COOLING", href=dash.page_registry['pages.electronics']['path']))), style={'color':'red'}),
                dbc.NavItem(dbc.NavLink(dbc.NavItem(dbc.NavLink("ACCUMULATOR", href=dash.page_registry['pages.electronics']['path']))), style={'color':'red'})
            ],
        color="dark",
        dark=True,

    ),

        dash.page_container

    ],
    className="body"
)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8050", debug=debug)
    