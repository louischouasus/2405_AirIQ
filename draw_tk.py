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


class Graph_noise(tk.Frame):
    global channel_list

    def __init__(self, master=None, title="", *args, **kwargs):

        super().__init__(master, *args, **kwargs)

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_noise(self, noise: dict[dict[list]], current_band: list[int], mix):

        self.ax.clear()
        self.ax.set_yticks(
            range(len(channel_list[current_band])),
            channel_list[current_band],
            size="small",
        )
        self.ax.set_ylim([0, len(channel_list[current_band])])
        self.ax.set_xlim([0, TIME_LENGTH])
        for channel in noise:
            if channel in channel_list[current_band]:
                if mix == False:
                    self.add_non_wifi(
                        channel, noise[channel]["non_wifi"][-TIME_LENGTH:]
                    )
                    self.add_wifi(channel, noise[channel]["wifi"][-TIME_LENGTH:])
                else:
                    self.add_mix(
                        channel,
                        noise[channel]["non_wifi"][-TIME_LENGTH:]
                        + noise[channel]["wifi"][-TIME_LENGTH:],
                    )
        self.canvas.draw()

    def add_non_wifi(self, channel: int, value: list):
        channel_index = channel_list[current_band].index(int(channel))
        if len(value) < TIME_LENGTH:
            value = [0] * (TIME_LENGTH - len(value)) + value
        t = 0
        for v in value:
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

    def add_wifi(self, channel: int, value: int):
        channel_index = self.channel_list.index(int(channel))
        if len(value) < TIME_LENGTH:
            value = [0] * (TIME_LENGTH - len(value)) + value
        t = 0
        for v in value:
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

    def add_mix(self, channel: int, value1: int):
        channel_index = self.channel_list.index(int(channel))
        if len(value) < TIME_LENGTH:
            value = [0] * (TIME_LENGTH - len(value)) + value
        t = 0
        for v in value:
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

    def add_currenct_channel(self, current_channel: list[int]):
        # add a light blue rectangle to highlight the current channel
        for channel in current_channel:
            self.ax.add_collection(
                PolyCollection(
                    [
                        [
                            [0, self.channel_list.index(channel)],
                            [TIME_LENGTH, self.channel_list.index(channel)],
                            [TIME_LENGTH, self.channel_list.index(channel) + 1],
                            [0, self.channel_list.index(channel) + 1],
                        ]
                    ],
                    facecolor=(0.8, 0.8, 1),
                    edgecolor=(0, 0, 0),
                    linewidth=0.5,
                ),
            )


class app(tk.Tk):
    def __init__(self):
        super().__init__()
        self.bind("<Configure>", self.resize)
        self.wm_title("2G")
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nesw")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.button = tk.Button(self, text="Click Me", command=self.change_band)
        self.button.grid(row=1, column=1, sticky="nesw")
        self.graph_noise = Graph_noise(self, title="2G")
        self.graph_noise.grid(row=0, column=0, sticky="nesw")

    def change_band(self):
        global current_band
        # switch graph showing band 2g <-> 5g
        if current_band == "2G":
            self.wm_title("5G")
            current_band = "5G"
        else:
            self.wm_title("2G")
            current_band = "2G"

    def resize(self, event):
        global window_width, window_height
        if event.widget.master != None:
            return
        window_height = event.height
        window_width = event.width

    def update_data(self, noise, txop, chanspec):
        self.graph_noise.update_noise(noise, "2G", True)
