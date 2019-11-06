import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
# see https://community.plot.ly/t/nolayoutexception-on-deployment-of-multi-page-dash-app-example-code/12463/2?u=dcomfort
from app import server
from app import app
from layouts import layout_index, layout_unprocessed, layout_alerts, noPage, layout_display, layout_sample
import callbacks
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)  # you can use other name

# see https://dash.plot.ly/external-resources to alter header, footer and favicon
app.index_string = ''' 
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>EPMT Job Display</title>
        {%favicon%}
        {%css%}
        <script>
        $(document).ready(function(){
        // jQuery methods go here...
        document.getElementById('expanded-row--empty-cell dash-select-header').innerHTML = 'Test';

        });
        </script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div>Experiment Performance Management Tool - Minimal Metrics LLC
        <p style="float: right">
        <img src="\\assets\\cc_logo.jpeg" width="120" height="120"></p>
        </div>
        <div style="clear: both;"></div>
    </body>
</html>
'''

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
# Update page
# # # # # # # # #

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'),
              Input('url', 'href')])
def display_page(pathname,pfullurl):
    from app import fullurl
    fullurl = pfullurl
    if pathname == '' or pathname == '/':
        return layout_index
    elif pathname == '/unprocessed/':
        return layout_unprocessed
    elif pathname == '/alerts/':
        return layout_alerts
    elif pathname == '/table/':
        from urllib.parse import parse_qs, urlparse
        # https://docs.python.org/3/library/urllib.parse.html
        # Parse URL using pfullurl
        logger.info("URL:{}".format(pfullurl))
        logger.debug(parse_qs(urlparse(pfullurl).query))
        ji = parse_qs(urlparse(pfullurl).query)
        logger.debug("jobids{}".format(ji['jobid'][0].split(',')))
        qjobids = ji['jobid'][0].split(',')
        # Generate DF for next layout
        from layouts import df
        logger.info(df.loc[df['Job ID'].isin(qjobids)])
        return layout_sample
    else:
        return noPage

# # # # # # # # #
# detail the way that external_css and external_js work and link to alternative method locally hosted
# # # # # # # # #
#external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
#                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
#                "https://fonts.googleapis.com/css?family=Raleway:400,300,600",
#                "https://codepen.io/bcd/pen/KQrXdb.css",
#                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
#                ]#"https://codepen.io/dmcomfort/pen/JzdzEZ.css"]


#for css in external_css:
    #app.css.append_css({"external_url": css})

#external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
#               "https://codepen.io/bcd/pen/YaXojL.js"]

#for js in external_js:
#    app.scripts.append_script({"external_url": js})

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
