import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash
from components import Header, Footer #, print_button
from datetime import datetime as dt
from datetime import date, timedelta
from logging import getLogger, basicConfig, DEBUG, ERROR, INFO, WARNING
logger = getLogger(__name__)  # you can use other name

DEFAULT_ROWS_PER_PAGE = 30

########################Jobs & References ########################
from jobs import job_gen
job_df = job_gen().df

from refs import get_references
ref_df = get_references()
######################## End Jobs & References ########################


######################## START index Layout ########################

# Autosizing Columns
# Need to export this
def create_conditional_style(df):
    PIXEL_FOR_CHAR = 10
    style=[]
    for col in df.columns:
        name_length = len(col)
        pixel = 50 + round(name_length * PIXEL_FOR_CHAR)
        pixel = str(pixel) + "px"
        style.append({'if': {'column_id': col}, 'minWidth': pixel})
    return style

recent_jobs_page =  html.Div([
    html.Div([
        # CC Header
        html.Div(style={'inline':'true'},children=[
        Header(),
        ]),
        ]),
        # These tabs are huge
        # https://community.plot.ly/t/adjusting-height-of-tabs/13136/5
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Recent Jobs', children=[
                dbc.Row([
                  # Selected jobs notification
                  dbc.Col([
                  html.Div(id='content',style={'inline':'true'}, children=[])]),
                # Search box query notification
                dbc.Col([html.Div(id='content2')]),
                # Models created notification
                dbc.Col([html.Div(style={'inline':'true'},children=["Model Status:",
                          html.Div(id='recent-job-model-status',
                                   children='')
                          ])])
                ]),
        #First Data Table
        html.Div([
            dash_table.DataTable(
                id='table-multicol-sorting',
                row_selectable="multi",
                page_current=0,
                page_size=DEFAULT_ROWS_PER_PAGE,
                page_action='custom',
                sort_action='custom',
                sort_by=[],
                #sort_mode='multi', Keeping it simple now
                #data=df.head(10).to_dict('records'), # Do not display data initially, callback will handle it
                #filter_action="native",
                #style_as_list_view=True,
                columns=[
                    {"name": i, "id": i} for i in job_df.columns
                ],
                fixed_rows={ 'headers': True, 'data': 0 },
                #fixed_columns={ 'headers': True, 'data': 1 },#, Css is not setup for this
                style_table={
                'padding': '5px',
                #'height': '430px',
                'font-size':'14px'
                },
                style_header={
                  'font-weight':'bold',
                  'padding': '5px',
                  'whiteSpace':'normal',
                  #'overflow': 'visible',
                  #'font-size':'14px',
                },
                style_cell={
                  'font-family':'sans-serif',
                  'overflow': 'hidden',
                  'minWidth': '100px',
                  #'font-size':'14px',
                  #'textOverflow': 'ellipsis',
                },
                style_header_conditional=[
                     {
                    'if': {'column_id': 'tags'},
                    'text-align': 'left',
                    },
                    {
                    'if': {'column_id': 'job id'},
                    'text-align': 'right',
                    },
                    
                ],
                style_data_conditional=[
                    {'if': {'filter_query': '{exit status} != 0'},
                        'backgroundColor': '#FFc0b5'
                    },
                    # Shrink Narrow columns
                    {
                    'if': {'column_id': 'bytes_in (Gb)'},
                    'minWidth': '75px',
                    },
                    {
                    'if': {'column_id': 'job id'},
                    'minWidth': '40px',
                    },
                    {
                    'if': {'column_id': 'bytes_out (Gb)'},
                    'minWidth': '75px',
                    },
                    {
                    'if': {'column_id': 'exit status'},
                    'minWidth': '50px',
                    },
                    {
                    'if': {'column_id': 'processing complete'},
                    'minWidth': '80px',
                    },

                    {
                    'if': {'column_id': 'job id'},
                    'text-align': 'right',
                    },
                    {
                    'if': {'column_id': 'tags'},
                    'text-align': 'left',
                    }
                    ],
            ),
    dbc.Row([
      dbc.Col([
            html.Button(id='run-analysis-btn', children="Run Analysis", n_clicks_timestamp=0, style={'background-color':'#20c997','color':'#020080'}),
      ], width='auto'),
      dbc.Col([
            html.Button(id='create-newModel-btn', children="Create Model", n_clicks_timestamp=0),
      ], width='auto'),
      dbc.Col([
            html.Button(id='index-select-all', children="Select All"),
      ], width='auto'),dbc.Col([
        html.Div(style={'display':'block','width':'360px','text-align':'center'},children=[
            dcc.DatePickerRange(
              id='jobs-date-picker',
              min_date_allowed=dt(1990, 1, 1),
              max_date_allowed=dt(2040, 12, 25),
              clearable=True,
              with_portal=True,
              show_outside_days=True,
              minimum_nights=0
            ),"(Inclusive Date Selections)"]),
      ],width='auto'),
      dbc.Col([
          dcc.Dropdown(
              id='row-count-dropdown',
              options=[
                  {'label': '5 Rows', 'value': '5'},
                  {'label': '30 Rows', 'value': '30'},
                  {'label': '50 Rows', 'value': '50'},
                  {'label': '1000 Rows', 'value': '1000'}
              ],
              clearable=False,
              searchable=False,
              value=DEFAULT_ROWS_PER_PAGE
          )
      ], width=2),
      # df.shape[0]
      # Old Page attempt
      #dbc.Col(['Page:'], html.Div(id="page-selector", children=[dcc.Link(str(n+1)+", ",href="?page="+str(n)) for n in range((job_df.shape[0]//DEFAULT_ROWS_PER_PAGE))])
      #, width='auto'),
          #','.join([str(n+1) for n in range((job_df.shape[0]//DEFAULT_ROWS_PER_PAGE))]),
      dbc.Col([
        "[ ",
        job_df.shape[0],
        " Jobs Total ]"
      ], width='auto'),
      
        
    ],)


        ], className="subpage"),
            ]),
      # Reference model datatable tab
      dcc.Tab(label='Models', children=[
        
        html.Div([
          html.H6(["Reference Models"], className="gs-header gs-text-header padded",style={'marginTop': 15})
          ]),
        # Radio Button
        
        html.Div([
          # The inline dropdowns are broken[not displayed] due to my sorting css work on column headers
          dash_table.DataTable(
                id='table-ref-models',
                row_selectable="single",
                sort_action='native',
                #sort_mode='multi', Keeping it simple now
                #data=df.head(10).to_dict('records'), # Do not display data initially, callback will handle it
                #filter_action="native",
                #style_as_list_view=True,
                columns=[
                    {"name": i, "id": i} for i in ref_df.columns
                    #{"name":"Model","id":"Model"},
                    #{"name":"Active","id":"Active"},#,"presentation":"dropdown"},
                    #{"name":"Tags","id":"Tags"},
                    #{"name":"Jobs","id":"Jobs"},
                    #{"name":"Features","id":"Features"},
                ],
                data=ref_df.to_dict('records'),
                #editable=True,
                dropdown={
                    'Active': {
                        'options': [
                            {'label': i, 'value': i}
                            for i in ['True','False']
                        ]
                    }
                },
                fixed_rows={ 'headers': True, 'data': 0 },
                #fixed_columns={ 'headers': True, 'data': 1 },#, Css is not setup for this
                style_header={
                  #'overflow': 'visible',
                  'font-size':'19px',
                  'font-weight':'bold',
                  'padding': '10px',
                  'whiteSpace':'normal',
                  #'width':'90px',
                  #'height':'40px'
                  #'text-align':'center',
                },
                style_cell={
                  'font-family':'sans-serif',
                  #'font-size':'16px',
                  #'overflow': 'hidden',
                  'minWidth': '70px',#, 'maxWidth': '140px',
                  'height':'50px'
                },
                style_table={
                'padding': '5px',
                },
                style_header_conditional=[
                    {
                    'if': {'column_id': 'job id'},
                    'text-align': 'right',
                    }
                ],
                style_data_conditional=[
                    {
                      'if': {'column_id': 'job id'},
                      'text-align': 'right',
                    }
                ],
            ),
            html.Button(id='toggle-Model-btn', children="Toggle Model Status", n_clicks_timestamp=0),
            html.Button(id='delete-Model-btn', children="Delete Model", n_clicks_timestamp=0, style={'background-color':'#ff0000','color':'#000000'}),
        ]),

        
        ])
          ]),
        Footer()
    ], className="page")

