import telnetlib
import time
import multiprocessing


def connect(hostname: str, username: str, password: str) -> telnetlib.Telnet:
    try:
        client = telnetlib.Telnet(hostname)
        client.read_until(b"login")
        client.write(username.encode("ascii") + b"\n")
        client.read_until(b"Password")
        client.write(password.encode("ascii") + b"\n")
        print("login successed")
        client.write("airiq_service -d".encode("ascii") + b"\n")
        time.sleep(0.5)
        return client
    except Exception as e:
        print("Connection failed: ", e)


def command(
    client: telnetlib.Telnet, cmd: str, log: list, log_lock: multiprocessing.Lock
):
    client.write(cmd.encode("ascii") + b"\n")
    while True:
        try:
            log_lock.acquire()
            log.value += client.read_until(b"\n").decode("ascii")
            print(log.value)
            log_lock.release()
        except KeyboardInterrupt:
            client.write("\x03\n")
            log_lock.release()
            break


def command_offline(
    client: telnetlib.Telnet, cmd: str, log: list, log_lock: multiprocessing.Lock
):
    print("telnet start")
    while True:

        log_lock.acquire()
        with open("AirIQ.log", "r") as f:
            l = f.read()
        log.value = log.value + l
        time.sleep(0.1)
        log_lock.release()
        time.sleep(1)
