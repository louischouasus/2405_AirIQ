import telnet
import multiprocessing
import draw_chart
import parse_airiq
import time
from ctypes import c_wchar_p

hostname = "192.168.50.1"
username = "admin"
password = "asus#1234"

if __name__ == "__main__":
    client = telnet.connect(hostname, username, password)
    log_lock = multiprocessing.Lock()
    manager = multiprocessing.Manager()
    log = manager.Value(c_wchar_p, "")

    telnet_read = multiprocessing.Process(
        target=telnet.command_offline,
        args=(
            client,
            "airiq_app -i wl0 -phy_mode 4x4 -d 1000 -c 50 -b -int -print_events",
            log,
            log_lock,
        ),
    )
    time.sleep(1)
    telnet_read.start()
    app = draw_chart.Graph()
    while True:
        try:
            print("main", log.value)
            log_lock.acquire()
            noise = parse_airiq.parse_airiq_offline(log)
            log.value = ""
            log_lock.release()
            app.update_data(noise)
        except KeyboardInterrupt:
            pass
            break

    telnet_read.join()
