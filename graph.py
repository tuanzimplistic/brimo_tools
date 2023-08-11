import numpy as np
import matplotlib.pyplot as plt
plt.ion()

class Plot():
    def on_launch(self):
        self.x_stirrer = []
        self.y_stirrer = []
        self.step_stirrer = 1000
        self.figure_stirrer, (self.ax_stirrer, self.ax_heater) = plt.subplots(2, 1)
        self.line_stirrer, = self.ax_stirrer.plot(self.x_stirrer, self.y_stirrer)
        self.ax_stirrer.set_xlim(0, self.step_stirrer)
        self.ax_stirrer.set_ylim(0, 3500)
        self.ax_stirrer.grid()

    def on_running(self, xdata, ydata):
        self.line_stirrer.set_xdata(xdata)
        self.line_stirrer.set_ydata(ydata)
        self.figure_stirrer.canvas.draw()
        self.figure_stirrer.canvas.flush_events()
        
    def update_stirrer(self, x, y):
        if x > self.step_stirrer:
            self.step_stirrer = 2*x
            self.ax_stirrer.set_xlim(x, self.step_stirrer)
            self.ax_stirrer.relim()
            self.ax_stirrer.autoscale_view()
        self.x_stirrer.append(x)
        self.y_stirrer.append(y)
        self.on_running(self.x_stirrer, self.y_stirrer)