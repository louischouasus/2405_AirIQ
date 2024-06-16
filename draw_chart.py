import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import sys
import numpy as np
import random
import time


class Graph(tk.Frame):
    def __init__(self, master: tk.Frame = None):
        super().__init__(master)
        self.master = master
        self.fig, self.ax = plt.subplots(2, 2, figsize=(8, 6))
        self.ax[0][0].plot([1, 1.4, 3.5, 4], [1, 4, 9, 16])
        x = np.array(["A", "B", "C", "D"])
        y = np.array([12, 22, 6, 18])
        self.ax[1][1].bar(x, y, color=["#4CAF50", "red", "hotpink", "#556B2F"])
        self.canvas = FigureCanvasTkAgg(self.fig, root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.toolbar = NavigationToolbar2Tk(self.canvas, root)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        master.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.update()
        self.data = [10]

    def closeWindow(self):
        sys.exit()

    def update_data(self):
        self.data.append(self.data[-1] + random.randint(-3, 3))
        self.ax[0][1].clear()
        self.ax[0][1].plot([i for i in range(len(self.data))], self.data)


root = tk.Tk()
app = Graph(master=root)
while True:
    app.update_data()
    app.update()
    app.canvas.draw()
    time.sleep(1)

app.mainloop()
