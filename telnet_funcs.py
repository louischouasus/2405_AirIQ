import multiprocessing.synchronize
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
        time.sleep(0.5)
        return client
    except Exception as e:
        print("Connection failed: ", e)


def command(
    client: telnetlib.Telnet,
    cmd: str,
    logdict: dict,
    logname: str,
    log_lock: multiprocessing.synchronize.Lock,
):
    # write a command and wait for its output once
    client.write(cmd.encode("ascii") + b"\n")
    # time.sleep(0.2)
    try:
        log_lock.acquire()
        logdict[logname] += client.read_very_eager().decode("ascii")
        print(logdict[logname])
        log_lock.release()
    except KeyboardInterrupt:
        client.write("\x03\n")
        log_lock.release()


def command_cycle(
    client: telnetlib.Telnet,
    cmd: str,
    logdict: dict,
    logname: str,
    log_lock: multiprocessing.synchronize.Lock,
):
    # write a command and get output every sec
    client.write(cmd.encode("ascii") + b"\n")
    while True:
        try:
            start_time = time.time()

            log_lock.acquire()
            if logdict.get(logname) is None:
                logdict[logname] = ""
            logdict[logname] += client.read_very_eager().decode("ascii")
            log_lock.release()
            if time.time() - start_time < 1:
                time.sleep(1 - (time.time() - start_time))

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
