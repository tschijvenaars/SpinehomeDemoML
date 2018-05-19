try:
    # Importing dash packets
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.dependencies import Input, Output, State
    # Importing plotly
    import plotly.graph_objs as go
except ImportError as e:
    print("The following error occurred: " + e.__str__())
    exit()


class Gui:
    """Graphical User Interface class

    This class contains all logic for making a graphical user interface with the Dash library.

    """
    app = ""
    controller = ""

    def __init__(self, controller):
        """GUI class constructor method

        :param controller: controller instance of class Controller

        """
        self.app = dash.Dash()
        self.controller = controller
        self.load_stylesheets()
        self.app.config.supress_callback_exceptions = True
        self.app.layout = self.get_overview()
        self.get_callbacks()

    def load_stylesheets(self):
        """Method for loading in style sheets

        The style sheets will be appended to the app variable of the GUI

        :return: None

        """
        external_css = ["https://codepen.io/Supermaniac101/pen/WJLNBV.css"]
        for css in external_css:
            self.app.css.append_css({"external_url": css})

    @staticmethod
    def get_overview():
        """Getter method for the main view

        :return: Overview variable containing the main view HTML

        """
        overview = html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content')
        ])
        return overview

    @staticmethod
    def get_menu():
        """Getter method for menu component

        :return: Menu component variable containing HTML

        """
        menu = html.Div([
            dcc.Link('Demo   ', href='/demo', className="orange"),
            dcc.Link('Pcap statistics   ', href='/statistics', className="blue")

        ], className="menu")
        return menu

    def get_demo(self):
        """Getter method for demo page

        :return: Demo page variable containing the main view HTML

        """
        demo_page = html.Div(children=[
                self.get_menu(),
                html.Br([]),
                html.Div([
                    html.H1(children='Machine Learning Demo')
                ]),
                html.H5(children='Informatie over het netwerk'),
                html.Div([  # Beginning of input page
                    html.Div([
                        html.Label('Type modem'),
                        dcc.Dropdown(
                            options=[
                                {'label': 'Technicolor TC7210', 'value': 'Technicolor TC7210'},
                                {'label': 'Technicolor TC7200', 'value': 'Technicolor TC7200'},
                                {'label': 'Connectbox (Compal CH7465LG)', 'value': 'Connectbox (Compal CH7465LG)'},
                                {'label': 'Connectbox (Arris TG2492LG)', 'value': 'Connectbox (Arris TG2492LG)'},
                                {'label': 'Cisco EPC3925', 'value': 'Cisco EPC3925'},
                                {'label': 'Cisco EPC3928', 'value': 'Cisco EPC3928'},
                                {'label': 'Cisco EPC3212', 'value': 'Cisco EPC3212'},
                                {'label': 'Mediabox XL (7401)', 'value': 'Mediabox XL (7401)'},
                                {'label': 'Mediabox XL (7400)', 'value': 'Mediabox XL (7400)'},
                                {'label': 'Samsung', 'value': 'Samsung'},
                                {'label': 'Ubee EVM3200', 'value': 'Ubee EVM3200'},
                                {'label': 'Ubee EVW321B', 'value': 'Ubee EVW321B'},
                                {'label': 'Ubee EVW3226', 'value': 'Ubee EVW3226'},
                                {'label': 'UBC1318ZG', 'value': 'UBC1318ZG'},
                                {'label': 'Cisco EPC3928AD', 'value': 'Cisco EPC3928AD'},
                                {'label': 'Hitron CGNV4', 'value': 'Hitron CGNV4'},
                                {'label': 'Thomson TWG870', 'value': 'Thomson TWG870'},
                                {'label': 'Linksys EA6900V1.1', 'value': 'Linksys EA6900V1.1'}
                            ],
                            multi=False, id='modem-type', value=''
                        )], style={'display': 'inline-block', 'width': '100%'}),
                    html.Div([
                        html.Label('Extra router used?'),
                        dcc.Dropdown(
                            options=[
                                {'label': 'Yes', 'value': 'Ja'},
                                {'label': 'No', 'value': 'Nee'}
                            ],
                            multi=False, id='has-router', value=''
                        )], style={'display': 'inline-block', 'width': '100%'}),
                    html.Div([
                        html.Label('Type router'),
                        dcc.Input(id='router-type', type='text', value='')
                    ], style={'display': 'inline-block', 'width': '100%'}),
                    html.Div([
                        html.Label('Router firmware versie'),
                        dcc.Input(id='router-firmware', type='text', value='')
                    ], style={'display': 'inline-block', 'width': '100%'}),
                    html.Div([
                        html.Label('Abonnement uploadsnelheid'),
                        dcc.Dropdown(
                            options=[
                                {'label': '200 Mbit/s down - 20 Mbit/s up', 'value': '200 Mbit/s down - 20 Mbit/s up'},
                                {'label': '250 Mbit/s down - 25 Mbit/s up', 'value': '250 Mbit/s down - 25 Mbit/s up'},
                                {'label': '300 Mbit/s down - 30 Mbit/s up', 'value': '300 Mbit/s down - 30 Mbit/s up'},
                                {'label': '500 Mbit/s down - 50 Mbit/s up', 'value': '500 Mbit/s down - 50 Mbit/s up'},
                                {'label': '400 Mbit/s down - 40 Mbit/s up', 'value': '400 Mbit/s down - 40 Mbit/s up'},
                                {'label': '40 Mbit/s down - 4 Mbit/s up', 'value': '40 Mbit/s down - 4 Mbit/s up'},
                                {'label': '100 Mbit/s down - 10 Mbit/s up', 'value': '100 Mbit/s down - 10 Mbit/s up'},
                                {'label': '250 Mbit/s down / 35 Mbit/s up', 'value': '250 Mbit/s down / 35 Mbit/s up'},
                                {'label': '500 Mbit/s down - 40 Mbit/s up', 'value': '500 Mbit/s down - 40 Mbit/s up'},
                                {'label': '50 Mbit/s down - 5 Mbit/s up', 'value': '50 Mbit/s down - 5 Mbit/s up'},
                                {'label': '250 Mbit/s down - 40 Mbit/s up', 'value': '250 Mbit/s down - 40 Mbit/s up'}
                            ],
                            multi=False, id='subscription', value=''
                        )], style={'display': 'inline-block', 'width': '100%'}),
                    html.Div([
                        html.Label('Speedtest uploadsnelheid'),
                        dcc.Input(id='test-upload', type='number', value='')
                    ], style={'display': 'inline-block', 'width': '100%'}),
                    html.Div([
                        html.Label('Speedtest downloadsnelheid'),
                        dcc.Input(id='test-download', type='number', value='')
                    ], style={'display': 'inline-block', 'width': '100%'}),
                    html.Div([
                        html.Label('Ping (Speedtest)'),
                        dcc.Input(id='test-ping', type='number', value='')
                    ], style={'display': 'inline-block', 'width': '100%'}),
                    html.Div([
                        html.Label('Processor'),
                        dcc.Input(id='processor-type', type='text', value=''),
                    ], style={'display': 'inline-block', 'width': '100%'}),
                    html.Div([
                        html.Label('Netwerkkaart'),
                        dcc.Input(id='networkcard-type', type='text', value='')
                    ], style={'display': 'inline-block', 'width': '100%'}),
                    html.Div([
                        html.Label('PCI network card?'),
                        dcc.Dropdown(
                            options=[
                                {'label': 'Yes', 'value': 'Ja'},
                                {'label': 'No', 'value': 'Nee'}
                            ],
                            multi=False, id='has-pcicard', value=''
                        )
                    ], style={'display': 'inline-block', 'width': '100%'}),
                    html.Div([
                        html.Label('Soort verbinding'),
                        dcc.Dropdown(
                            options=[
                                {'label': 'Ethernet', 'value': 'Netwerkkabel'},
                                {'label': 'Wi-Fi 2.4 GHz', 'value': 'Wifi via 2,4 GHz frequentieband'},
                                {'label': 'Wi-Fi 5 GHz', 'value': 'Wifi via 5,0 GHz frequentieband'}
                            ],
                            multi=False, id='connection', value='ethernet'
                        )
                    ], style={'display': 'inline-block', 'width': '100%'}),
                    html.Div([
                        html.Label('Activiteit op de computer'),
                        dcc.Dropdown(
                            options=[
                                {'label': 'Downloading/Torrenting', 'value': 'Downloaden'},
                                {'label': 'Gamen', 'value': 'Gamen'},
                                {'label': 'Entertainment (Youtube, Netflix)', 'value': '(video)streamen'},
                                {'label': 'Surfen (websites bezoeken)', 'value': 'Surfen (websites bezoeken)'},
                                {'label': 'Downloaden', 'value': 'Downloaden'}
                            ],
                            multi=False, id='activity', value='download'
                        )
                    ], style={'display': 'inline-block', 'width': '100%'})
                ], style={'display': 'inline-block', 'columnCount': 3}),
                html.Div([
                    html.Br(),
                    html.Button('Calculate Probability', className="button-primary", id='calculateButton'),
                    html.Br()
                ]),
                html.Div([
                    html.H2(children='Output:'),
                    html.Div(id='model-output')
                ])
        ])
        return demo_page

    @staticmethod
    def get_statistics_inner(packets):
        """Getter method for statistics page information inner component

        This page is the inner page containing all the information of the pcap analytics page.

        :param packets: Packets variable as StatsInstance class
        :return: Statistical information component variable containing HTML and graphs about the pcap-file

        """
        statistics_div = html.Div([
            html.Div([
                html.H4(["Packet information"]),
                html.P(["Packet name: " + str(packets.filename)]),
                html.P(["Total time of the capture: " + str(round(packets.total_time, 2)) + " seconds"]),
                html.P(["Amount of TCP packets: " + str(packets.tcp_count)]),
                html.P(["Amount of UDP packets: " + str(packets.udp_count)]),
                html.P(["Amount of DNS packets: " + str(packets.dns_count)]),
                html.P(["Amount of ICMP packets: " + str(packets.icmp_count)]),
                html.Br([])
            ]),
            html.Div([
                html.H4(["Statistics graphs"]),
                dcc.Graph(
                    figure=go.Figure(
                        data=[
                            go.Histogram(
                                x=list(packets.dst_addresses),
                                name='Destination Addresses',
                                marker=go.Marker(
                                    color='rgb(66, 10, 99)'
                                ),
                                opacity=0.75
                            ),
                            go.Histogram(
                                x=list(packets.src_addresses),
                                name='Source Addresses',
                                marker=go.Marker(
                                    color='rgb(10, 99, 66)'
                                ),
                                opacity=0.75
                            )
                        ],
                        layout=go.Layout(
                            title='Histogram of source and destination addresses',
                            showlegend=True,
                            legend=go.Legend(
                                x=0,
                                y=1.0
                            ),
                            xaxis=dict(
                                title='Value'
                            ),
                            yaxis=dict(
                                title='IP address'
                            ),
                            bargap=0.2,
                            bargroupgap=0.1
                        )
                    ),
                    style={'height': 400},
                    id='histogramDst'
                ),
                dcc.Graph(
                    figure=go.Figure(
                        data=[
                            go.Scatter(
                                x=list(packets.time_list),
                                y=list(packets.sent_bytes),
                                name='Bytes of data sent over time',
                                marker=go.Marker(
                                    color='rgb(55, 83, 109)'
                                )
                            )
                        ],
                        layout=go.Layout(
                            title='Bytes',
                            showlegend=True,
                            legend=go.Legend(
                                x=0,
                                y=1.0
                            ),
                            xaxis=dict(
                                title='Time (s)'
                            ),
                            yaxis=dict(
                                title='Size (bytes)'
                            ),
                        )
                    ),
                    style={'height': 400},
                    id='bytesPlot'
                )
            ])
        ])
        return statistics_div

    def get_statistics(self):
        """Getter method for statistics page without any information

        This page is the wapper page of the pcap analytics page.

        :param self: Self instance of GUI
        :return: Statistics page variable containing HTML

        """
        statistics = html.Div([  # 404
            # self.get_logo(),
            self.get_menu(),
            html.Div([
                html.Br([]),
                html.H1(children='Network Traffic Statistics')
            ]),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '50%%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=False
            ),
            html.Div(id='output-data-upload')
            ], className="stats-page")
        return statistics

    def get_error(self):
        """Getter method for error page

        This page is shown when the page is wrong or not found.

        :param self: Self instance of GUI
        :return: Error page variable containing HTML

        """
        error = html.Div([  # 404
            html.Br([]),
            self.get_menu(),
            html.P(["404 Page not found"])
            ], className="no-page")
        return error

    def get_callbacks(self):
        """Getter method of all callback functions

        This page contains all interactive callback functions of all pages

        :return: Nothing

        """
        # Callback to Machine Learning (DEMO)
        @self.app.callback(
            Output('model-output', 'children'),
            [Input('calculateButton', 'n_clicks')],
            state=[
                State('modem-type', 'value'),
                State('has-router', 'value'),
                State('router-type', 'value'),
                State('router-firmware', 'value'),
                State('subscription', 'value'),
                State('test-upload', 'value'),
                State('test-download', 'value'),
                State('test-ping', 'value'),
                State('processor-type', 'value'),
                State('networkcard-type', 'value'),
                State('has-pcicard', 'value'),
                State('connection', 'value'),
                State('activity', 'value')
            ])
        def update_output(n_clicks, modem_type, has_router, router_type, router_firmware,
                          subscription, test_upload, test_download, test_ping, processor_type,
                          network_card, has_pcicard, connection, activity):
            self.controller.create_unseen_instance(
                modem_type, has_router, router_type, router_firmware,
                subscription, test_upload, test_download, test_ping, processor_type,
                network_card, has_pcicard, connection, activity
            )
            if self.controller.unseen_instance.is_empty():
                return "Lege velden ontdekt!"
            else:
                try:
                    self.controller.create_encoded_instance()
                except ValueError:
                    return "Inserted inputs are unknown to the models."
                kmodes_pred = self.controller.get_kmodes_prediction()
                kmeans_pred = self.controller.get_kmeans_prediction()
                nb_pred = self.controller.get_bayes_prediction()
                rf_pred = self.controller.get_rf_prediction()
                acc_nb = self.controller.get_bayes_accuracy()
                acc_rf = self.controller.get_rf_accuracy()
                output = html.Div([
                    html.P(["Unseen instance assigned to kmodes cluster: " + str(kmodes_pred)]),
                    html.P(["Unseen instance assigned to kmeans cluster: " + str(kmeans_pred)]),
                    html.P(["Advice from Naive Bayes Algorithm: " + str(str(nb_pred))]),
                    html.P(["Advice from Random Forest Algorithm: " + str(str(rf_pred))]),
                    html.P(["Accuracy of Naive Bayes Model: " + str(round(acc_nb, 2)) + "%"]),
                    html.P(["Accuracy of Random Forest Model: " + str(round(acc_rf, 2)) + "%"]),
                ])
                return output

        # Callback for page update
        @self.app.callback(dash.dependencies.Output('page-content', 'children'),
                           [dash.dependencies.Input('url', 'pathname')])
        def display_page(pathname):
            if pathname == '/' or pathname == '/demo':
                return self.get_demo()
            elif pathname == '/statistics':
                return self.get_statistics()
            else:
                return self.get_error()

        # Callback for statistics page (PCAP)
        @self.app.callback(Output('output-data-upload', 'children'),
                           [Input('upload-data', 'filename')])
        def update_output(filename):
            if filename is None or "":
                return "Select a file"
            else:
                if 'pcap' in filename:
                    try:
                        packets = self.controller.parse_filename(filename)
                        return self.get_statistics_inner(packets)
                    except Exception as ex:
                        return 'Something went wrong with loading in the file: ' + ex.__str__()
                else:
                    return 'Wrong type of file'
