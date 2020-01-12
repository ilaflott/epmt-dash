"""Configure the Dash server and load the layout"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
import layouts as lay
import callbacks  # pylint: disable=unused-import


def init_app():
    """
    Configure initial layout
    """
    # see https://dash.plot.ly/external-resources to alter header, footer and favicon
    app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>EPMT Job Display</title>
            {%favicon%}
            {%css%}
        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''
    # <img src="\\assets\\cc_logo.jpeg" width="120" height="120">

    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])

# Update page
# # # # # # # # #


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'),
               Input('url', 'href')])
def display_page(pathname, pfullurl):
    """Method:
    For displaying/returning all layouts as requested by url
    """
    app.fullurl = pfullurl
    if pathname == '' or pathname == '/':
        return lay.recent_jobs_page
    elif pathname == '/unprocessed/':
        return lay.layout_unprocessed
    elif pathname == '/alerts/':
        return lay.layout_alerts
    elif pathname == '/refs/':
        return lay.layout_references
    elif pathname == '/table/':
        return lay.layouts(pfullurl)
    else:
        return lay.noPage

if __name__ == '__main__':
    from logging import getLogger, basicConfig, DEBUG, ERROR, INFO, WARNING # pylint: disable=unused-import
    logger = getLogger(__name__)  # pylint: disable=invalid-name
    basicConfig(level=DEBUG)
    init_app()
    app.run_server(debug=True, host='0.0.0.0')
