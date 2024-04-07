# rolling_buffer.py
from collections import deque
import numpy as np

class RollingBuffer:
    def __init__(self, buffer_time=10, sfreq=250, num_channels=8):
        self.buffer_length = buffer_time * sfreq
        self.num_channels = num_channels
        self.buffer = deque(maxlen=self.buffer_length)
        
    def update(self, new_data):
        self.buffer.extend(new_data)
        
    def get_data(self):
        return np.array(self.buffer).T  # Transpose to make rows correspond to channels
