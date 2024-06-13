import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import sosfilt, butter
from sklearn.cross_decomposition import CCA


class CCAClassifier():

    def __init__(self, path, channel_names): 
        self.path = path
        self.channel_names = channel_names
        self.num_channels = len(channel_names)

        self.full_channels = self.load_data()[self.channel_names]

    # Load the data
    def load_data(self):
        data = pd.read_csv(self.path)
        data = data[self.channel_names]
        return data
    
    def process_data(self):

        seven_hz_scores = []
        twenty_one_hz_scores = []

        # Generate 5 value subsections of code
        for i in range(0, self.channels.shape[0], 5):
            if (i + 5 < self.channels.shape[0]):
                self.channels = self.full_channels[i:i+5]
                seven_hz_scores, twenty_one_hz_scores = self.preprocess_segment()
                #print("7hz scores: ", seven_hz_scores)
                #print("21hz scores: ", twenty_one_hz_scores)

                seven_hz_scores.append(seven_hz_scores)
                twenty_one_hz_scores.append(twenty_one_hz_scores)

        return seven_hz_scores, twenty_one_hz_scores

        

    # Returns the 7hz and the 21hz scores
    def preprocess_segment(self):

        channel_signals = [self.channels[:,x] for x in range(1, self.num_channels + 1)]

        # figure out time duration between each sample
        python_time_channel = self.channels[:,0]
        time_channel = [python_time_channel[x] - python_time_channel[x-1] for x in range(1, len(python_time_channel))]

        # average time duration
        avg_time = np.mean(time_channel)

        # above is average seconds per sample
        # number of avg time per second is
        avg_time_per_second = 1/avg_time

        # create duration of channels var
        duration = self.channels.shape[0]

        # create time array
        time_arr = np.arange(0, duration).astype(float)

        # goofy AAAA code -> probably could do wit linspace
        for i in range(time_arr.shape[0]):
            if (i == 0):
                time_arr[i] = 0
            else:
                time_arr[i] = time_arr[i-1] + avg_time


        # create a 7hz signal
        seven_hz_signal = np.sin(2 * np.pi * 7 * time_arr / avg_time_per_second)

        # create a 21hz signal
        twentyone_hz_signal = np.sin(2 * np.pi * 21 * time_arr / avg_time_per_second)


        # Generate scores for the 7hz & 21hz signal

        seven_hz_scores = []
        twenty_one_hz_scores = []


        for channel_num, hz_channel in enumerate([seven_hz_signal, twentyone_hz_signal]):
            for channel in channel_signals:
                cca = CCA(n_components=1)
                cca.fit(channel.reshape(-1, 1), hz_channel.reshape(-1, 1))
                
                if (channel_num == 0):
                    seven_hz_scores.append(cca.score(channel.reshape(-1, 1), hz_channel.reshape(-1, 1)))
                else:
                    twenty_one_hz_scores.append(cca.score(channel.reshape(-1, 1), hz_channel.reshape(-1, 1)))

        return seven_hz_scores, twenty_one_hz_scores




