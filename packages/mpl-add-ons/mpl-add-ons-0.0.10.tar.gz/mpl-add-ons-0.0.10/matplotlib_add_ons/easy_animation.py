import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class FigureAnimation:
    def __init__(self, figures, get_new_data_func, redraw=False, frames=100, interval=50):
        self.figures = figures
        self.get_new_data_func = get_new_data_func
        self.redraw = redraw
        self.frames = frames
        self.interval = interval
        self.animations = []
        self.animate()

    def update(self, frame):
        new_data = self.get_new_data_func(frame)

        for fig, data in zip(self.figures, new_data):
            ax = fig.gca()
            if self.redraw:
                ax.clear()
                x, y = data[0]
                ax.plot(x, y)
            else:
                for line, (x, y) in zip(ax.get_lines(), data):
                    line.set_xdata(x)
                    line.set_ydata(y)
        return ax.get_lines(),

    def animate(self):
        for fig in self.figures:
            self.animations.append(FuncAnimation(fig, self.update, frames=self.frames, interval=self.interval))

    def show(self):
        plt.show()


# Example usage:

def get_new_data(frame):
    data = []
    for _ in range(len(figures)):
        x = range(100)
        y = [xi ** 2 + frame * 10 for xi in x]
        data.append([(x, y)])
    return data


figures = []
for _ in range(3):  # Creating 3 figures
    fig, ax = plt.subplots()
    x = range(100)
    y = [xi ** 2 for xi in x]
    ax.plot(x, y)
    figures.append(fig)

animation = FigureAnimation(figures, get_new_data_func=get_new_data, redraw=True, interval=50)
animation.show()