######################## END index Layout ########################

unproc = job_df.loc[job_df['processing complete'] == "No"].to_dict('records')
#logger.info(unproc)
######################## START unprocessed Layout ########################
layout_unprocessed =  html.Div([
    html.Div([
        # CC Header
        Header(),
        # Date Picker
        
        # Header Bar
        html.Div([
          html.H6(["Unprocessed Jobs"], className="gs-header gs-text-header padded",style={'marginTop': 15})
          ]),
        # Radio Button
        
        # First Data Table
        html.Div([
          dash_table.DataTable(
          id='table-multicol-sorting',
          columns=[
            {"name": i, "id": i} for i in sorted(job_df.columns)
          ],
          data=unproc
          )
        ]),
        # GRAPHS
        html.Div([
          html.Div(
            id='update_graph_1'
            ),
            html.Div([
                html.P("Unprocessed Table Here")
            ]
            )]
        ),
        ], className="subpage")
    ], className="page")

######################## END unprocessed Layout ########################

######################## START References Layout ########################
layout_references =  html.Div([
    html.Div([
        # CC Header
        Header(),
        # Date Picker
        
        # Header Bar
        html.Div([
          html.H6(["Reference Models"], className="gs-header gs-text-header padded",style={'marginTop': 15})
          ]),
        # Radio Button
        
        # First Data Table
        html.Div([
          dash_table.DataTable(
                id='table-ref-models',
                row_selectable="multi",
                sort_action='native',
                #sort_mode='multi', Keeping it simple now
                #data=df.head(10).to_dict('records'), # Do not display data initially, callback will handle it
                #filter_action="native",
                #style_as_list_view=True,
                columns=[
                    #{"name": i, "id": i, "presentation":"dropdown"} for i in ref_df.columns
                    {"name":"Model","id":"Model"},
                    {"name":"Active","id":"Active","presentation":"dropdown"},
                    {"name":"Tags","id":"Tags"},
                    {"name":"Jobs","id":"Jobs"},
                    {"name":"Features","id":"Features"},
                ],
                data=ref_df.to_dict('records'),
                editable=True,
                dropdown={
                    'Active': {
                        'options': [
                            {'label': i, 'value': i}
                            for i in ['True','False']
                        ]
                    }
                },
                fixed_rows={ 'headers': True, 'data': 0 },
                #fixed_columns={ 'headers': True, 'data': 1 },#, Css is not setup for this
                style_header={
                  #'overflow': 'visible',
                  'font-size':'19px',
                  'font-weight':'bold',
                  'padding': '10px',
                  'whiteSpace':'normal',
                  #'width':'90px',
                  #'height':'40px'
                  #'text-align':'center',
                },
                style_cell={
                  'font-family':'sans-serif',
                  #'font-size':'16px',
                  #'overflow': 'hidden',
                  'minWidth': '70px',#, 'maxWidth': '140px',
                  'height':'50px'
                },
                style_table={
                'padding': '5px',
                },
                style_header_conditional=[
                    {
                    'if': {'column_id': 'job id'},
                    'text-align': 'right',
                    }
                ],
                style_data_conditional=[
                    {
                      'if': {'column_id': 'job id'},
                      'text-align': 'right',
                    }
                ],
            )
        ]),

        ], className="subpage")
    ], className="page")
