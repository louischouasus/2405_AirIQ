import multiprocessing.context
import multiprocessing.managers
import multiprocessing.synchronize
import telnet_funcs
import telnetlib
import multiprocessing
import draw_chart
import parse_airiq
import parse_wifistat
import time
from ctypes import c_wchar_p

hostname = "192.168.50.1"
username = "admin"
password = "asus#1234"


def wifistat_commands(
    client_wifistat: telnetlib.Telnet,
    wifistat_dict: multiprocessing.managers.DictProxy,
    wifistat_lock: multiprocessing.synchronize.Lock,
):

    commands = {
        "txop": "sqlite3 wifi_detect.db 'select txop, band from DATA_INFO ORDER BY rowid DESC LIMIT 3;'",
        "2G_chanspec": "wl -i wl0 chanspec",
        "5G_chanspec": "wl -i wl1 chanspec",
        "6G_chanspec": "wl -i wl2 chanspec",
    }
    for command in commands:
        wifistat_dict[command] = ""
    while True:
        start_time = time.time()
        for command in commands:
            telnet_funcs.command(
                client_wifistat,
                commands[command],
                wifistat_dict,
                command,
                wifistat_lock,
            )
        print(wifistat_dict)
        if time.time() - start_time < 1:
            time.sleep(1 - (time.time() - start_time))


def airiq_commands(
    client_airiq: telnetlib.Telnet,
    airiq_dict: multiprocessing.managers.DictProxy,
    airiq_lock: multiprocessing.synchronize.Lock,
):
    telnet_funcs.command_cycle(
        client_airiq,
        "airiq_app -i wl0 -phy_mode 4x4 -d 1000 -c 50 -b -int -i wl1 -phy_mode 4x4 -d 1000 -c 50 -a -int -print_events",
        airiq_dict,
        "airiq",
        airiq_lock,
    )


if __name__ == "__main__":

    # create telnet connection and init
    client_airiq = telnet_funcs.connect(hostname, username, password)
    client_airiq.write("airiq_service -d".encode("ascii") + b"\n")

    client_wifistat = telnet_funcs.connect(hostname, username, password)
    client_wifistat.write("cd /tmp/.diag".encode("ascii") + b"\n")

    # multiprocessing lock and value can trans between threads
    airiq_lock = multiprocessing.Lock()
    airiq_manager = multiprocessing.Manager()
    airiq_dict = airiq_manager.dict()

    wifistat_lock = multiprocessing.Lock()
    wifistat_manager = multiprocessing.Manager()
    wifistat_dict = wifistat_manager.dict()

    telnet_airiq = multiprocessing.Process(
        target=airiq_commands,
        args=(
            client_airiq,
            airiq_dict,
            airiq_lock,
        ),
    )
    telnet_wifistat = multiprocessing.Process(
        target=wifistat_commands,
        args=(
            client_wifistat,
            wifistat_dict,
            wifistat_lock,
        ),
    )
    time.sleep(1)
    telnet_wifistat.start()
    app = draw_chart.Graph()
    while True:
        try:
            start_time = time.time()

            airiq_lock.acquire()
            noise = parse_airiq.parse_airiq(airiq_dict)
            airiq_lock.release()

            wifistat_lock.acquire()
            txop = parse_wifistat.parse_txop(wifistat_dict)
            wifistat_lock.release()
            print(txop)
            if time.time() - start_time < 1:
                time.sleep(1 - (time.time() - start_time))
        except KeyboardInterrupt:
            telnet_wifistat.join()
            telnet_airiq.join()
            break
