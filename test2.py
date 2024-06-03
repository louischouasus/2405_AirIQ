import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class TkinterApp:
    def __init__(self, root: tk.Tk):
        self.master = root
        root.title("Resizable Matplotlib Figure")

        # Create the Matplotlib figure and axis
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.ax.plot([1, 2, 3, 4], [1, 4, 9, 16])

        # Create the Tkinter canvas and toolbar
        self.canvas = FigureCanvasTkAgg(self.fig, root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.toolbar = NavigationToolbar2Tk(self.canvas, root)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Bind the <Configure> event to the window to resize the figure
        root.bind("<Configure>", self.resize_figure)

    def resize_figure(self, event):
        print("Resizing figure...")
        # Get the new window size
        width = event.width
        height = event.height

        # Resize the figure to fit the new window size
        self.fig.set_size_inches(
            width / self.fig.get_dpi(), height / self.fig.get_dpi(), forward=True
        )

        # Redraw the canvas
        self.canvas.draw()


def main():

    root = tk.Tk()
    app = TkinterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
