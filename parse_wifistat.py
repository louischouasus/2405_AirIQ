import regex


def parse_txop(log: dict):
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

    return txop_2g, txop_5g, txop_6g


def parse_chanspec(log):
    pass