######################## END References Layout ########################


######################## START Display Layout ########################
layout_display =  html.Div([
    html.Div([
        # CC Header
        Header(),
        # Date Picker
        
        # Header Bar
        html.Div([
          html.H6(["Layout Display"], className="gs-header gs-text-header padded",style={'marginTop': 15})
          ]),
        # Radio Button
        
        # First Data Table
        html.Div([
          dash_table.DataTable(
          id='table-multicol-sorting',
          columns=[
            {"name": i, "id": i} for i in sorted(job_df.columns)
          ],
          data=job_df.to_dict('records')
          )
        ]),
        # Download Button
        html.Div([
          html.A(html.Button('Download Data', id='download-button'), id='download-link-ga-category')
          ]),
        # Second Data Table
        
        # GRAPHS
        html.Div([
          html.Div(
            id='update_graph_1'
            ),
            html.Div([
                html.P("Graph Here")
            ]
            )]
        ),
        ], className="subpage")
    ], className="page")

######################## END Display Layout ########################

######################## START alerts Layout ########################
layout_alerts =  html.Div([
    html.Div([
        # CC Header
        Header(),
        # Date Picker
        
        # Header Bar
        html.Div([
          html.H6(["Alert Jobs"], className="gs-header gs-text-header padded",style={'marginTop': 15})
          ]),
        # Radio Button
        
        # First Data Table
        html.Div([
          dash_table.DataTable(
          id='table-multicol-sorting',
          columns=[
            {"name": i, "id": i} for i in sorted(job_df.columns)
          ],
          data=job_df.to_dict('records')
          )
        ]),
        # Download Button
        html.Div([
          html.A(html.Button('Download Data', id='download-button'), id='download-link-ga-category')
          ]),
        # Second Data Table
        
        # GRAPHS
        html.Div([
          html.Div(
            id='update_graph_1'
            ),
            html.Div([
                html.P("Alert Table Here")
            ]
            )]
        ),
        ], className="subpage")
    ], className="page")


