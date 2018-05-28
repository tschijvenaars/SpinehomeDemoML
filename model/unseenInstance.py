try:
    import numpy as np
except ImportError:
    print("Pandas/Numpy is not installed")
    exit()


class UnseenInstance:
    """Unseen instance class

    This class is used to create a single instance which represents the values received from a system.
    The values in this instance correspond with the values of the columns in the data set used
    in the machine learning value.

    """
    modem_type = ""
    has_router = ""
    router_type = ""
    router_firmware = ""
    subscription = ""
    test_upload = 9999
    test_download = 9999
    test_ping = 9999
    processor_type = ""
    network_card = ""
    has_pcicard = ""
    connection = ""
    activity = ""

    def __init__(self, modem_type, has_router, router_type, router_firmware,
                 subscription, test_upload, test_download, test_ping, processor_type,
                 network_card, has_pcicard, connection, activity):
        """Constructor method for unseen instance class

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

        """
        self.modem_type = modem_type
        self.has_router = has_router
        self.router_type = router_type
        self.router_firmware = router_firmware
        self.subscription = subscription
        self.test_upload = test_upload
        self.test_download = test_download
        self.test_ping = test_ping
        self.processor_type = processor_type
        self.network_card = network_card
        self.has_pcicard = has_pcicard
        self.connection = connection
        self.activity = activity

    def to_string(self):
        """ToString method to turn the instance to text for testing purposes

        :return: String of all values of the unseen instance

        """
        return 'The inputs are: {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {} and {}'.format(
            self.modem_type, self.has_router, self.router_type, self.router_firmware,
            self.subscription, self.test_upload, self.test_download, self.test_ping,
            self.processor_type, self.network_card, self.has_pcicard, self.connection, self.activity
        )

    def get_array(self):
        """ Method for returning array of all variables to use in kmodes prediction

        :return: Returns numpy array of all values of this Unseen Instance

        """
        ph = np.array([self.modem_type,
                       self.has_router,
                       self.router_type,
                       self.router_firmware,
                       self.subscription,
                       self.test_ping,
                       self.test_upload,
                       self.test_download,
                       self.connection,
                       self.network_card,
                       self.has_pcicard,
                       self.processor_type,
                       self.activity])
        return ph

    def get_encoded_array(self):
        """ Method for returning encoded array of all variables. ONLY use for machine learning predictions!

        :return: Returns numpy array of int variables

        """
        try:
            ph = np.array([int(self.modem_type),
                           int(self.has_router),
                           int(self.router_type),
                           int(self.router_firmware),
                           int(self.subscription),
                           int(self.test_ping),
                           int(self.test_upload),
                           int(self.test_download),
                           int(self.connection),
                           int(self.network_card),
                           int(self.has_pcicard),
                           int(self.processor_type),
                           int(self.activity)])
            return ph
        except ValueError:
            return np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    def is_empty(self):
        """Helper method to check if values are empty or not. Use for error checking

        :return: Boolean if any necessary value is missing

        """
        if self.modem_type == "" or None:
            return True
        if self.has_router == "" or None:
            return True
        if self.router_type == "" or None:
            return True
        if self.router_firmware == "" or None:
            return True
        if self.subscription == 9999 or None:
            return True
        if self.test_upload == 9999 or None:
            return True
        if self.test_download == 9999 or None:
            return True
        if self.test_ping == 9999 or None:
            return True
        if self.processor_type == "" or None:
            return True
        if self.network_card == "" or None:
            return True
        if self.has_pcicard == "" or None:
            return True
        if self.connection == "" or None:
            return True
        if self.activity == "" or None:
            return True
        return False
