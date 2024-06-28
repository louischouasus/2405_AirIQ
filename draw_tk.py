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


current_band = "2G"


class Graph(tk.Frame):
    def __init__(self, master=None, title="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.fig = Figure(figsize=(4, 3))
        ax = self.fig.add_subplot(111)
        df = pd.DataFrame({"values": np.random.randint(0, 50, 10)})  # dummy data
        df.plot(ax=ax)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        tk.Label(self, text=f"Graph {title}").grid(row=0)
        self.canvas.get_tk_widget().grid(row=1, sticky="nesw")
        toolbar_frame = tk.Frame(self)
        toolbar_frame.grid(row=2, sticky="ew")
        NavigationToolbar2Tk(self.canvas, toolbar_frame)


def change_band():
    global current_band
    # switch graph showing band 2g <-> 5g
    if current_band == "2G":
        root.wm_title("5G")
        show_5g()
        current_band = "5G"
    else:
        root.wm_title("2G")
        show_2g()
        current_band = "2G"


def show_2g():
    for num, i in enumerate(list("222")):
        Graph(root, title=i, width=200).grid(row=num // 2, column=num % 2)


def show_5g():
    for num, i in enumerate(list("555")):
        Graph(root, title=i, width=200).grid(row=num // 2, column=num % 2)


root = tk.Tk()
root.wm_title("2G")
show_2g()


text_box = tk.Text(root, width=50, height=10, wrap=tk.WORD)
text_box.delete(0.0, "end")
text_box.insert(0.0, "My message will be here.")
button = tk.Button(root, text="Click Me", command=change_band)
button.grid(row=1, column=1, sticky="nesw")

root.mainloop()

print("asdasd")
