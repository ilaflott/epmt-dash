#import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash
from components import Header #, print_button
from datetime import datetime as dt
from datetime import date, timedelta

from logging import getLogger, basicConfig, DEBUG, ERROR, INFO, WARNING
logger = getLogger(__name__)  # you can use other name



######################## Random List of Jobs & DF ########################

import jobs
joblist = jobs.job_gen()

df = joblist.df
    
######################## End List of jobs ########################


######################## START index Layout ########################
layout_index =  html.Div([
    html.Div([
        # CC Header
        html.Div(style={'inline':'true'},children=[
        Header(),
        html.Div(id='switches', style={'inline':'true'}, children=[
              daq.ToggleSwitch(
              id='raw-switch',
              label='Display Raw',
              # labelPosition='left',
              style={'display':'inline-block','fontsize':'medium'}, # Set font size so it's not randomly inherited between browsers
              value=False,
              color='Green'
              ),
        html.Button('New Data', id='new-data-button')]),
        ]),
        ]),
        # Date Picker
        
        # Header Bar
        html.Div([
          html.H6(["Recent Jobs"], className="gs-header gs-text-header padded",style={'marginTop': 15})
          ]),
        # Radio Button
        
        # Pageable table
        # dash_table.DataTable(
        #   id='table-multicol-sorting',
        #   columns=[
        #       {"name": i, "id": i} for i in sorted(df.columns)
        #   ],
        #   page_current=0,
        #   page_size=PAGE_SIZE,
        #   page_action='custom',

        #   sort_action='custom',
        #   sort_mode='multi',
        #   sort_by=[]
        #   ),
        #First Data Table
        html.Div([
            dash_table.DataTable(
                id='table-multicol-sorting',
                row_selectable="multi",
                sort_action='native',
                #sort_mode='multi', Keeping it simple now
                #data=df.head(10).to_dict('records'), # Do not display data initially, callback will handle it
                filter_action="native",
                #style_as_list_view=True,
                columns=[
                    {"name": i, "id": i} for i in df.columns
                ],
                fixed_rows={ 'headers': True, 'data': 0 },
                #fixed_columns={ 'headers': True, 'data': 1 },#, Css is not setup for this
                style_header={
                  #'overflow': 'visible',
                  'font-size':'18px',
                  'padding': '10px',
                  'whiteSpace':'normal',
                  #'height':'100%'
                  #'text-align':'center',
                },
                style_cell={
                  'font-family':'sans-serif',
                  'font-size':'16px',
                  'overflow': 'hidden',
                  #'textOverflow': 'ellipsis',
                  'minWidth': '120px'#, 'maxWidth': '140px',
                },
                style_table={
                'padding': '5px',
                'height': '600px'},
                style_header_conditional=[
                      #                {
                     #'if': {'column_id': 'tags'},
                     #'text-align': 'left',
                     #},
                    {
                    'if': {'column_id': 'Job ID'},
                    'text-align': 'right',
                    }
                ],
                style_data_conditional=[
                    #{
                    #    'if': {

                    #        'filter_query': '{Processing Complete} eq "No"'
                    #    },
                    #    'backgroundColor': '#FF6347',
                    #    'color': 'Black',
                    #},
                    {
                        'if': {

                            'filter_query': '{Exit Status} != 0'
                        },
                        'backgroundColor': '#FFc0b5'
                    },
                    {
                    'if': {'filter_query': '{Exit Status} != 0','column_id': 'Exit Status'},
                          'text-align': 'left',
                          'font-weight':'600',
                    },
                    #{
                    #'if': {'column_id': 'tags'},
                    #'text-align': 'left',
                    #},
                    {
                    'if': {'column_id': 'Job ID'},
                    'text-align': 'right',
                    }
                    ],
            ),
            html.Div(id='lower-menu', style={'inline':'true'}, children=[
              html.Button(id='index-select-all', children="Select All"),
            html.Div(id='content', children=[html.P("Hi")]),
            html.Div(id='content2')
        ]),
        html.Script('''window.alert("sometext");''')

        ], className="subpage")
    ], className="page")

######################## END index Layout ########################

unproc = df.loc[df['Processing Complete'] == "No"].to_dict('records')
logger.info(unproc)
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
            {"name": i, "id": i} for i in sorted(df.columns)
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
            {"name": i, "id": i} for i in sorted(df.columns)
          ],
          data=df.to_dict('records')
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
            {"name": i, "id": i} for i in sorted(df.columns)
          ],
          data=df.to_dict('records')
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
from app import fullurl
######################## START sample Layout ########################
layout_sample =  html.Div([
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
            {"name": i, "id": i} for i in sorted(df.columns)
          ],
          data=df.to_dict('records')
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
                html.P(fullurl)
            ]
            )]
        ),
        ], className="subpage")
    ], className="page")

######################## END sample Layout ########################

######################## 404 Page ########################
noPage = html.Div([ 
    # CC Header
    Header(),
    html.P(["404 Page not found"])
    ], className="no-page")
