import regex
import random

noise = {}
radar = {}

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
for c in channel_list:
    noise[c] = {}
    noise[c]["non_wifi"] = [None]
    noise[c]["wifi"] = [None]
    noise[c]["total"] = [None]
    radar[c] = [0]


def parse_airiq(log):
    tmp = log["airiq"]
    log["airiq"] = ""
    lines = regex.split("\n", tmp)
    found_channel = channel_list.copy()
    count = 0
    for line in lines:
        res = regex.match(
            #  eventdata:10 Channel  11: Non-wifi:   0% Wi-fi:  54% Total:  54%
            r"#eventdata:.*Channel *([0-9]+): Non-wifi: *([0-9]+)% Wi-fi: *([0-9]+)% Total: *([0-9]+)%",
            line,
        )

        if res != None:
            count += 1
            channel = int(res.group(1))
            non_wifi = int(res.group(2))
            wifi = int(res.group(3))
            total = int(res.group(4))

            if channel not in noise:
                continue

            noise[channel]["non_wifi"].append(int(non_wifi))
            noise[channel]["wifi"].append(int(wifi))
            noise[channel]["total"].append(int(total))
            radar[channel].append(0)
            try:
                found_channel.remove(int(channel))
            except:
                pass

    for c in found_channel:
        noise[c]["non_wifi"].append(noise[c]["non_wifi"][-1])
        noise[c]["wifi"].append(noise[c]["wifi"][-1])
        noise[c]["total"].append(noise[c]["total"][-1])
        radar[c].append(0)
    print(f"parse_airiq get: {count}/{len(channel_list)}")
    return noise, radar
