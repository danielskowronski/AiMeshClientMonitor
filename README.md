# AiMeshClientMonitor

Python classes and CLI tool for displaying live WiFi clients information from ASUS-WRT routers and all connected AiMesh nodes or regular APs.

ASUS-WRT has built-in clients information in two places:

- *System Log* - *Wireless Log* which is as detailed as it can be, but only shows clients from current device, which is very problematic if you want to look for node roaming (plus, by default you can't log in to Web UI of AiMesh nodes)
- *Network Map* - *Clients* - *View List* which is very limited in waht it can show, but at least lists all clients

For source data format see [wl_log.md](./docs/wl_log.md) and [clientlist.md](./docs/clientlist.md).

## Classes

### Mesh

Takes username, passowrd, main router IP and IPs of APs/nodes. Keeps `MeshNode` data for all APs including router and additional data polled from router (device aliases, IPs etc.) aas they are only available on controller.

### MeshNode

Wraps around `RouterInfo`, which is fork of [github.com/lmeulen/AsusRouterMonitor](https://github.com/lmeulen/AsusRouterMonitor) with `get_wl_log()` added.  

Additionaly, attempts to parse raw data about connected clients (stations) and construct `ClientInfo` objects to be stored in map.

### ClientInfo

Stores all information about wireless station that are available from radio and optional additional metadata from router like friendly name (DHCP name), IP address, radio type, vendor (from MAC).

---

## CLI app

CLI app uses Rich library to draw live refreshing table of all clients groupped by AP and then sorted by RSSI from strongest to weakest signal.

```
usage: AiMeshClientMonitor [-h] [--delay DELAY] router [ap ...]

AiMeshClientMonitor

positional arguments:
  router         IP of AiMesh Controller or single Router
  ap             IPs of AiMesh nodes or APs

options:
  -h, --help     show this help message and exit
  --delay DELAY  how many seconds between data refresh
```

It uses system [Keyring](https://pypi.org/project/keyring/) to keep username and passowrd as they are the same for all AiMesh nodes. IPs are passed as CLI arguments with option to change refresh rate.

Fields in table:

- **RSSI** - value in dBm
- **GHz** - radio type, mapped as follows:
  - `cable` for wired clients (those are omitted),
  - `2` for `2.4GHz` used internally
  - `5` for `5GHz` and `5 GHz 2` used internally (first and 2nd 5GHz radio if present)
  - `6` for `6GHz` and `6 GHz 2` used internally (first and 2nd 6GHz radio if present)
- **PH** - PHYsical connection mode, extensions to 802.11 standard (d, ac, ax etc.)
- **Client Name** - DHCP name, name discovered by router or MAC if not available
- **Client MAC**
- **RX** & **TX** - currently negotiated receive and transmit speeds, rounded up to decimals; not actually transfer used
- **Flag** - various modes in convention from ASUS-WRT: 
  - `P` - Powersave Mode
  - `S` - Short GI
  - `T` - STBC
  - `M` - MU Beamforming
  - `A` - Associated (omitted)
  - `U` - Authenticated (omitted)
- **Streama cnt** - value of NSS
- **BW MHz** - bandwith allocated to client connection
- **Conn Time** - how long connection is established, HH:MM:SS

set credentials:

```bash
keyring set AiMeshClientMonitor username
keyring set AiMeshClientMonitor password
```

example run `python3 AiMeshClientMonitor.py 192.168.1.1 192.168.1.4 192.168.1.5 --delay 1`

```
┏━━━━━━┳━━━┳━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━┳━━━━━━┳━━━━━┳━━━━━┳━━━━━━━━━━━┓
┃      ┃ G ┃    ┃                                ┃                   ┃      ┃      ┃      ┃ Str ┃     ┃           ┃
┃      ┃ H ┃    ┃                                ┃                   ┃   RX ┃   TX ┃      ┃ eam ┃  BW ┃           ┃
┃ RSSI ┃ z ┃ PH ┃ Client Name                    ┃ Client MAC        ┃ Mb/s ┃ Mb/s ┃ Flag ┃ cnt ┃ MHz ┃ Conn Time ┃
┡━━━━━━╇━━━╇━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━╇━━━━━━╇━━━━━╇━━━━━╇━━━━━━━━━━━┩
│      │   │    │ AiMesh 192.168.1.2             │                   │      │      │      │     │     │           │
│  -41 │ 2 │  n │ foo_001                        │ XX:XX:XX:XX:XX:XX │   72 │   72 │ _ST_ │   1 │  20 │   9:51:49 │
│  -50 │ 2 │  n │ foo_002                        │ A8:XX:XX:XX:XX:XX │   24 │   65 │ PS__ │   1 │  20 │   4:13:00 │
├──────┼───┼────┼────────────────────────────────┼───────────────────┼──────┼──────┼──────┼─────┼─────┼───────────┤
│      │   │    │ AiMesh 192.168.1.3             │                   │      │      │      │     │     │           │
│  -32 │ 2 │  n │ foo_003                        │ XX:XX:XX:XX:XX:XX │    6 │   58 │ PST_ │   1 │  20 │   7:06:30 │
│  -55 │ 5 │ ax │ foo_004                        │ XX:XX:XX:XX:XX:XX │ 1081 │ 1081 │ _ST_ │   2 │  80 │   3:19:32 │
│  -65 │ 5 │ ax │ foo_005                        │ XX:XX:XX:XX:XX:XX │   24 │  544 │ _S__ │   2 │  80 │   2:00:02 │
│  -68 │ 5 │ ax │ foo_006                        │ XX:XX:XX:XX:XX:XX │  172 │  961 │ _S__ │   2 │  80 │  16:50:43 │
│  -73 │ 5 │ ac │ foo_007                        │ XX:XX:XX:XX:XX:XX │   18 │  351 │ PST_ │   2 │  80 │  16:17:37 │
├──────┼───┼────┼────────────────────────────────┼───────────────────┼──────┼──────┼──────┼─────┼─────┼───────────┤
│      │   │    │ AiMesh 192.168.1.1             │                   │      │      │      │     │     │           │
│  -37 │ 5 │ ax │ foo_008                        │ XX:XX:XX:XX:XX:XX │   24 │ 1201 │ _S__ │   2 │  80 │  22:02:18 │
│  -40 │ 2 │  n │ foo_009                        │ XX:XX:XX:XX:XX:XX │    6 │   72 │ PST_ │   1 │  20 │  22:01:03 │
│  -42 │ 2 │  n │ foo_010                        │ XX:XX:XX:XX:XX:XX │   24 │   65 │ PS__ │   1 │  20 │  22:01:11 │
│  -43 │ 2 │  n │ foo_011                        │ XX:XX:XX:XX:XX:XX │    1 │   65 │ PS__ │   1 │  20 │  18:33:38 │
│  -43 │ 2 │  n │ foo_012                        │ XX:XX:XX:XX:XX:XX │   72 │   72 │ _ST_ │   1 │  20 │  22:00:14 │
│  -43 │ 2 │  n │ foo_013                        │ XX:XX:XX:XX:XX:XX │    6 │   72 │ PST_ │   1 │  20 │  22:01:01 │
│  -43 │ 5 │  n │ foo_014                        │ XX:XX:XX:XX:XX:XX │   72 │   72 │ _ST_ │   1 │  20 │  22:02:29 │
│  -46 │ 5 │ ac │ foo_015                        │ XX:XX:XX:XX:XX:XX │  867 │  780 │ PS__ │   2 │  80 │  19:05:40 │
│  -47 │ 5 │ ac │ foo_016                        │ XX:XX:XX:XX:XX:XX │  867 │  780 │ _S__ │   2 │  80 │  18:29:29 │
│  -49 │ 2 │  n │ foo_017                        │ XX:XX:XX:XX:XX:XX │    1 │   65 │ PST_ │   1 │  20 │  18:33:39 │
│  -49 │ 2 │  n │ foo_018                        │ XX:XX:XX:XX:XX:XX │   54 │  130 │ _ST_ │   2 │  20 │  22:00:57 │
│  -49 │ 5 │ ac │ foo_019                        │ XX:XX:XX:XX:XX:XX │  867 │  867 │ PS__ │   2 │  80 │  19:06:10 │
│  -49 │ 5 │  n │ foo_020                        │ XX:XX:XX:XX:XX:XX │   72 │   72 │ _ST_ │   1 │  20 │  22:02:29 │
│  -50 │ 5 │ ac │ foo_021                        │ XX:XX:XX:XX:XX:XX │  260 │  292 │ _S__ │   1 │  80 │  22:02:19 │
│  -56 │ 5 │  n │ foo_022                        │ XX:XX:XX:XX:XX:XX │  150 │  135 │ _S__ │   1 │  40 │  22:02:11 │
│  -57 │ 5 │ ax │ foo_023                        │ XX:XX:XX:XX:XX:XX │ 1081 │ 1201 │ _S__ │   2 │  80 │  22:02:26 │
│  -60 │ 5 │ ac │ foo_024                        │ XX:XX:XX:XX:XX:XX │   24 │  780 │ PS__ │   2 │  80 │  21:48:12 │
│  -63 │ 2 │  g │ foo_025                        │ XX:XX:XX:XX:XX:XX │   24 │   24 │ ____ │   1 │  20 │  19:06:09 │
└──────┴───┴────┴────────────────────────────────┴───────────────────┴──────┴──────┴──────┴─────┴─────┴───────────┘
```
