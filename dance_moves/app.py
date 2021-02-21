import dash
import dash_bootstrap_components as dbc

external_stylesheets = dbc.themes.LITERA


# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, title='Dance Video Analysis', suppress_callback_exceptions=True, external_stylesheets=[external_stylesheets])

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions']=True

server = app.server
