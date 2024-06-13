import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import sosfilt, butter
from sklearn.cross_decomposition import CCA
from scipy.special import expit


class CCAClassifier():

    def __init__(self, path, channel_names, ground_truth_channel, sliding_window_size=5): 
        self.path = path
        self.channel_names = channel_names
        self.num_channels = len(channel_names)
        self.ground_truth_channel = ground_truth_channel

        self.full_channels = self.load_data()[self.channel_names]
        self.sliding_window_size = sliding_window_size

        self.seven_hz_threshold = 0.5
        self.twentyone_hz_threshold = 0.2

    # Load the data
    def load_data(self):
        data = pd.read_csv(self.path)
        data = data[self.channel_names]
        return data
    
    def load_channel(self, channel_name):
        return pd.read_csv(self.path)[channel_name]
    
    def process_data(self):

        seven_hz_scores_list = []
        twenty_one_hz_scores_list = []

        # Generate 5 value subsections of code
        for i in range(0, self.full_channels.shape[0], self.sliding_window_size):
            #if (i + self.sliding_window_size < self.full_channels.shape[0]):
            self.channels = self.full_channels[i:i+self.sliding_window_size]
            seven_hz_scores, twenty_one_hz_scores = self.preprocess_segment()
            #print("7hz scores: ", seven_hz_scores)
            #print("21hz scores: ", twenty_one_hz_scores)

            seven_hz_scores_list.append(seven_hz_scores)
            twenty_one_hz_scores_list.append(twenty_one_hz_scores)

        return seven_hz_scores_list, twenty_one_hz_scores_list
    
    def get_treshold_preds(self, seven_hz_scores_list, twenty_one_hz_scores_list):
        seven_hz_scores = np.array(seven_hz_scores_list)
        twenty_one_hz_scores = np.array(twenty_one_hz_scores_list)

        
        combined_scores = np.array([seven_hz_scores, twenty_one_hz_scores]).reshape(2, -1)
        predicted_scores = []

        for score in combined_scores:
            predicted_scores.append(1 if (expit(score[0]) - expit(score[1]))/2  > 0 else 2)
            




        # accuracy_seven_hz = [x for x in seven_hz_scores if x > self.seven_hz_threshold]
        # accuracy_twenty_hz = [x for x in twenty_one_hz_scores if x > self.twentyone_hz_threshold]

        return predicted_scores
    
    def get_accuracy(self):
        seven_hz_scores_list, twenty_one_hz_scores_list = self.process_data()
        predicted_score = self.get_treshold_preds(seven_hz_scores_list, twenty_one_hz_scores_list)

        truth = self.load_channel(self.ground_truth_channel)

        filter_7hz = truth == 1 or truth == 2

        ground_truth = self.full_channels[filter]

        accuracy = 0

        for val in zip(ground_truth, predicted_score):
            if (val[0] == 0):
                continue
            else:
                if val[0] == val[1]:
                    accuracy += 1


        accuracy = accuracy / len(ground_truth)

        return accuracy




    


    # Returns the 7hz and the 21hz scores
    def preprocess_segment(self):

        channel_signals = self.channels[self.channel_names].values.T

        # figure out time duration between each sample
        python_time_channel = channel_signals[0]
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

        # DONE
        for channel_num, hz_channel in enumerate([seven_hz_signal, twentyone_hz_signal]):
            for channel in channel_signals:
                cca = CCA(n_components=1)
                cca.fit(channel.reshape(-1, 1), hz_channel.reshape(-1, 1))
                
                if (channel_num == 0):
                    seven_hz_scores.append(cca.score(channel.reshape(-1, 1), hz_channel.reshape(-1, 1)))
                else:
                    twenty_one_hz_scores.append(cca.score(channel.reshape(-1, 1), hz_channel.reshape(-1, 1)))

        return seven_hz_scores, twenty_one_hz_scores




