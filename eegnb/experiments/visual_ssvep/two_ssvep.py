
from eegnb.experiments import Experiment
import os
from time import time
from glob import glob
from random import choice

import numpy as np
from pandas import DataFrame
from psychopy import visual, core, event


from eegnb.devices.eeg import EEG
from eegnb import generate_save_fn
from typing import Optional

class CheckerBoard:
    """Flickering radial checkerboard stimulation"""

    def __init__(self, window, size, position, n_frame, log_time=False):
        """
        Args:
            window (psychopy.visual.window): Psychopy window
            size (int): Size of the checkerboard stimulation
            position (tuple): Position of stimulation on the screen
            n_frame (int): Number of frames for the stim to flicker (frequency = monitor_refresh_rate/n_frame)
            log_time (bool): Whether to log toggle times
        """
        self._window = window
        self._fr_rate = n_frame
        self._fr_counter = n_frame
        pattern = np.ones((4, 4))
        pattern[::2, ::2] *= -1
        pattern[1::2, 1::2] *= -1
        self._stim1 = visual.RadialStim(win=self._window, tex=pattern, pos=position,
                                        size=size, radialCycles=1, texRes=256, opacity=1)
        self._stim2 = visual.RadialStim(win=self._window, tex=pattern*(-1), pos=position,
                                        size=size, radialCycles=1, texRes=256, opacity=1)
        self.log_time = log_time
        self.toggle_times = []

    def draw(self):
        """Draw stimulation"""
        self._stim1.draw()  
        self._stim2.draw()  


    def get_statistics(self):
        """Get stimulation toggle statistics
        Returns:
            mean and standard deviation of the stimulation time length (in case log_time is False returns None)
        """
        assert self.log_time, "Time logging has not been activated for this checkerboard."
        if self.log_time:
            diff_t = np.diff(np.array(self.toggle_times))
            return diff_t.mean(), diff_t.std()
        
        
class VisualSSVEPTwo(Experiment.BaseExperiment):

    def __init__(self, duration=120, eeg: Optional[EEG]=None, save_fn=None, n_trials = 2010, iti = 0.5, soa = 3.0, jitter = 0.2):
        
        exp_name = "Visual SSVEP"
        super().__init__(exp_name, duration, eeg, save_fn, n_trials, iti, soa, jitter)

    def load_stimulus(self):
        stim_size = 8  # Size of the checkerboard stimulation
        positions = [(18, -5), (-18, -5)]  # Positions of stimulation on the screen
        frame_rates = [15, 50]  # Number of frames for each stim to flicker

        self.targets = []
        for pos, fr_rate in zip(positions, frame_rates):
            self.targets.append(CheckerBoard(window=self.window, size=stim_size, position=pos, n_frame=fr_rate, log_time=True))

        return self.targets

    def present_stimulus(self, idx, trial):
        
        # Select stimulus frequency
        ind = self.trials["parameter"].iloc[idx]

        # Push sample
        if self.eeg:
            timestamp = time()
            
            marker = self.markernames[ind]
            self.eeg.push_sample(marker=marker, timestamp=timestamp)

        # Present checkerboard stim
        for target in self.targets:
            target.draw()
            #self.window.flip()