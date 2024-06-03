import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import sys


class Graph(tk.Frame):
    def __init__(self, master: tk.Frame = None):
        super().__init__(master)
        self.master = master
        self.fig, self.ax = plt.subplots(2, 2, figsize=(8, 6))
        self.ax[0][0].plot([1, 1.4, 3.5, 4], [1, 4, 9, 16])
        self.canvas = FigureCanvasTkAgg(self.fig, root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.toolbar = NavigationToolbar2Tk(self.canvas, root)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        master.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.update()

    def closeWindow(self):
        sys.exit()

    def update_data(self, target, data):
        self.ax[target[0]][target[1]].clear()
        self.ax[target[0]][target[1]].plot([1, 2, 3.5, 4], [1, 4, 9, 16])


root = tk.Tk()
app = Graph(master=root)
app.mainloop()
