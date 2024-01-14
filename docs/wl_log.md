# wl_log

## Data origin

WebUI has page [`/Main_WStatus_Content.asp`](https://github.com/RMerl/asuswrt-merlin.ng/blob/master/release/src/router/www/Main_WStatus_Content.asp) which calls `/wl_log.asp`. Basic version of ASUSWRT shows just plain output from that second endpoint, Merlin renders it as a nice table, but still alows you to see raw data.

This short ASP script consists only of `<% nvram_dump("wlan11b_2g.log",""); %>`. Normally, `nvram_dump` is equivalent of `/bin/nvram get`, however `wlan11b_2g.log` is one of special cases for this function. After long series of interanl calls, `ej_wl_status` from [`./release/src/router/httpd/sysdeps/web-broadcom.c`](https://github.com/RMerl/asuswrt-merlin.ng/blob/master/release/src/router/httpd/sysdeps/web-broadcom.c) is called to construct output. 

There's `get_wl_status()` (which calls `ej_wl_status_array` from ``./release/src/router/httpd/sysdeps/web-broadcom-am.c`), but it works only on AiMesh router, not repaters/nodes.

## Data structure

Data returned is raw text with various sections and no header to entire data. Sections may or may not be present depending on specific radio being enabled, disabled, not present or probably various other conditions. Some section content varies by device model or mode it is in.

All sections except for first, have header: title that is "underlined" in next line by fixed amount of dashes, for example:

```
Stations List
----------------------------------------
```

The only known thing is that if both 2.4GHz and 5GHz radios are enabled, 2.4GHz one will be first. Code is so spaghetti that I can't decipher how would it behave for devices with 6GHz radio or multiple 5GHz...

### Stations List

Example data:

for 2.4GHz:
```
Stations List
----------------------------------------
idx MAC               Associated Authorized   RSSI PHY PSM SGI STBC MUBF NSS   BW Tx rate Rx rate Connect Time
1   XX:XX:XX:XX:XX:C8 Yes        Yes        -30dBm n   Yes Yes Yes  No     1  20M   72.2M      6M     04:03:24
```

for 5GHz:
```
Stations List
----------------------------------------
idx MAC               Associated Authorized   RSSI PHY PSM SGI STBC MUBF NSS   BW Tx rate Rx rate Connect Time
1   XX:XX:XX:XX:XX:12 Yes        Yes        -59dBm ax  Yes Yes No   No     2  80M  864.7M     24M     00:02:24
1   XX:XX:XX:XX:XX:6A Yes        Yes        -61dBm ax  No  Yes No   No     2  80M  720.6M  960.7M     00:14:16
1   XX:XX:XX:XX:XX:26 Yes        Yes        -49dBm ax  No  Yes Yes  No     2  80M  612.5M  864.7M     00:16:25
1   XX:XX:XX:XX:XX:AF Yes        Yes        -73dBm ac  Yes Yes Yes  No     2  80M    390M     18M     13:14:30
1   XX:XX:XX:XX:XX:63 Yes        Yes        -69dBm ax  No  Yes No   No     2  80M  864.7M  154.8M     13:47:36
```
