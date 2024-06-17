import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.collections import PolyCollection
import sys
import numpy as np
import random
import time


class Graph(tk.Frame):
    def __init__(self, master: tk.Frame = None):
        super().__init__(master)
        self.master = master
        self.ax = plt.gca()
        master.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.update()

    def closeWindow(self):
        sys.exit()

    def update_data(self):
        self.ax.clear()
        self.ax.add_collection(
            PolyCollection(
                [[[0, 0], [1, 0], [0, 1]]],
                facecolor=(1, 0, 0),
                edgecolor=(0, 0, 0),
                linewidth=1,
            ),
        )
        self.ax.add_collection(
            PolyCollection(
                [[[1, 0], [1, 1], [0, 1]]],
                facecolor=(0, 1, 0),
                edgecolor=(0, 0, 0),
                linewidth=1,
            ),
        )
        self.ax.set_xlim([0, 36])
        self.ax.set_ylim([0, 10])
        plt.show()


root = tk.Tk()
app = Graph(master=root)
while True:
    app.update_data()
    app.update()
    time.sleep(1)

app.mainloop()
