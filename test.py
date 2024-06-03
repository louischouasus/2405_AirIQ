import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import numpy as np
import time, sys
import threading
import random

global win
global tempGraphLabel, tempData, runFlag
runFlag = True
tempData = []
now = 0


class tempGraph:
    def __init__(self, root: tk.Frame):
        global win
        self.root = root  # 主窗体
        self.canvas = tk.Canvas()  # 创建一块显示图形的画布
        self.figure = self.create_matplotlib()  # 返回matplotlib所画图形的figure对象
        self.showGraphIn(self.figure)  # 将figure显示在tkinter窗体上面
        win.bind("<Configure>", self.resize_figure)

    """生成fig"""

    def resize_figure(self, event):
        print("resize")

    def create_matplotlib(self):
        # 创建绘图对象f
        self.f = plt.figure(
            num=2, figsize=(16, 8), dpi=100, edgecolor="green", frameon=True
        )
        # 创建一副子图
        self.fig11 = plt.subplot(1, 1, 1)
        (self.line11,) = self.fig11.plot([], [])

        def setLabel(fig, title, titleColor="red"):
            fig.set_title(title + "temp", color=titleColor)  # 设置标题
            fig.set_xlabel("time")  # 设置x轴标签
            fig.set_ylabel("temp")  # 设置y轴标签

        setLabel(self.fig11, "1")
        # fig1.set_yticks([-1, -1 / 2, 0, 1 / 2, 1])  # 设置坐标轴刻度
        self.f.tight_layout()  # 自动紧凑布局
        return self.f

    """把fig显示到tkinter"""

    def showGraphIn(self, figure):
        # 把绘制的图形显示到tkinter窗口上
        self.canvas = FigureCanvasTkAgg(figure, self.root)
        self.canvas.draw()  # 以前的版本使用show()方法，matplotlib 2.2之后不再推荐show（）用draw代替，但是用show不会报错，会显示警告
        self.canvas.get_tk_widget().pack(side=tk.TOP)  # , fill=tk.BOTH, expand=1

        # 把matplotlib绘制图形的导航工具栏显示到tkinter窗口上
        toolbar = NavigationToolbar2Tk(
            self.canvas, self.root
        )  # matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    """更新fig"""

    def updateMeltGraph(self, meltData):
        x = [i for i in range(len(meltData))]
        self.line11.set_xdata(x)  # x轴也必须更新
        self.line11.set_ydata(meltData)  # 更新y轴数据
        #  更新x数据，但未更新绘图范围。当我把新数据放在绘图上时，它完全超出了范围。解决办法是增加：
        self.fig11.relim()
        self.fig11.autoscale_view()
        displayWidth = win.winfo_width()  # 获取屏幕宽度
        displayHeight = win.winfo_height()
        print(displayWidth, displayHeight)
        self.f.set_size_inches(
            displayWidth / self.figure.get_dpi(),
            displayHeight / self.figure.get_dpi(),
            forward=True,
        )
        plt.draw()
        # self.canvas.draw_idle()


"""
更新数据，在次线程中运行
"""


def updataData():
    global tempData, runFlag, now
    while runFlag:
        now += random.randint(-3, 3)
        tempData.append(now)
        time.sleep(1)


"""
更新窗口
"""


def updateWindow():
    global win
    global tempGraphLabel, tempData, runFlag
    if runFlag:
        if len(tempData) > 100:
            tempGraphLabel.updateMeltGraph(
                tempData[len(tempData) - 100 : len(tempData)]
            )
        else:
            tempGraphLabel.updateMeltGraph(tempData)
    win.after(1000, updateWindow)  # 1000ms更新画布


"""
关闭窗口触发函数，关闭S7连接，置位flag
"""


def closeWindow():
    global runFlag
    runFlag = False
    sys.exit()


"""
创建控件
"""


def createGUI():
    global win
    win = tk.Tk()
    displayWidth = win.winfo_screenwidth()  # 获取屏幕宽度
    displayHeight = win.winfo_screenheight()
    winWidth, winHeight = displayWidth, displayHeight - 70
    winX, winY = -8, 0
    # winX, winY = int((displayWidth - winWidth) /
    #                  2), int((displayHeight - winHeight - 70) / 2)
    win.title("title")

    # win.resizable(0, 0) # 不使能最大化
    win.protocol("WM_DELETE_WINDOW", closeWindow)
    # win.iconbitmap(r'resource/images/motor.ico')  # 窗口图标

    graphFrame = tk.Frame(win)  # 创建图表控件
    graphFrame.place(x=0, y=0)
    global tempGraphLabel
    tempGraphLabel = tempGraph(graphFrame)

    recv_data = threading.Thread(target=updataData)  # 开启线程
    recv_data.start()

    updateWindow()  # 更新画布
    win.mainloop()


if __name__ == "__main__":
    createGUI()
