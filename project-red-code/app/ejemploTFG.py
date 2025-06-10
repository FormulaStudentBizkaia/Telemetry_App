import dash_daq as daq
import dash
from dash import  Input, Output, callback


app = dash.Dash(__name__)

app.layout = dash.html.Div([
    daq.Indicator(
        id='my-indicator-1',
        label="Default",
    ),
    dash.html.Button(
        'On/Off',
        id='my-indicator-button-1',
        n_clicks=0
    ),
])

@callback(
    Output('my-indicator-1', 'value'),
    Input('my-indicator-button-1', 'n_clicks')
)
def update_output(value):
    return True if value % 2 == 0 else False

if __name__ == '__main__':
    app.run(debug=True)