######################## END alerts Layout ########################

######################## START table Layout ########################
layout_sample =  html.Div([
    html.Div([
      #dcc.Location(id='url', refresh=False),
        html.Div([
          dash_table.DataTable(
          id='custom-table',
          columns=[
            {"name": i, "id": i} for i in sorted(job_df.columns)
          ],
          #data=df.to_dict('records')
          )
        ])
        ], className="subpage")
    ], className="page")


def layouts(pfullurl):
    from components import parseurl
    # offset = page * DEFAULT_ROWS_PER_PAGE
    q = parseurl(pfullurl)
    # Grab jobid values from query dict
    page = int(q['page'][0])
    job_df = job_gen(limit=DEFAULT_ROWS_PER_PAGE,offset=page*DEFAULT_ROWS_PER_PAGE).df
    jobids = q.get('jobid',None)
    logger.info(jobids)
    if jobids:
      logger.debug("{}\n{}".format(jobids,job_df.loc[job_df['job id'].isin(jobids)]))
      tableData = job_df.loc[job_df['job id'].isin(jobids)]
    else:
      tableData = job_df
    
    return html.Div([
      html.Div([
        #dcc.Location(id='url', refresh=False),
          html.Div([
            dash_table.DataTable(
            id='custom-table',
            columns=[
              {"name": i, "id": i} for i in sorted(tableData.columns)
            ],
            sort_action='native',
            data=tableData.to_dict('records'),
            fixed_rows={ 'headers': True, 'data': 0 },
                  #fixed_columns={ 'headers': True, 'data': 1 },#, Css is not setup for this
                  style_table={
                  'padding': '5px',
                  'height': '300px',
                  'font-size':'14px'
                  },
                  style_header={
                    'font-weight':'bold',
                    'padding': '5px',
                    'whiteSpace':'normal',
                    #'overflow': 'visible',
                    #'font-size':'14px',
                  },
                  style_cell={
                    'font-family':'sans-serif',
                    'overflow': 'hidden',
                    'minWidth': '100px',
                    #'font-size':'14px',
                    #'textOverflow': 'ellipsis',
                  },
            )
          ])
          ], className="subpage")
      ], className="page")

######################## END table Layout ########################

######################## 404 Page ########################
noPage = html.Div([ 
    # CC Header
    #Header(),
    html.P(["404 Page not found"])
    ], className="no-page")
