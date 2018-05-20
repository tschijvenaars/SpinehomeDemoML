try:
    from view import gui as gui
    from model import unseenInstance
    from model import statsModel
    # Import of Helper libraries
    import os
    import pandas as pd
    import numpy as np
    # Import Scapy libraries
    from scapy.layers.dns import DNS
    from scapy.layers.inet import IP, ICMP, UDP, TCP, Ether
    from scapy.all import *
    # Import Library of KModes clustering
    from kmodes.kmodes import KModes
    # Import Library of KMeans clustering
    from sklearn.cluster import KMeans
    # Import Library of Gaussian Naive Bayes classification
    from sklearn.naive_bayes import GaussianNB
    # Import Library of Random Forest classification
    from sklearn.ensemble import RandomForestClassifier
    # Import Sklearn Helper libraries
    from sklearn.metrics import accuracy_score
    from sklearn.metrics import confusion_matrix
    from sklearn import preprocessing
    from sklearn.model_selection import train_test_split
except ImportError as e:
    print("Libraries are not installed: " + e.__str__())
    exit()


class Controller:
    """Controller class

    The controller class should be initialized in the main to start the program. The controller class controls
    everything: The GUI, the models and everything between them.

    """
    gui = ""
    unseen_instance = ""
    encoded_instance = ""
    ul_dataset = ""
    sl_dataset = ""
    # Machine learning algorithms
    kmodes = KModes(n_clusters=5, init='Huang', n_init=5, verbose=1)
    nb_model = GaussianNB()
    rf_model = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=12356)
    kmeans = KMeans(n_clusters=5, random_state=0)
    # All encoders
    advice_encoder = preprocessing.LabelEncoder()
    activities_encoder = preprocessing.LabelEncoder()
    has_router_encoder = preprocessing.LabelEncoder()
    modem_type_encoder = preprocessing.LabelEncoder()
    router_type_encoder = preprocessing.LabelEncoder()
    router_firmware_encoder = preprocessing.LabelEncoder()
    subscription_encoder = preprocessing.LabelEncoder()
    connection_encoder = preprocessing.LabelEncoder()
    network_card_encoder = preprocessing.LabelEncoder()
    has_external_encoder = preprocessing.LabelEncoder()
    processor_encoder = preprocessing.LabelEncoder()
    # Training datasets (values and labels)
    train_values = []
    train_labels = []
    # Test datasets (values and labels)
    test_values = []
    test_labels = []

    def __init__(self):
        """Init method

        Making a new GUI instance, preparing data for machine learning and starting the app server.

        """
        self.gui = gui.Gui(self)
        self.make_unsupervised_set()
        self.make_supervised_set()
        self.create_datasets()
        self.train_kmodes()
        self.train_kmeans()
        self.train_bayes()
        self.train_random_forest()
        self.get_bayes_confmatrix()
        self.get_rf_confmatrix()
        self.gui.app.run_server(debug=True)

    def create_unseen_instance(self, modem_type, has_router, router_type, router_firmware,
                               subscription, test_upload, test_download, test_ping, processor_type,
                               network_card, has_pcicard, connection, activity):
        """Method for creating an unseen instance object

        :param modem_type: Modem type input as string
        :param has_router: Has router input as string
        :param router_type: Router type input as string
        :param router_firmware: Router firmware input as string
        :param subscription: Subscription plan input as string
        :param test_upload: Speedtest upload speed in MB/s input as int
        :param test_download: Speedtest download speed in MB/s input as int
        :param test_ping: Speedtest ping speed in ms input as int
        :param processor_type: Processor type input as string
        :param network_card: Network card type input as string
        :param has_pcicard: Has PCI network card input as string
        :param connection: Connection type input as string
        :param activity: Activities input as string
        :return: None

        """
        self.unseen_instance = unseenInstance.UnseenInstance(modem_type, has_router, router_type, router_firmware,
                                                             subscription, test_upload, test_download, test_ping,
                                                             processor_type, network_card, has_pcicard,
                                                             connection, activity)

    # noinspection PyBroadException
    def parse_filename(self, filename):
        """Method for loading pcap-file

        :param filename: Name of the chosen pcap-file
        :return: Statistics Model instance

        """
        try:
            location = os.getcwd()
            packets = rdpcap(location + '/res/' + filename)
            return self.make_statistics(packets, filename)
        except Exception:
            return 'An error occurred while uploading'

    @staticmethod
    def make_statistics(packets, filename):
        """Method for loading pcap-file, calculating statistical
        values and making statistics model instance

        :param filename: Filename of the loaded pcap file
        :param packets: Loaded pcap file instance
        :return: Statistical Model instance

        """
        # Make packet counts
        tcp_count = packets[TCP].__len__()
        udp_count = packets[UDP].__len__()
        dns_count = packets[DNS].__len__()
        icmp_count = packets[ICMP].__len__()
        # Make address lists
        source_addresses = list(p[IP].src for p in packets if IP in p)
        destination_addresses = list(p[IP].dst for p in packets if IP in p)
        # Calculate protocols used
        protocols_used = list(p[IP].get_field('proto').i2s[p.proto] for p in packets if IP in p)
        # Make unique address lists
        unique_source_addresses = set(source_addresses)
        unique_destination_addresses = set(destination_addresses)
        # Calculate total session time
        total_time = packets[packets.__len__()-1].time - packets[0].time
        # Make empty variables
        total_throughput = 0
        sent_bytes = []
        time_list = []
        # For-loop for calculating values
        for pkt in packets:
            if Ether in pkt:
                time_list.append(pkt[Ether].time - packets[0].time)
                sent_bytes.append(total_throughput)
                total_throughput += pkt[Ether].wirelen
        stats_model = statsModel.StatsInstance(tcp_count, udp_count, dns_count, icmp_count,
                                               source_addresses, destination_addresses,
                                               unique_source_addresses, unique_destination_addresses,
                                               sent_bytes, time_list, protocols_used, total_time, filename)
        return stats_model

    def make_unsupervised_set(self):
        """Method for preparing unsupervised learning dataset

        :return: None

        """
        self.ul_dataset = pd.read_csv(os.getcwd() + '/res/finaladvice.csv', sep=',')
        self.ul_dataset = self.ul_dataset.drop('Advice', 1)
        self.ul_dataset["ModemType"] = self.ul_dataset["ModemType"].astype('category')
        self.ul_dataset["HasRouter"] = self.ul_dataset["HasRouter"].astype('category')
        self.ul_dataset["RouterType"] = self.ul_dataset["RouterType"].astype('category')
        self.ul_dataset["Subscription"] = self.ul_dataset["Subscription"].astype('category')
        self.ul_dataset["ConnectionType"] = self.ul_dataset["ConnectionType"].astype('category')
        self.ul_dataset["NetworkCard"] = self.ul_dataset["NetworkCard"].astype('category')
        self.ul_dataset["ExternalNIC"] = self.ul_dataset["ExternalNIC"].astype('category')
        self.ul_dataset["Processor"] = self.ul_dataset["Processor"].astype('category')
        self.ul_dataset["Activities"] = self.ul_dataset["Activities"].astype('category')
        self.ul_dataset["RouterSoftware"] = self.ul_dataset["RouterSoftware"].astype('category')

    def make_supervised_set(self):
        """Method for preparing supervised learning dataset

        :return: None

        """
        self.sl_dataset = pd.read_csv(os.getcwd() + '/res/finaladvice.csv', sep=',')
        self.sl_dataset["ModemType"] = self.sl_dataset["ModemType"].astype('category')
        self.sl_dataset["HasRouter"] = self.sl_dataset["HasRouter"].astype('category')
        self.sl_dataset["RouterType"] = self.sl_dataset["RouterType"].astype('category')
        self.sl_dataset["Subscription"] = self.sl_dataset["Subscription"].astype('category')
        self.sl_dataset["ConnectionType"] = self.sl_dataset["ConnectionType"].astype('category')
        self.sl_dataset["NetworkCard"] = self.sl_dataset["NetworkCard"].astype('category')
        self.sl_dataset["ExternalNIC"] = self.sl_dataset["ExternalNIC"].astype('category')
        self.sl_dataset["Processor"] = self.sl_dataset["Processor"].astype('category')
        self.sl_dataset["Activities"] = self.sl_dataset["Activities"].astype('category')
        self.sl_dataset["RouterSoftware"] = self.sl_dataset["RouterSoftware"].astype('category')
        self.sl_dataset["Advice"] = self.sl_dataset["Advice"].astype('category')

    def get_kmodes_prediction(self):
        """Method for predicting cluster of the unseen instance

        :return: Predicted cluster for unseen instance

        """
        prediction = self.kmodes.predict(self.unseen_instance.get_array().reshape(1, -1))[0]
        return prediction

    def get_bayes_prediction(self):
        """Method for predicting advice label for the unseen instance using Naive Bayes (Gaussian)

        :return: Predicted label for unseen instance

        """
        prediction = self.nb_model.predict(self.encoded_instance.get_encoded_array().reshape(1, -1))
        if prediction.size > 0:
            return self.advice_encoder.inverse_transform(prediction[0])
        else:
            return "Error"

    def get_rf_prediction(self):
        """Method for predicting advice label for the unseen instance using Random Forest trees

        :return: Predicted label for unseen instance

        """
        prediction = self.rf_model.predict(self.encoded_instance.get_encoded_array().reshape(1, -1))
        if prediction.size > 0:
            return self.advice_encoder.inverse_transform(prediction[0])
        else:
            return "Error"

    def get_kmeans_prediction(self):
        """Method for predicting kmeans cluster of the unseen instance

        :return: Predicted kmeans cluster for unseen instance

        """
        prediction = self.kmeans.predict(self.unseen_instance.get_array().reshape(1, -1))[0]
        return prediction

    def train_kmodes(self):
        """Method for training kmodes (clustering) model

        :return: None

        """
        self.kmodes.fit(self.ul_dataset)

    def train_bayes(self):
        """Method for training Naive Bayes (Gaussian) model

        :return: None

        """
        self.nb_model.fit(self.train_values, self.train_labels)

    def train_random_forest(self):
        """Method for training Random Forest trees model

        :return: None

        """
        self.rf_model.fit(self.train_values, self.train_labels)

    def train_kmeans(self):
        """Method for training kmeans (clustering) model

        :return: None

        """
        self.kmeans.fit(self.train_values)

    def get_bayes_accuracy(self):
        """Method for getting the accuracy of the Naive Bayes model using accuracy score and test dataset

        :return: Accuracy of the model as float

        """
        ph = self.nb_model.predict(self.test_values)
        return accuracy_score(self.test_labels, ph)

    def get_rf_accuracy(self):
        """Method for getting the accuracy of the Random Forest model using accuracy score and test dataset

        :return: Accuracy of model as float

        """
        ph = self.rf_model.predict(self.test_values)
        return accuracy_score(self.test_labels, ph)

    def get_bayes_confmatrix(self):
        """Method for calculating the confusion matrix of the Naive Bayes model

        :return: Prints confusion matrix of Naive Bayes model

        """
        ph = self.nb_model.predict(self.test_values)
        print(pd.crosstab(self.test_labels, ph, rownames=['True'], colnames=['Predicted'], margins=True))

    def get_rf_confmatrix(self):
        """Method for calculating the confusion matrix of the Random Forests model

        :return: Prints confusion matrix of Random Forests model

        """
        ph = self.rf_model.predict(self.test_values)
        print(pd.crosstab(self.test_labels, ph, rownames=['True'], colnames=['Predicted'], margins=True))

    def create_datasets(self):
        """Method for creating test datasets and training datasets

        :return: None

        """
        ph = self.sl_dataset.drop('Advice', axis=1)
        self.activities_encoder.fit(ph['Activities'])
        ph['Activities'] = self.activities_encoder.transform(ph['Activities'])
        self.has_router_encoder.fit(ph['HasRouter'])
        ph['HasRouter'] = self.has_router_encoder.transform(ph['HasRouter'])
        self.modem_type_encoder.fit(ph['ModemType'])
        ph['ModemType'] = self.modem_type_encoder.transform(ph['ModemType'])
        self.router_type_encoder.fit(ph['RouterType'])
        ph['RouterType'] = self.router_type_encoder.transform(ph['RouterType'])
        self.subscription_encoder.fit(ph['Subscription'])
        ph['Subscription'] = self.subscription_encoder.transform(ph['Subscription'])
        self.connection_encoder.fit(ph['ConnectionType'])
        ph['ConnectionType'] = self.connection_encoder.transform(ph['ConnectionType'])
        self.network_card_encoder.fit(ph['NetworkCard'])
        ph['NetworkCard'] = self.network_card_encoder.transform(ph['NetworkCard'])
        self.has_external_encoder.fit(ph['ExternalNIC'])
        ph['ExternalNIC'] = self.has_external_encoder.transform(ph['ExternalNIC'])
        self.processor_encoder.fit(ph['Processor'])
        ph['Processor'] = self.processor_encoder.transform(ph['Processor'])
        self.router_firmware_encoder.fit(ph['RouterSoftware'])
        ph['RouterSoftware'] = self.router_firmware_encoder.transform(ph['RouterSoftware'])
        x = ph
        ph = self.sl_dataset[['Advice']]
        self.advice_encoder.fit(ph['Advice'])
        ph = self.advice_encoder.transform(ph['Advice'])
        y = ph
        self.train_values, self.test_values, self.train_labels, self.test_labels = train_test_split(x, y, test_size=0.3,
                                                            stratify=y, random_state=123456)

    def create_encoded_instance(self):
        """Method for encoding unseen instance for use in prediction model

        :return: None

        """
        self.encoded_instance = self.unseen_instance
        self.encoded_instance.activity = self.activities_encoder.transform(
            np.array([self.encoded_instance.activity])
        )[0]
        self.encoded_instance.has_router = self.has_router_encoder.transform(
            np.array([self.encoded_instance.has_router])
        )[0]
        self.encoded_instance.modem_type = self.modem_type_encoder.transform(
            np.array([self.encoded_instance.modem_type])
        )[0]
        self.encoded_instance.router_type = self.router_type_encoder.transform(
            np.array([self.encoded_instance.router_type])
        )[0]
        self.encoded_instance.subscription = self.subscription_encoder.transform(
            np.array([self.encoded_instance.subscription])
        )[0]
        self.encoded_instance.connection = self.connection_encoder.transform(
            np.array([self.encoded_instance.connection])
        )[0]
        self.encoded_instance.network_card = self.network_card_encoder.transform(
            np.array([self.encoded_instance.network_card])
        )[0]
        self.encoded_instance.has_pcicard = self.has_external_encoder.transform(
            np.array([self.encoded_instance.has_pcicard])
        )[0]
        self.encoded_instance.processor_type = self.processor_encoder.transform(
            np.array([self.encoded_instance.processor_type])
        )[0]
        self.encoded_instance.router_firmware = self.router_firmware_encoder.transform(
            np.array([self.encoded_instance.router_firmware])
        )[0]
