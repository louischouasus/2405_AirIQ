import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.animation import FuncAnimation
import sys
import numpy as np
import random
import parse_airiq
import time

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

TIME_LENGTH = 10


class Graph:
    def __init__(self):
        super().__init__()
        self.ax = plt.gca()
        plt.subplots_adjust(
            top=0.95, bottom=0.05, right=0.95, left=0.05, hspace=0, wspace=0
        )

    def closeWindow(self):
        sys.exit()

    def update_data(self, noise: dict[dict[list]], current_channel: list[int]):
        self.ax.clear()
        self.ax.set_yticks(range(len(channel_list)), channel_list, size="small")
        self.ax.set_ylim([0, len(channel_list)])
        self.ax.set_xlim([0, TIME_LENGTH])
        for channel in noise:
            self.add_non_wifi(channel, noise[channel]["non_wifi"][-TIME_LENGTH:])
            self.add_wifi(channel, noise[channel]["wifi"][-TIME_LENGTH:])
        plt.pause(1)

    def add_non_wifi(self, channel: int, value: list):
        channel_index = channel_list.index(int(channel))
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
        channel_index = channel_list.index(int(channel))
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

    def add_currenct_channel(self, current_channel: list[int]):
        # add a light blue rectangle to highlight the current channel
        for channel in current_channel:
            self.ax.add_collection(
                PolyCollection(
                    [
                        [
                            [0, channel_list.index(channel)],
                            [TIME_LENGTH, channel_list.index(channel)],
                            [TIME_LENGTH, channel_list.index(channel) + 1],
                            [0, channel_list.index(channel) + 1],
                        ]
                    ],
                    facecolor=(0.8, 0.8, 1),
                    edgecolor=(0, 0, 0),
                    linewidth=0.5,
                ),
            )
