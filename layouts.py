#import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash
from components import Header #, print_button
from datetime import datetime as dt
from datetime import date, timedelta




######################## Random List of Jobs & DF ########################

import jobs
df = jobs.df

    
######################## End List of jobs ########################


######################## START index Layout ########################
layout_index =  html.Div([
    html.Div([
        # CC Header
        Header(),
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
                columns=[
                    {"name": i, "id": i} for i in df.columns
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
                        'backgroundColor': '#FF6347',
                        'color': 'Black',
                    }],
                data=df.head(5).to_dict('records'),
            ),
            html.Div(id='switches', style={'inline':'true'}, children=[
              html.Button(id='index-select-all', children="Select All"),
              daq.ToggleSwitch(
              id='my-toggle-switch',
              label='Abbreviated',
              labelPosition='left',
              style={'display':'inline-block'},
              value=False,
              color='Green'
              )]),
            html.Div(id='content', children=[html.P("Hi")])
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
                html.P("Index Job Table Here")
            ]
            )]
        ),
        ], className="subpage")
    ], className="page")

######################## END index Layout ########################


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
          data=df.loc[df['Processing Complete'] == "No"].to_dict('records')
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
                html.P("Alert Table Here")
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
