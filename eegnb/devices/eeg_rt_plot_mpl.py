# eeg_rt_plot_mpl.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class EEGRealTimePlotMPL:
    def __init__(self, rolling_buffer, channel_names=None):
        self.rolling_buffer = rolling_buffer
        self.channel_names = channel_names if channel_names else [f'Ch{i+1}' for i in range(self.rolling_buffer.num_channels)]
        self.fig, self.axs = plt.subplots(self.rolling_buffer.num_channels, 1, figsize=(10, 8), sharex=True)
        
        # Initialize lines for updating data
        self.lines = []
        for ax, name in zip(self.axs, self.channel_names):
            ax.set_ylabel(name)
            line, = ax.plot([], [])  # Initialize empty line
            self.lines.append(line)

    def update_plot(self, frame):
        data = self.rolling_buffer.get_data()
        for i, line in enumerate(self.lines):
            line.set_data(np.arange(data[i].size), data[i])
            self.axs[i].relim()  # Recompute the data limits
            self.axs[i].autoscale_view()  # Rescale the view
        return self.lines

    def animate(self):
        self.anim = FuncAnimation(self.fig, self.update_plot, interval=100, blit=True, cache_frame_data=False)
        plt.show()
