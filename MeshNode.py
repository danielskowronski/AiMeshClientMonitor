import re

from RouterInfo import RouterInfo
from ClientInfo import ClientInfo

from pprint import pprint


class MeshNode:
    def __init__(self, ip, user, password):
        self.ri = RouterInfo(ip, user, password)
        self.wl_log = self.ri.get_wl_log()
        self.clients = {}

        splitter = "----------------------------------------"
        station_list_header = "idx MAC               Associated Authorized   RSSI PHY PSM SGI STBC MUBF NSS   BW Tx rate Rx rate Connect Time"

        if not splitter in self.wl_log:
            return

        wl_log_sections = self.wl_log.split(splitter)
        for wl_log_section in wl_log_sections:
            if station_list_header in wl_log_section:
                possible_station_lines = wl_log_section.split("\n")
                for possible_station_line in possible_station_lines:
                    # TODO: make it smarter
                    match_mac = re.search(
                        r"[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]", possible_station_line)
                    if match_mac:
                        try:
                            client = ClientInfo(possible_station_line)
                            self.clients[client.get_mac()] = client
                        except Exception:
                            pass

    def get_wl_log(self):
        return self.wl_log

    def get_clients(self):
        return self.clients
