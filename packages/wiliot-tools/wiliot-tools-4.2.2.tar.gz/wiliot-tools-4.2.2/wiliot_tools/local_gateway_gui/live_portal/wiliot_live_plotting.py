import threading
import time
import numpy as np
import pandas as pd
import wiliot_tools.local_gateway_gui.live_portal.customized_filters as customized_filters
import dash
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.express as px

try:
    from wiliot_core.packet_data.extended.config_files.get_decoded_data_attributes import \
        get_all_decoded_data_fields_names
except Exception as e:
    def get_all_decoded_data_fields_names():
        pass

print('Live plotting requirements are installed')


class WiliotLivePlotting(object):

    def __init__(self, gw_instance, stop_event):
        self.live_plot_thread = None
        self.live_plots_data = None
        self.gw_instance = gw_instance
        self.packet_attributes_list = get_all_decoded_data_fields_names(only_num=True)
        self.filter_kernel = 5
        self.threshold_value = ''
        self.limit_history = False
        self.history_value = 0
        self.plot_hight = 300
        self.live_update = True
        self.show_filter = False
        self.show_threshold = False
        self.show_record = True
        self.record_slider_value = 10
        self.tags_record = {'REPLAY-02C6': 'live_portal/tag_records/26_07_2023__16_34_33_plot 2c6 no duplicates.csv',
                            'REPLAY-02CB': 'live_portal/tag_records/26_07_2023__16_34_33_plot 2cb no duplicates.csv'}
        self.live_plots_event = stop_event
        self.dash_app = None
        self.server = None

    def init_live_plot(self):
        def Header(name, app):
            title = html.H2(name, style={"margin-top": 5})
            logo = html.Img(
                src='https://www.wiliot.com/src/uploads/Wiliotlogo.png', style={"float": "right", "height": 50}
            )

            return dbc.Row([dbc.Col(title, md=9), dbc.Col(logo, md=3)])

        customized_filters_map = {
            'Median filter': customized_filters.median_filter_function,
            'Mean filter': customized_filters.mean_filter_function,
            'TTI filter': customized_filters.tti_filter_function,
        }

        h_style = {
            'display': 'flex',
            'flex-direction': 'row',
            'alignItems': 'center',
            'justifyContent': 'space-between',
            'margin': '5px'
        }
        h_style_block = {
            'display': 'flex',
            'flex-direction': 'row',
            'alignItems': 'center',
            'justifyContent': 'space-between',
            'margin': '5px'
        }

        # Card components
        cards = [
            dbc.Card(
                [
                    # html.H2(f"{30}", className="card-title",id='num-tags-text'),
                    html.Div(id='num-tags-text'),
                    html.P("Number of tags", className="card-text"),  # self.decrypted_multi_tag.get_tags_count()
                ],
                body=True,
                color="light",
                id='num-tags-card'
            ),
            dbc.Card(
                [
                    html.Div(id='data-points-text'),
                    html.P("Data points", className="card-text"),
                ],
                body=True,
                color="primary",  # dark
                inverse=True,
            ),

        ]

        # dropdowns components
        dropdowns = [
            [

                html.P("Tag ID"),
                html.Div(
                    id='tagid-dropdown-parent',
                    children=[
                        dcc.Dropdown(
                            id='tagid-dropdown',
                            options=[{'label': 'Wiliot', 'value': 'Wiliot'}]
                        )
                    ]
                )
            ],
            [

                html.P("Attribute"),
                html.Div(
                    id='attribute-dropdown-parent',
                    children=[
                        dcc.Dropdown(
                            id='attribute-dropdown',
                            options=[{'label': 'Wiliot', 'value': 'Wiliot'}]
                        )
                    ]
                )
            ],
        ]

        extra_options = [
            [
                html.Div(
                    [
                        'Live update',
                        daq.BooleanSwitch(id="live_update_switch", on=True),
                    ],
                    title='Live update graph',
                    style=h_style
                ),
                html.Div(id="live_update_text"),

                html.Div(
                    [
                        'Limit history',
                        daq.BooleanSwitch(id="history_switch", on=False),
                    ],
                    title='History',
                    style=h_style
                ),
                html.Div(id="history_switch_text"),

                html.Div(
                    [
                        html.P('Set to:', id='history-label', style={'display': 'block'}),
                        daq.NumericInput(
                            id='history-numeric',
                            value=50,
                            min=0,
                            max=10000,
                        ),
                    ],
                    title='History',
                    style=h_style
                ),
                html.Div(id="history-text"),

            ], [],
            [

                html.Div(
                    [
                        'Filter',
                        daq.BooleanSwitch(id="filter_switch", on=False),
                    ],
                    title='Filter kernel',
                    style=h_style
                ),
                html.Div(id="filter_switch_text"),
                html.Div(
                    [
                        'Kernel',
                        daq.NumericInput(
                            id='filter-kernel-numeric',
                            value=5,
                            min=0.0,
                            max=1000,
                        ),
                    ],
                    title='Filter kernel',
                    style=h_style
                ),
                html.Div(id="filter-kernel-text"),

            ], [],
            [
                html.Div(
                    [
                        'Show Threshold',
                        daq.BooleanSwitch(id="threshold_switch", on=False),
                    ],
                    title='Threshold',
                    style=h_style
                ),
                html.Div(id="threshold_switch_text"),

                html.Div(
                    [
                        'Set to:',
                        daq.NumericInput(
                            id='threshold-numeric',
                            value=5,
                            min=-1000,
                            max=10000,
                        ),
                    ],
                    title='Threshold',
                    style=h_style
                ),
                html.Div(id="threshold-text"),

            ],

        ]
        replay_options = [
            html.Div([
                daq.Slider(
                    id='replay-slider',
                    value=self.record_slider_value,
                    handleLabel={"showCurrentValue": True, "label": "VALUE"},
                    step=5
                ),
                html.Div(id='slider-result', style={"display": "none"})
            ], style={'display': 'block'}),
            html.Div(id="where", style={"display": "none"})
        ]
        # graph components
        graphs = [
            dcc.Graph("graph-v"),
            html.Div(dcc.Graph("graph-replay"), style={'display': 'block'})
        ]

        self.dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.dash_app.title = 'Wiliot Demo Portal'

        self.server = self.dash_app.server

        self.dash_app.layout = dbc.Container(
            [
                Header("Wiliot Demo Portal", self.dash_app),
                html.Hr(),
                dbc.Row([dbc.Col(card) for card in cards]),
                html.Br(),
                dbc.Row([dbc.Col(dropdown) for dropdown in dropdowns]),
                html.Br(),
                dbc.Row([dbc.Col(extra) for extra in extra_options]),
                html.Br(),
                dbc.Row([dbc.Col(replay) for replay in replay_options]),
                html.Br(),
                dbc.Col([dbc.Row(graph) for graph in graphs]),
                dcc.Interval(
                    id='interval-component',
                    interval=1 * 1000,  # in milliseconds
                    n_intervals=0),
                dcc.Interval(
                    id='interval-component-5sec',
                    interval=1 * 5000,  # in milliseconds
                    n_intervals=0),
                html.Footer('Copyright (c) 2019 Plotly')  # https://github.com/plotly/dash-sample-apps/blob/main/LICENSE
            ],
            fluid=False,
        )

        @self.dash_app.callback(output=Output('tagid-dropdown', 'options'),
                                inputs=[Input('tagid-dropdown-parent', 'n_clicks')])
        def change_my_tagid_dropdown_options(n_clicks):
            if n_clicks is None:
                raise dash.exceptions.PreventUpdate
            try:
                options = list(self.gw_instance.decrypted_multi_tag.tags.keys())
                if self.show_record:
                    for k in self.tags_record:
                        options.append(k)

                return [{"label": k, "value": k} for k in options]
            except Exception as e:
                print('Choose tag')
                raise PreventUpdate

        @self.dash_app.callback(
            [dash.dependencies.Output('attribute-dropdown', 'options'),
             Output(component_id='replay-slider', component_property='style'),
             Output(component_id='graph-replay', component_property='style')],
            [dash.dependencies.Input('tagid-dropdown', 'value')]
        )
        def update_attribute_dropdown(name):
            if name is None:
                raise PreventUpdate
            try:
                slider_style = {'display': 'none'}
                if self.show_record and name in self.tags_record.keys():
                    slider_style = {'display': 'block'}
                return [[{'label': i, 'value': i} for i in self.packet_attributes_list],
                        slider_style, slider_style]
            except Exception as e:
                print('Choose tag <')
                raise PreventUpdate

        @self.dash_app.callback(
            [Output("graph-v", "figure"), Output("graph-replay", "figure")],
            [Input("tagid-dropdown", "value"), Input("attribute-dropdown", "value"),
             Input('interval-component', 'n_intervals')],
        )
        def update_figures(tagid, attribute, n_intervals):
            if attribute is None:
                raise PreventUpdate
            if attribute == '' or not self.live_update:
                raise PreventUpdate
            try:
                if self.show_record and tagid in self.tags_record.keys():
                    tag_df = pd.read_csv(self.tags_record[tagid], low_memory=False)

                    tag_df = tag_df[:(tag_df.shape[0] // 100) * self.record_slider_value]
                else:
                    tag_df = self.gw_instance.decrypted_multi_tag.tags[tagid].get_df()

                x_axis_values_df = tag_df['time_from_start']
                x_axis_values_df_not_nan_mask = x_axis_values_df.notna()
                x_axis_values_df = x_axis_values_df[x_axis_values_df_not_nan_mask]
                x_axis_values = x_axis_values_df.to_list()
                y_axis_values = tag_df[attribute]
                y_axis_values = y_axis_values[x_axis_values_df_not_nan_mask]
                y_axis_values = y_axis_values.to_list()
                if self.filter_kernel < len(x_axis_values) and self.show_filter:
                    self.filter_kernel = int(self.filter_kernel)
                    y_values_not_nan_mask = tag_df[attribute].notna()
                    x_axis_values_df = x_axis_values_df[y_values_not_nan_mask]
                    y_axis_values = tag_df[attribute][y_values_not_nan_mask]
                    y_filtered_axis_values = y_axis_values.rolling(self.filter_kernel).median()
                    y_filtered_axis_values_nonan = y_filtered_axis_values[y_filtered_axis_values.notna()]
                if self.show_threshold:
                    y_threshold_axis_values = np.ones(np.size(x_axis_values)) * self.threshold_value
            except Exception as e:
                print('Attribute issue occurred')
                raise PreventUpdate

            try:
                attribute_figure = px.line(
                    title="{attribute}\t-\ttag id: {tagid}".format(attribute=attribute, tagid=tagid),
                    labels={"x": 'time[s]', "y": "{attribute}".format(attribute=attribute)}, )
                attribute_figure.add_scatter(
                    x=x_axis_values,
                    y=y_axis_values, line=dict(width=1, color="#0000FF"), marker=dict(size=5, color="#0000FF"),
                    mode='lines+markers', name='Measured value'
                )
            except Exception as e:
                raise PreventUpdate

            if self.show_threshold:
                try:
                    attribute_figure.add_scatter(x=x_axis_values,
                                                 y=y_threshold_axis_values, line=dict(width=3, color="#008000"),
                                                 mode='lines', name='Threshold value')
                except Exception as e:
                    print(e)

            if self.filter_kernel < len(x_axis_values) and self.show_filter:
                try:
                    attribute_figure.add_scatter(x=x_axis_values,
                                                 y=y_filtered_axis_values, line=dict(width=4, color="#FF0000"),
                                                 mode='lines', name='Filtered value')

                    attribute_figure.update_yaxes(range=[min(y_filtered_axis_values_nonan) - 0.1,
                                                         max(y_filtered_axis_values_nonan) + 0.1])
                except Exception as e:
                    print(e)

            if str(self.history_value).isnumeric():
                if self.history_value > 0 and self.limit_history:
                    try:
                        end_value = x_axis_values[-1]
                        start_value = end_value - self.history_value - 2
                        if start_value < 0:
                            start_value = 0

                        if self.filter_kernel < len(x_axis_values) and self.show_filter:
                            try:
                                y_filtered_axis_values_nonan_history = y_filtered_axis_values_nonan[
                                    x_axis_values_df > start_value]
                                attribute_figure.update_yaxes(range=[min(y_filtered_axis_values_nonan_history) - 0.1,
                                                                     max(y_filtered_axis_values_nonan_history) + 0.1])
                            except Exception as e:
                                print(e)

                        attribute_figure.update_xaxes(range=[start_value, end_value + 2])
                    except Exception as e:
                        print(e)

            temp_attribute_figure = attribute_figure
            if self.show_record and tagid in self.tags_record.keys():
                try:
                    attribute = 'curr_temperature_val'
                    x_axis_values_df = tag_df['time_from_start']
                    x_axis_values_df_not_nan_mask = x_axis_values_df.notna()
                    x_axis_values_df = x_axis_values_df[x_axis_values_df_not_nan_mask]
                    x_axis_values = x_axis_values_df.to_list()
                    y_axis_values = tag_df[attribute]
                    y_axis_values = y_axis_values[x_axis_values_df_not_nan_mask]
                    y_axis_values = y_axis_values.to_list()
                    if self.filter_kernel < len(x_axis_values) and self.show_filter:
                        self.filter_kernel = int(self.filter_kernel)
                        y_values_not_nan_mask = tag_df[attribute].notna()
                        x_axis_values_df = x_axis_values_df[y_values_not_nan_mask]
                        y_axis_values = tag_df[attribute][y_values_not_nan_mask]
                        y_filtered_axis_values = y_axis_values.rolling(self.filter_kernel).median()
                        y_filtered_axis_values_nonan = y_filtered_axis_values[y_filtered_axis_values.notna()]
                except Exception as e:
                    print('Attribute issue occurred')
                    raise PreventUpdate

                try:
                    temp_attribute_figure = px.line(
                        title="{attribute}\t-\ttag id: {tagid}".format(attribute=attribute, tagid=tagid),
                        labels={"x": 'time[s]', "y": "{attribute}".format(attribute=attribute)}, )

                    temp_attribute_figure.add_scatter(
                        x=x_axis_values,
                        y=y_axis_values, line=dict(width=1, color="#0000FF"), marker=dict(size=5, color="#0000FF"),
                        mode='lines+markers', name='Measured value'
                    )

                    if self.filter_kernel < len(x_axis_values) and self.show_filter:
                        try:
                            temp_attribute_figure.add_scatter(x=x_axis_values,
                                                              y=y_filtered_axis_values,
                                                              line=dict(width=4, color="#FF0000"),
                                                              mode='lines', name='Filtered value')

                            temp_attribute_figure.update_yaxes(range=[min(y_filtered_axis_values_nonan) - 0.1,
                                                                      max(y_filtered_axis_values_nonan) + 0.1])
                        except Exception as e:
                            print(e)

                except Exception as e:
                    raise PreventUpdate

            return [attribute_figure, temp_attribute_figure]

        @self.dash_app.callback(
            Output("where", "children"),
            Input("graph-v", "clickData"),
        )
        def click(clickData):
            if not clickData:
                raise dash.exceptions.PreventUpdate
            self.threshold_value = clickData["points"][0]['y']
            return self.threshold_value

        @self.dash_app.callback(Output('num-tags-text', 'children'),
                                Input('interval-component-5sec', 'n_intervals'))
        def update_metrics(n):
            try:
                num_of_tags = self.gw_instance.decrypted_multi_tag.get_tags_count()
                return html.H2('{num_of_tags}'.format(num_of_tags=num_of_tags), className="card-title")

            except Exception as e:
                raise PreventUpdate

        @self.dash_app.callback(Output('data-points-text', 'children'),
                                Input('interval-component-5sec', 'n_intervals'))
        def update_metrics(n):
            try:
                data_points = self.gw_instance.decrypted_multi_tag.get_packet_count()
                return html.H2('{data_points}'.format(data_points=data_points), className="card-title")
            except Exception as e:
                raise PreventUpdate

        @self.dash_app.callback(
            Output("filter-input-text", "children"),
            Input("filter-input", "value"),
        )
        def filter_input_render(value):
            if str(self.filter_kernel).isnumeric():
                self.filter_kernel = value
            return value

        @self.dash_app.callback(
            Output("threshold-input-text", "children"),
            Input("threshold-input", "value"),
        )
        def filter_input_render(value):
            if np.isreal(value):
                self.threshold_value = value
            return value

        @self.dash_app.callback(
            Output("history-input-text", "children"),
            Input("history-input", "value"),
        )
        def filter_input_render(value):
            self.history_value = value
            return value

        @self.dash_app.callback(
            Output("filter_switch_text", "children"),
            Input("filter_switch", "on"),
        )
        def update_filter_switch(on):
            self.show_filter = on

        @self.dash_app.callback(
            Output("live_update_text", "children"),
            Input("live_update_switch", "on"),
        )
        def update_filter_switch(on):
            self.live_update = on

        @self.dash_app.callback(
            Output("threshold_switch_text", "children"),
            Input("threshold_switch", "on"),
        )
        def update_threshold_switch(on):
            self.show_threshold = on

        @self.dash_app.callback(
            [Output(component_id='history-numeric', component_property='style'),
             Output(component_id='history-label', component_property='style')],
            Input("history_switch", "on"),
        )
        def update_threshold_switch(on):
            self.limit_history = on
            if self.limit_history:
                return [{'display': 'block'}, {'display': 'block'}]
            else:
                return [{'display': 'none'}, {'display': 'none'}]

        @self.dash_app.callback(
            Output("filter-kernel-text", "children"),
            Input("filter-kernel-numeric", "value"),
        )
        def update_filter_kernel(kernel):
            self.filter_kernel = kernel

        @self.dash_app.callback(
            Output("threshold-text", "children"),
            Input("threshold-numeric", "value"),
        )
        def update_threshold(threshold_value):
            self.threshold_value = threshold_value

        @self.dash_app.callback(
            Output("history-text", "children"),
            Input("history-numeric", "value"),
        )
        def update_history(history_value):
            self.history_value = history_value

        @self.dash_app.callback(
            Output("checklist-text", "children"),
            Input("all-checklist", "value"),
        )
        def sync_checklist(checklist_selected):
            if 'Live update' in checklist_selected:
                self.live_update = True
            else:
                self.live_update = False

            if 'Show filter' in checklist_selected:
                self.show_filter = True
            else:
                self.show_filter = False

            if 'Show threshold' in checklist_selected:
                # self.threshold_value = 3
                self.show_threshold = True
            else:
                self.show_threshold = False

            return 'checklist_selected'

        @self.dash_app.callback(
            Output("threshold-checklist-text", "children"),
            Input("threshold-checklist", "value"),
        )
        def sync_threshold_checklist(checklist_selected):
            if 'Show threshold' in checklist_selected:
                # self.threshold_value = 3
                self.show_threshold = True
            else:
                self.show_threshold = False

            return 'checklist_selected'

        @self.dash_app.callback(
            Output('slider-result', 'children'),
            Input('replay-slider', 'value')
        )
        def update_output(value):
            self.record_slider_value = value
            return f'The slider is currently at {value}.'

        live_plot_listener = threading.Thread(target=self.live_plot_task, args=())
        self.live_plot_thread = live_plot_listener.start()

    def live_plot_task(self):
        self.dash_app.run_server(dev_tools_hot_reload=False, debug=False)
        while True:
            time.sleep(1)
            if self.live_plots_event.is_set():
                break
        print('Live plotting has been stopped')
