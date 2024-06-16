import regex

noise = {}


def parse_airiq(log: list):
    lines = regex.split("\n", log)
    for line in lines:
        print(line)
        res = regex.match(
            #  eventdata:10 Channel  11: Non-wifi:   0% Wi-fi:  54% Total:  54%
            r"#eventdata:.*Channel *([0-9]+): Non-wifi: *([0-9]+)% Wi-fi: *([0-9]+)% Total: *([0-9]+)%",
            line,
        )
        if res != None:
            channel = res.group(1)
            non_wifi = res.group(2)
            wifi = res.group(3)

            if channel not in noise:
                noise[channel] = {}
                noise[channel]["non_wifi"] = []
                noise[channel]["wifi"] = []
            noise[channel]["non_wifi"].append(int(non_wifi))
            noise[channel]["wifi"].append(int(wifi))
    return noise
