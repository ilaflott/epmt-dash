import dash_html_components as html
import dash_core_components as dcc

def Header():
    return html.Div([
        #get_logo(),
        get_header(),
        html.Br([]),
        get_menu()
    ])

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
    menu = html.Div([

        dcc.Link('Overview - Recent Jobs', href='/', className="tab first"),

        dcc.Link('Overview - Unprocessed Jobs', href='/unprocessed/', className="tab"),

        dcc.Link('Alert Jobs', href='/alerts/', className="tab"),

        # dcc.Link('Menu Entry', href='/url/', className="tab"),

    ], className="row ")
    return menu
