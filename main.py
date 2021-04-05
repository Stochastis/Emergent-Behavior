import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter

xpoints = [1, 2, -1]
ypoints = [2, 4, -2]


def main():
    ani = animation.FuncAnimation(plt, animate())


def plot():
    for i in range(0, len(xpoints)):
        plt.scatter(xpoints[i], ypoints[i])
    return plt


def animate():
    for i in range(0, len(xpoints)):
        xpoints[i] = xpoints[i] + 1


if __name__ == "__main__":
    main()
