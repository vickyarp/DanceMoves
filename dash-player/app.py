import dash
import dash_bootstrap_components as dbc


external_stylesheets = dbc.themes.SPACELAB

#BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
#external_stylesheets = BS
#external_stylesheets = dbc.themes.LITERA

#SPACELAB
#XROMATISTA : SOLAR, JOURNAL

#CERULEAN, COSMO, CYBORG, DARKLY, FLATLY, JOURNAL, LITERA, LUMEN, LUX, MATERIA, MINTY, PULSE, SANDSTONE, SIMPLEX, SKETCHY, SLATE,



# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, title='Dance Video Analysis', suppress_callback_exceptions=True, external_stylesheets=[external_stylesheets])







#for mobile version
#app = dash.Dash(__name__, suppress_callback_exceptions=True,
 #               meta_tags=[{'name': 'viewport',
  #                          'content': 'width=device-width, initial-scale=1.0'}])


server = app.server