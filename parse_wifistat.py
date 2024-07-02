import regex

txop = {"2G": [], "5G": [], "6G": []}
chanspec = {"2G": [], "5G": [], "6G": []}


def parse_txop(logdict: dict):
    log = logdict["txop"]
    logdict["txop"] = ""
    txop_2g = regex.search(r"([0-9]+)\|2G", log)
    txop_5g = regex.search(r"([0-9]+)\|5G", log)
    txop_6g = regex.search(r"([0-9]+)\|6G", log)
    if txop_2g:
        txop_2g = int(txop_2g.group(1))
    else:
        txop_2g = -1
    if txop_5g:
        txop_5g = int(txop_5g.group(1))
    else:
        txop_5g = -1
    if txop_6g:
        txop_6g = int(txop_6g.group(1))
    else:
        txop_6g = -1
    txop["2G"].append(txop_2g)
    txop["5G"].append(txop_5g)
    txop["6G"].append(txop_6g)
    return txop


def parse_chanspec_log(log: str):
    res = regex.search(r"(6g)?([0-9]+)\/?([0-9]+)?.*\(*\)", log)
    if res != None:
        if res.group(3):
            return int(res.group(2)), int(res.group(3))
        else:
            return int(res.group(2)), 20


def parse_chanspec(logdict: dict):

    chanspec_2g = parse_chanspec_log(logdict["chanspec_2g"])
    chanspec_5g = parse_chanspec_log(logdict["chanspec_5g"])
    chanspec_6g = logdict["chanspec_6g"]
    chanspec["2G"].append(chanspec_2g)
    chanspec["5G"].append(chanspec_5g)
    chanspec["6G"].append(chanspec_6g)
    return chanspec
