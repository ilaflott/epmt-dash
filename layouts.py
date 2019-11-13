#import dash_bootstrap_components as dbc
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



######################## Random List of Jobs & DF ########################

import jobs
joblist = jobs.job_gen()
df = joblist.df


    
######################## End List of jobs ########################


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

layout_index =  html.Div([
    html.Div([
        # CC Header
        html.Div(style={'inline':'true'},children=[
        Header(),
        html.Div(id='switches', style={'inline':'true'}, children=[
              daq.ToggleSwitch(
              id='raw-switch',
              label='Raw Data',
              # labelPosition='left',
              style={'display':'inline-block','fontsize':'medium'}, # Set font size so it's not randomly inherited between browsers
              value=False,
              color='Green'
              ),
        ]),
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
                #filter_action="native",
                #style_as_list_view=True,
                columns=[
                    {"name": i, "id": i} for i in df.columns
                ],
                fixed_rows={ 'headers': True, 'data': 0 },
                #fixed_columns={ 'headers': True, 'data': 1 },#, Css is not setup for this
                style_header={
                  #'overflow': 'visible',
                  'font-size':'15px',
                  'padding': '5px',
                  'whiteSpace':'normal',
                },
                style_cell={
                  'font-family':'sans-serif',
                  'font-size':'16px',
                  'overflow': 'hidden',
                  'minWidth': '95px',
                  #'textOverflow': 'ellipsis',
                },
                style_table={
                'padding': '5px',
                #'height': '600px'
                },
                style_header_conditional=[
                     {
                    'if': {'column_id': 'tags'},
                    'text-align': 'left',
                    },
                    {
                    'if': {'column_id': 'Job ID'},
                    'text-align': 'right',
                    },
                    
                ],
                style_data_conditional=[
                    {'if': {'filter_query': '{Exit Status} != 0'},
                        'backgroundColor': '#FFc0b5'
                    },
                    # Shrink Narrow columns
                    {
                    'if': {'column_id': 'bytes_in (Gb)'},
                    'minWidth': '75px',
                    },
                    {
                    'if': {'column_id': 'bytes_out (Gb)'},
                    'minWidth': '75px',
                    },
                    {
                    'if': {'column_id': 'Exit Status'},
                    'minWidth': '60px',
                    },
                    {
                    'if': {'column_id': 'Processing Complete'},
                    'minWidth': '80px',
                    },

                    {
                    'if': {'column_id': 'Job ID'},
                    'text-align': 'right',
                    },
                    {
                    'if': {'column_id': 'tags'},
                    'text-align': 'left',
                    }
                    ],
            ),
            html.Div(id='lower-menu', style={'inline':'true'}, children=[
              html.Button(id='index-select-all', children="Select All"),
            html.Button('New Data', id='new-data-button'),
            html.Div(id='content', children=[]),
            html.Div(id='content2')
        ]),
        html.Script('''window.alert("sometext");''')

        ], className="subpage"),
        Footer()
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

######################## START References Layout ########################
import pandas as pd
refs = {1:["ref1",['tag1:tag1','tag2:tag2'],['job1','job2'],['duration','cpu_time','num_procs']],
        2:["ref2",['tag1:tag1','tag2:tag2'],['job1','job2'],['duration','cpu_time','num_procs']],
        3:["ref3",['tag1:tag1','tag2:tag2'],['job1','job2'],['duration','cpu_time','num_procs']],
        4:["ref4",['tag1:tag1','tag2:tag2'],['job1','job2'],['duration','cpu_time','num_procs']]}
ref_df = pd.DataFrame(refs)
ref_df = ref_df.transpose()
ref_df.rename(columns={0:"Model",1:"Tags",2:"Jobs",3:"Features"},inplace=True)
from json import dumps
ref_df['Tags'] = ref_df['Tags'].apply(dumps)
ref_df['Jobs'] = ref_df['Jobs'].apply(dumps)
ref_df['Features'] = ref_df['Features'].apply(dumps)
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
                id='table-multicol-sorting',
                row_selectable="multi",
                sort_action='native',
                #sort_mode='multi', Keeping it simple now
                #data=df.head(10).to_dict('records'), # Do not display data initially, callback will handle it
                #filter_action="native",
                #style_as_list_view=True,
                columns=[
                    {"name": i, "id": i} for i in ref_df.columns
                ],
                data=ref_df.to_dict('records'),
                fixed_rows={ 'headers': True, 'data': 0 },
                #fixed_columns={ 'headers': True, 'data': 1 },#, Css is not setup for this
                style_header={
                  #'overflow': 'visible',
                  'font-size':'18px',
                  'padding': '10px',
                  'whiteSpace':'normal',
                  'width':'90px'
                  #'height':'100%'
                  #'text-align':'center',
                },
                style_cell={
                  'font-family':'sans-serif',
                  'font-size':'16px',
                  'overflow': 'hidden',
                  'minWidth': '40px'#, 'maxWidth': '140px',
                },
                style_table={
                'padding': '5px',
                },
                style_header_conditional=[
                    {
                    'if': {'column_id': 'Job ID'},
                    'text-align': 'right',
                    }
                ],
                style_data_conditional=[
                    {
                      'if': {'column_id': 'Job ID'},
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
