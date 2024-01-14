import ipaddress

from pprint import pprint


class ClientInfo:
    def __init__(self, raw_ap_line):
        # can't use raw_ap_line.split() as some fields are empty
        if len(raw_ap_line) != 110:
            raise Exception("uknown format!")

        self.mac = raw_ap_line[4: 21].strip()
        self.assoc = raw_ap_line[22: 25].strip()
        self.auth = raw_ap_line[33: 36].strip()
        self.rssi = raw_ap_line[43: 50].strip()
        self.phy = raw_ap_line[51: 54].strip()
        self.psm = raw_ap_line[55: 58].strip()
        self.sgi = raw_ap_line[59: 62].strip()
        self.stbc = raw_ap_line[63: 66].strip()
        self.mubf = raw_ap_line[68: 71].strip()
        self.nss = raw_ap_line[73: 76].strip()
        self.bw = raw_ap_line[77: 81].strip()
        self.tx = raw_ap_line[82: 89].strip()
        self.rx = raw_ap_line[90: 97].strip()
        self.time = raw_ap_line[98:110].strip()

        self.name = self.mac
        self.vendor = "N/A"
        self.ip = ipaddress.ip_address("255.255.255.255")
        self.ip_method = "N/A"
        self.is_wifi = False
        self.wifi_radio = "N/A"

    def get_radio(self):
        return self.radio

    def get_mac(self):
        return self.mac

    def get_flags(self):
        # mimics Main_WStatus_Content.asp
        # "Flags: P=Powersave Mode, S=Short GI, T=STBC, M=MU Beamforming, A=Associated, U=Authenticated"

        flags = ""

        if self.psm == "Yes":
            flags += "P"
        else:
            flags += "_"
        if self.sgi == "Yes":
            flags += "S"
        else:
            flags += "_"
        if self.stbc == "Yes":
            flags += "T"
        else:
            flags += "_"
        if self.mubf == "Yes":
            flags += "M"
        else:
            flags += "_"
        if self.assoc == "Yes":
            flags += "A"
        else:
            flags += "_"
        if self.auth == "Yes":
            flags += "U"
        else:
            flags += "_"

        return flags

    def get_rssi(self):
        try:
            value = int(self.rssi[:-3])
        except Exception:
            value = 0
        return value

    def get_physical_mode(self):
        return self.phy  # n, ac, ax etc.

    def get_number_of_conn_streams(self):
        return int(self.nss) if self.nss.isdecimal() else 0

    def get_bandwith(self):
        bw = self.bw[:-1]  # "20M" means 20MHz
        return int(bw) if bw.isdecimal() else 0

    def _get_xx(self, value):
        xx = value[:-1]  # "720.6M" or "390M"
        try:
            value = float(xx)
        except ValueError:
            value = 0.0
        return value

    def get_tx(self):
        return self._get_xx(self.tx)

    def get_rx(self):
        return self._get_xx(self.rx)

    def get_time_in_seconds(self):
        seconds_total = 0
        # HH:MM:SS as defined in source code of asuswrt
        time_split = self.time.split(":")
        hours = int(time_split[0]) if time_split[0].isdecimal() else 0
        minutes = int(time_split[1]) if time_split[1].isdecimal() else 0
        seconds = int(time_split[2]) if time_split[2].isdecimal() else 0
        seconds_total = 60*60*hours+60*minutes+seconds
        return seconds_total

    def get_name(self):
        return self.name

    def get_vendor(self):
        return self.vendor

    def get_ip(self):
        return self.ip

    def get_ip_method(self):
        return self.ip_method

    def get_is_wifi(self):
        return self.is_wifi

    def get_wifi_radio(self):
        return self.wifi_radio

    def set_extra_fields_from_clientlist(self, client_dict):
        if type(client_dict) != dict:
            return
        self.name = client_dict.get("name", client_dict.get("nickName", "N/A"))
        self.vendor = client_dict.get("vendor", "N/A")
        try:
            self.ip = ipaddress.ip_address(
                client_dict.get("ip", "255.255.255.255"))
        except Exception:
            pass
        self.ip_method = client_dict.get("ip_method", "N/A")
        self.is_wifi = client_dict.get("isWL", "0") != "0"

        match client_dict.get("isWL", "0"):
            case "0":
                self.wifi_radio = "wired"
            case "1":
                self.wifi_radio = "2.4GHz"
            case "2":
                self.wifi_radio = "5GHz"
            case "3":
                self.wifi_radio = "5GHz2"
            case "4":
                self.wifi_radio = "6GHz"
            case "4":
                self.wifi_radio = "6GHz2"
            case _:
                self.wifi_radio = "N/A"
