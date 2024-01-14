from RouterInfo import RouterInfo
from ClientInfo import ClientInfo
from MeshNode import MeshNode

from pprint import pprint


class Mesh:
    def __init__(self, username, password, controller_ip, nodes_ips):
        self.username = username
        self.password = password
        self.controller_ip = controller_ip
        self.nodes_ips = nodes_ips

        self.nodes = {}
        self.high_level_client_list = {}
        self.clients_by_node = {}

        nodes_ips.append(controller_ip)
        for ip in nodes_ips:
            node = MeshNode(ip, username, password)
            self.nodes[ip] = node
            self.clients_by_node[ip] = node.get_clients()

        self.ri = RouterInfo(ip, username, password)
        self.high_level_client_list = self.ri.get_clients_fullinfo()[
            "get_clientlist"]

        for node_ip, clients in self.clients_by_node.items():
            for client_mac, client in clients.items():
                high_level_client_info = self.high_level_client_list.get(
                    client_mac)
                if high_level_client_info:
                    client.set_extra_fields_from_clientlist(
                        high_level_client_info)

    def get_clients_by_node(self):
        return self.clients_by_node
