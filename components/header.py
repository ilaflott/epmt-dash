import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_daq as daq

def Header():
    return html.Div([
        #get_logo(),
        get_header(),
        html.Br([]),
        get_menu()
    ])

from jobs import get_version
def Footer():
    # https://gitlab.com/minimal-metrics-llc/epmt/epmt-dash/issues
    return html.Div(["Experiment Performance Management Tool - ", html.Div(id='version',children=[dcc.Link(get_version() + " Issue Tracker",href='https://gitlab.com/minimal-metrics-llc/epmt/epmt-dash/issues')],style={'width': '49%', 'display': 'inline-block'})])

def get_logo():
    logo = html.Div([

        html.Div([
            html.Img(src='https://pbs.twimg.com/profile_images/779313079289077761/f2YOWoLW_400x400.jpg', height='101', width='141')
        ], className="ten columns padded"),

        # html.Div([
        #     dcc.Link('Full View   ', href='/cc-travel-report/full-view')
        # ], className="two columns page-view no-print")

    ], className="row gs-header")
    return logo


def get_header():
    header = html.Div([

        html.Div([
            html.H5(
                'Experiment Performance Management Tool')
        ], className="twelve columns padded")

    ], className="row gs-header gs-text-header")
    return header


def get_menu():
    menu = dbc.Container([
        dbc.Row(
            [
                dbc.Col([
                html.Div([
                    dcc.Link('Overview - Recent Jobs', href='/', className="tab first"),
                    dcc.Link('Models', href='/refs/', className="tab"),
                    dcc.Link('Alert Jobs', href='/alerts/', className="tab")])
                ],width="auto"),
                dbc.Col(
                        dcc.Input(placeholder='Search/Filter...',
                            type='text',
                            value='',
                            style={'display':'block','width':'100%'}
                        ),
                    width="auto",
                    #md=3,
                    lg=6
                    ),
                html.Div(id='switches', 
                    children=[
                    dbc.Col(
                        daq.ToggleSwitch(
                            id='raw-switch',
                            label='Raw Data',
                            # labelPosition='left',
                            #style={'display':'inline-block','fontsize':'medium'}, # Set font size so it's not randomly inherited between browsers
                            value=False,
                            color='Green'
                        ),
                    width="auto"
                    )
                    ]
                ),
            ],
            justify="between",
            align="center"
            )
    ], fluid=True)
    return menu
                    #dcc.Linhtml.Div(k('Overview - Unprocessed Jobs', href='/unprocessed/', className="tab"),
