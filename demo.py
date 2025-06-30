"""
Demonstration application for the Dash Auto Save State plugin.
This app showcases how to use the plugin to automatically persist
the state of various form components.
"""

import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback

# Corrected import: Import from the package name, not the __init__ file.
# This works after installing the package with `pip install -e .`
from dash_auto_save_state import enable_auto_save

# --- 1. App Initialization and Data ---
# Sample data for the chart
df = px.data.iris()

# Initialize the Dash app with a Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# --- 2. App Layout ---
# The layout is defined before enabling auto-save so that the plugin
# can find all the components to which it needs to attach callbacks.
app.layout = dbc.Container(
    [
        # This dcc.Store component is ESSENTIAL for the plugin to work.
        # It uses the browser's localStorage to persist data across sessions.
        dcc.Store(id='auto-save-storage', storage_type='local'),

        html.H1('Dash Auto Save State Demo', className='mb-4'),

        dbc.Alert(
            [
                html.H4('🚀 Auto-Save is Active!', className='alert-heading'),
                html.P(
                    'Try filling out the form below, then refresh the page. '
                    'Your data will be automatically restored!'
                ),
                html.P(
                    'Open the browser console (F12) to see debug messages.',
                    className='mb-0 small text-muted',
                ),
            ],
            color='success',
            className='mb-4',
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader('Personal Information'),
                            dbc.CardBody(
                                [
                                    # Various input components to test auto-save
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    dbc.Label('Full Name'),
                                                    dcc.Input(
                                                        id='full-name',
                                                        type='text',
                                                        placeholder='Enter your full name',
                                                        style={'width': '100%'},
                                                    ),
                                                ],
                                                md=6,
                                            ),
                                            dbc.Col(
                                                [
                                                    dbc.Label('Email'),
                                                    dcc.Input(
                                                        id='email',
                                                        type='email',
                                                        placeholder='Enter your email',
                                                        style={'width': '100%'},
                                                    ),
                                                ],
                                                md=6,
                                            ),
                                        ],
                                        className='mb-3',
                                    ),
                                    dcc.Dropdown(
                                        id='country',
                                        options=[
                                            {'label': 'United States', 'value': 'us'},
                                            {'label': 'Canada', 'value': 'ca'},
                                            {'label': 'United Kingdom', 'value': 'uk'},
                                        ],
                                        placeholder='Select your country',
                                        className='mb-3',
                                    ),
                                    dcc.Textarea(
                                        id='comments',
                                        placeholder='Tell us about yourself...',
                                        style={'width': '100%', 'height': 100},
                                        className='mb-3',
                                    ),
                                    dcc.Input(
                                        id='sensitive-field',
                                        type='password',
                                        placeholder='This field is excluded from auto-save',
                                        style={'width': '100%'},
                                    ),
                                    dbc.FormText(
                                        'This field is excluded for security.'
                                    ),
                                ]
                            ),
                        ]
                    ),
                    md=6,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader('Preferences'),
                            dbc.CardBody(
                                [
                                    dbc.Label('Notification Preferences'),
                                    dcc.Checklist(
                                        id='notifications',
                                        options=[
                                            {'label': ' Email', 'value': 'email'},
                                            {'label': ' SMS', 'value': 'sms'},
                                        ],
                                        value=['email'],
                                    ),
                                    html.Hr(),
                                    dbc.Label('Preferred Contact Method'),
                                    dcc.RadioItems(
                                        id='contact-method',
                                        options=[
                                            {'label': ' Email', 'value': 'email'},
                                            {'label': ' Phone', 'value': 'phone'},
                                        ],
                                        value='email',
                                        inline=True,
                                    ),
                                    html.Hr(),
                                    dbc.Label('Budget Range'),
                                    dcc.RangeSlider(
                                        id='budget-range',
                                        min=0,
                                        max=10000,
                                        step=500,
                                        value=[2000, 5000],
                                        marks={
                                            i * 2500: f'${i*2.5}K'
                                            for i in range(5)
                                        },
                                    ),
                                ]
                            ),
                        ]
                    ),
                    md=6,
                ),
            ],
            className='mb-4',
        ),

        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader('Chart Preferences'),
                        dbc.CardBody(
                            [
                                dcc.Dropdown(
                                    id='chart-type',
                                    options=[
                                        {'label': 'Scatter Plot', 'value': 'scatter'},
                                        {'label': 'Bar Chart', 'value': 'bar'},
                                    ],
                                    value='scatter',
                                    className='mb-3',
                                ),
                                dcc.Graph(id='sample-chart'),
                            ]
                        ),
                    ]
                ),
                md=12,
            )
        ),
    ],
    fluid=True,
)


# --- 3. Enable Auto-Save ---
# This function is called AFTER the layout is defined.
# It inspects the layout, finds all savable components, and creates
# the necessary callbacks to link them to the 'auto-save-storage'.
enable_auto_save(
    app=app,
    debug=True,  # Prints helpful messages to the console
    excluded_components=['sensitive-field'],  # A list of IDs to ignore
)


# --- 4. App Callbacks ---
@callback(
    Output('sample-chart', 'figure'),
    Input('chart-type', 'value'),
)
def update_chart(chart_type):
    """Updates the chart based on the selected chart type."""
    if chart_type == 'scatter':
        return px.scatter(
            df,
            x='sepal_length',
            y='sepal_width',
            color='species',
            title='Iris Dataset: Sepal Length vs. Width',
        )
    elif chart_type == 'bar':
        return px.bar(
            df.groupby('species')['sepal_length'].mean().reset_index(),
            x='species',
            y='sepal_length',
            title='Average Sepal Length by Species',
        )
    return {}


# --- 5. Run the App ---
if __name__ == '__main__':
    app.run(debug=True, port=8050)
