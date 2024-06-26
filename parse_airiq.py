import regex
import random

noise = {}
channel_list = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    36,
    40,
    44,
    48,
    52,
    56,
    60,
    64,
    100,
    104,
    108,
    112,
    116,
    120,
    124,
    128,
    132,
    136,
    140,
    144,
    149,
    153,
    157,
    161,
    165,
    169,
    173,
    177,
]


def parse_airiq(log):
    tmp = log["airiq"]
    log["airiq"] = ""
    lines = regex.split("\n", tmp)
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
                noise[channel]["non_wifi"] = [0]
                noise[channel]["wifi"] = [0]
            noise[channel]["non_wifi"].append(int(non_wifi))
            noise[channel]["wifi"].append(int(wifi))
    return noise


def parse_airiq_offline(log: list):
    tmp = log.value
    lines = regex.split("\n", tmp)
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
                noise[channel]["non_wifi"] = [random.randint(0, 100)]
                noise[channel]["wifi"] = [random.randint(0, 100)]
            noise[channel]["non_wifi"].append(
                min(
                    100,
                    max(0, noise[channel]["non_wifi"][-1] + random.randint(-20, 20)),
                )
            )
            noise[channel]["wifi"].append(
                min(
                    100,
                    max(0, noise[channel]["wifi"][-1] + random.randint(-20, 20)),
                )
            )
    return noise
