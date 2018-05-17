class StatsInstance:
    """Statistics Instance class

    This class contains all information about pcap-files, which will be calculated by the controller and
    passed to the GUI. The GUI will use this instance to visualise statistical data about the pcap-file.

    """
    tcp_count = 0
    udp_count = 0
    dns_count = 0
    icmp_count = 0
    src_addresses = []
    dst_addresses = []
    unique_source = []
    unique_dest = []
    sent_bytes = []
    time_list = []
    protocols_used = []
    total_time = 0
    throughput_time = []
    filename = ""

    def __init__(self, tcp, udp, dns, icmp, src, dst, un_src, un_dest, sent_bytes, time_list, proto, totime,
                 filename):
        """Constructor method for making a statistics class instance

        :param tcp: Amount of TCP packets as integer
        :param udp: Amount of UDP packets as integer
        :param dns: Amount of DNS packets as integer
        :param icmp: Amount of ICMP packets as integer
        :param src: List of source IP addresses
        :param dst: List of destination IP addresses
        :param un_src: List of unique source IP addresses
        :param un_dest: List of unique destination IP addresses
        :param sent_bytes: List of packet sizes sent
        :param time_list: List of the time packets are sent in seconds
        :param proto: List of protocols used
        :param totime: Integer of total session time
        :param filename: Filename of selected file

        """
        self.tcp_count = tcp
        self.udp_count = udp
        self.dns_count = dns
        self.icmp_count = icmp
        self.src_addresses = src
        self.dst_addresses = dst
        self.unique_source = un_src
        self.unique_dest = un_dest
        self.sent_bytes = sent_bytes
        self.time_list = time_list
        self.protocols_used = proto
        self.total_time = totime
        self.filename = filename
