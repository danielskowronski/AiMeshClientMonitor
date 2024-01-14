from Mesh import Mesh
from pprint import pprint
from operator import itemgetter

from rich.console import Console
from rich.table import Table
import time
from rich.live import Live
import datetime
import keyring
import argparse

console = Console()


def gen_table(user, password, router, aps):
    m = Mesh(user, password, router, aps)
    clients_by_node = m.get_clients_by_node()
    table = Table(show_header=True, header_style="bold")
    table.add_column("RSSI", style="cyan", width=4, justify="right")
    table.add_column("G\nH\nz",  style="yellow", width=1, justify="left")
    table.add_column("PH",  style="yellow", width=2, justify="right")
    table.add_column("Client Name", width=30)
    table.add_column("Client MAC", style="dim", width=17)
    table.add_column("RX\nMb/s", style="dim", width=4, justify="right")
    table.add_column("TX\nMb/s", style="dim", width=4, justify="right")
    table.add_column("Flag", style="dim", width=4)  # 6
    table.add_column("Str\neam\ncnt", style="dim", width=3, justify="right")
    table.add_column("BW\nMHz", style="dim", width=3, justify="right")
    table.add_column("Conn Time", style="dim", justify="right")

    for node, clients in clients_by_node.items():
        table.add_section()
        table.add_row(None, None, None, f"AiMesh {node}", None, None, None, None, None, None, None, style="magenta")

        clients_list_sorted = sorted(
            list(clients.values()), key=lambda x: x.rssi)
        for client in clients_list_sorted:
            table.add_row(
                "{: 3d}".format(client.get_rssi()),
                client.get_wifi_radio().replace("GHz", "")[0],
                client.get_physical_mode(),
                client.get_name(),
                client.get_mac(),
                "{:.0f}".format(client.get_rx()),
                "{:.0f}".format(client.get_tx()),
                client.get_flags()[0:4],
                str(client.get_number_of_conn_streams()),
                str(client.get_bandwith()),
                # str(client.get_time_in_seconds())
                str(datetime.timedelta(seconds=client.get_time_in_seconds()))
            )
    return table


parser = argparse.ArgumentParser(prog="AiMeshClientMonitor",
                                 description="AiMeshClientMonitor")
parser.add_argument("--delay",  nargs=1, type=int,
                    default=[3], help="how many seconds between data refresh")
parser.add_argument("router", nargs=1, type=str,
                    help="IP of AiMesh Controller or single Router")
parser.add_argument("ap", nargs="*", default=[], type=str,
                    help="IPs of AiMesh nodes or APs")
args = parser.parse_args()

user = keyring.get_password("AiMeshClientMonitor", "username")
password = keyring.get_password("AiMeshClientMonitor", "password")
router = args.router[0]
aps = args.ap
delay = args.delay[0]

console.clear()
with Live(gen_table(user, password, router, aps), refresh_per_second=1) as live:
    while True:
        time.sleep(delay)
        live.update(gen_table(user, password, router, aps))
