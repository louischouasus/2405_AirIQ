import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.collections import PolyCollection
import sys
import numpy as np
import random
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

    def update_data(self, noise: dict[dict[list]]):
        self.ax.clear()
        self.ax.set_yticks(range(len(channel_list)), channel_list, size="small")
        self.ax.set_ylim([0, len(channel_list)])
        self.ax.set_xlim([0, TIME_LENGTH])

        plt.show()

    def add_non_wifi(self, channel: int, value: int, time: int):

        self.ax.add_collection(
            PolyCollection(
                [[[0, 0], [1, 0], [0, 1]]],
                facecolor=(1, 0, 0),
                edgecolor=(0, 0, 0),
                linewidth=1,
            ),
        )


app = Graph()
while True:
    app.update_data()
    time.sleep(1)

app.mainloop()
