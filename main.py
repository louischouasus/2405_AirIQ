import multiprocessing.context
import multiprocessing.managers
import multiprocessing.synchronize
import telnet_funcs
import telnetlib
import multiprocessing
import draw_tk
import parse_airiq
import parse_wifistat
import time
from ctypes import c_wchar_p

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
import sys
import pandas as pd
import numpy as np
import time
import random

TIME_LENGTH = 30
current_band = "2G"
channel_list = {
    "2G": [
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
    ],
    "5G": [
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
    ],
}


class Graph_txop(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_txop(self, txop: dict[dict[list]]):
        self.ax.clear()
        self.ax.set_yticks([i for i in range(0, 101, 10)], size="small")
        self.ax.set_ylim([0, 100])
        self.ax.set_xlim([0, TIME_LENGTH])
        self.ax.text(13, 30, "TXop", fontsize=30)
        for band in ["2G", "5G", "6G"]:
            if band in txop:
                x = txop[band][-TIME_LENGTH:]
                if len(x) < TIME_LENGTH:
                    x = [None] * (TIME_LENGTH - len(x)) + x
                self.ax.plot(x, linewidth=5, markersize=15)

        self.canvas.draw()


class Graph_util(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_util(self, noise: dict[dict[list]]):
        self.ax.clear()
        self.ax.set_yticks([i for i in range(0, 101, 10)], size="small")
        self.ax.set_ylim([0, 100])
        self.ax.set_xlim([0, TIME_LENGTH])
        self.ax.text(12, 30, "Channel usage", fontsize=30)
        for channel in noise:
            if channel in channel_list[current_band]:
                x = noise[channel]["wifi"][-TIME_LENGTH:]
                if len(x) < TIME_LENGTH:
                    x = [None] * (TIME_LENGTH - len(x)) + x
                self.ax.plot(x, linewidth=5, markersize=15)
        self.canvas.draw()


class Graph_noise(tk.Frame):
    global channel_list

    def __init__(self, master=None, *args, **kwargs):

        super().__init__(master, *args, **kwargs)

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_noise(
        self, noise: dict[dict[list]], current_band: str, mix, chanspec, radar
    ):
        self.ax.clear()
        self.ax.set_yticks(
            range(len(channel_list[current_band])),
            channel_list[current_band],
            size="small",
        )
        self.ax.set_ylim([0, len(channel_list[current_band])])
        self.ax.set_xlim([0, TIME_LENGTH])
        for channel in noise:
            if int(channel) in channel_list[current_band]:
                if mix == False:
                    self.add_non_wifi(
                        channel, noise[channel]["non_wifi"][-TIME_LENGTH:]
                    )
                    self.add_wifi(channel, noise[channel]["wifi"][-TIME_LENGTH:])
                else:
                    self.add_mix(
                        channel,
                        noise[channel]["total"][-TIME_LENGTH:],
                    )
                self.add_radar(channel, radar[channel][-TIME_LENGTH:])
        self.add_currenct_channel(chanspec[current_band][-TIME_LENGTH:])
        self.canvas.draw()

    def add_non_wifi(self, channel: int, value: list):
        channel_index = channel_list[current_band].index(int(channel))
        if len(value) < TIME_LENGTH:
            value = [None] * (TIME_LENGTH - len(value)) + value
        t = 0
        for v in value:
            if v == None:
                t += 1
                continue
            self.ax.add_collection(
                PolyCollection(
                    [
                        [
                            [t, channel_index],
                            [t, channel_index + 1],
                            [t + 1, channel_index + 1],
                        ]
                    ],
                    facecolor=(0.9, 0.9 - v / 112, 0.9 - v / 112),
                    edgecolor=(0, 0, 0),
                    linewidth=0.5,
                ),
            )
            t += 1

    def add_wifi(self, channel: int, value: list):
        channel_index = channel_list[current_band].index(int(channel))
        if len(value) < TIME_LENGTH:
            value = [None] * (TIME_LENGTH - len(value)) + value
        t = 0
        for v in value:
            if v == None:
                t += 1
                continue
            self.ax.add_collection(
                PolyCollection(
                    [
                        [
                            [t, channel_index],
                            [t + 1, channel_index],
                            [t + 1, channel_index + 1],
                        ]
                    ],
                    facecolor=(0.9 - v / 112, 0.9, 0.9 - v / 112),
                    edgecolor=(0, 0, 0),
                    linewidth=0.5,
                ),
            )
            t += 1

    def add_mix(self, channel: int, value: list):
        channel_index = channel_list[current_band].index(int(channel))
        if len(value) < TIME_LENGTH:
            value = [None] * (TIME_LENGTH - len(value)) + value
        t = 0
        for v in value:
            if v == None:
                t += 1
                continue
            v = min(v, 100)
            self.ax.add_collection(
                PolyCollection(
                    [
                        [
                            [t, channel_index],
                            [t + 1, channel_index],
                            [t + 1, channel_index + 1],
                            [t, channel_index + 1],
                        ]
                    ],
                    facecolor=(0.1 + v / 112, 0.9 - v / 112, 0.1),
                    edgecolor=(0, 0, 0),
                    linewidth=0.5,
                ),
            )
            t += 1

    def add_currenct_channel(self, current_channels):
        # add a light blue rectangle to highlight the current channel
        if len(current_channels) < TIME_LENGTH:
            current_channels = [None] * (
                TIME_LENGTH - len(current_channels)
            ) + current_channels
        t = 0
        for channels in current_channels:
            if channels == None:
                t += 1
                continue
            channel = channels[0]
            bandwidth = channels[1]
            h = bandwidth / 20 / 2
            if channel in channel_list[current_band]:
                w = channel_list[current_band].index(channel)
                self.ax.add_collection(
                    PolyCollection(
                        [
                            [
                                [t, w + 0.5 - h],
                                [t + 1, w + 0.5 - h],
                                [t + 1, w + 0.5 + h],
                                [t, w + 0.5 + h],
                            ]
                        ],
                        facecolor="none",
                        edgecolor=(0, 0, 1),
                        linewidth=2,
                    ),
                )
            t += 1

    def add_radar(self, channel, value: list):
        channel_index = channel_list[current_band].index(int(channel))
        if len(value) < TIME_LENGTH:
            value = [0] * (TIME_LENGTH - len(value)) + value
        t = 0
        for v in value:
            if v == 0:
                t += 1
                continue

            self.ax.add_collection(
                PolyCollection(
                    [
                        [
                            [t, channel_index + 0.3],
                            [t + 1, channel_index + 0.3],
                            [t + 1, channel_index + 0.7],
                            [t, channel_index + 0.7],
                        ]
                    ],
                    facecolor=(0.3, 0.3, 0.3),
                    edgecolor=(0, 0, 0),
                    linewidth=0.5,
                ),
            )
            t += 1


class app(tk.Tk):
    def __init__(self):
        super().__init__()
        self.bind("<Configure>", self.resize)
        self.wm_title("Noise 2G")
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nesw")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.button_changeband = tk.Button(
            self, text="Noise: Change band", command=self.change_band
        )
        self.button_changeband.grid(row=1, column=0, sticky="nesw")
        self.button2 = tk.Button(self, text="Mix", command=self.change_noise_mix)
        self.button2.grid(row=1, column=1, sticky="nesw")
        self.button3 = tk.Button(self, text="Add radar", command=self.add_radar_signal)
        self.button3.grid(row=1, column=2, sticky="nesw")
        self.button3 = tk.Button(
            self, text="Channel Utilization", command=self.change_utilmode
        )
        self.button3.grid(row=1, column=3, sticky="nesw")
        self.graph_util = Graph_util(self)
        self.graph_txop = Graph_txop(self)
        self.graph_noise = Graph_noise(self)
        self.graph_noise.grid(row=0, column=0, columnspan=10, sticky="nesw")
        self.in_radar = []
        self.mode = "noise"
        self.mix = False

    def change_band(self):
        global current_band
        # switch graph showing band 2g <-> 5g
        if current_band == "2G":
            current_band = "5G"
        else:
            current_band = "2G"

    def change_noise_mix(self):
        self.mix = not self.mix

    def resize(self, event):
        global window_width, window_height
        if event.widget.master != None:
            return
        window_height = event.height
        window_width = event.width

    def add_radar_signal(self):
        t = random.randint(0, len(channel_list[current_band]))
        self.in_radar.append(channel_list[current_band][t])
        self.after(5000, self.remove_radar, channel_list[current_band][t])

    def remove_radar(self, t):
        self.in_radar.remove(t)

    def change_utilmode(self):
        if self.mode == "util":
            self.mode = "noise"
            self.wm_title(f"Noise {current_band}")
        elif self.mode == "txop":
            self.mode = "util"
            self.wm_title(f"Channel Usage {current_band}")
        elif self.mode == "noise":
            self.mode = "txop"
            self.wm_title("Txop")

    def update_data(self):
        print("mainapp update_data")
        airiq_lock.acquire()
        noise, radar = parse_airiq.parse_airiq(airiq_dict)
        for r in self.in_radar:
            radar[r][-1] = 1
        airiq_lock.release()

        wifistat_lock.acquire()
        txop = parse_wifistat.parse_txop(wifistat_dict)
        chanspec = parse_wifistat.parse_chanspec(wifistat_dict)
        wifistat_lock.release()
        if self.mode == "util":
            self.graph_util.grid(row=0, column=0, columnspan=10, sticky="nesw")
            self.graph_noise.grid_forget()
            self.graph_txop.grid_forget()
            self.graph_util.update_util(noise)
            pass
        elif self.mode == "txop":
            self.graph_util.grid_forget()
            self.graph_noise.grid_forget()
            self.graph_txop.grid(row=0, column=0, columnspan=10, sticky="nesw")
            self.graph_txop.update_txop(txop)
            pass
        elif self.mode == "noise":
            self.graph_util.grid_forget()
            self.graph_txop.grid_forget()
            self.graph_noise.grid(row=0, column=0, columnspan=10, sticky="nesw")
            self.graph_noise.update_noise(
                noise, current_band, self.mix, chanspec, radar
            )
            self.graph_noise.update()
        self.update()
        self.after(1000, self.update_data)


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
        "chanspec_2g": "wl -i wl0 chanspec",
        "chanspec_5g": "wl -i wl1 chanspec",
        "chanspec_6g": "wl -i wl2 chanspec",
    }
    for command in commands:
        if command not in wifistat_dict:
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
        if time.time() - start_time < 1:
            time.sleep(1 - (time.time() - start_time))


def airiq_commands(
    client_airiq: telnetlib.Telnet,
    airiq_dict: multiprocessing.managers.DictProxy,
    airiq_lock: multiprocessing.synchronize.Lock,
):
    telnet_funcs.command_cycle(
        client_airiq,
        "airiq_app -i wl0 -phy_mode 4x4 -d 500 -c 50 -b -int -i wl1 -phy_mode 4x4 -d 1000 -c 50 -a -int -print_events",
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
    telnet_airiq.start()
    telnet_wifistat.start()
    time.sleep(1)
    a = app()

    a.after(
        1,
        a.update_data,
    )
    a.mainloop()
