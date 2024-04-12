
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


class VisualSSVEP(Experiment.BaseExperiment):

    def __init__(self, duration=120, eeg: Optional[EEG]=None, save_fn=None, freq1 = 10, freq2 = 50, n_trials = 1, iti = 0, soa = 120.0, jitter = 0): # iti = 0 makes the stimuli constant throughout. soa does not matter.
        
        exp_name = "Visual SSVEP"
        super().__init__(exp_name, duration, eeg, save_fn, n_trials, iti, soa, jitter)

        self.freq1 = freq1
        self.freq2 = freq2

    def load_stimulus(self):
        
        pattern = np.ones((4, 4))
        pattern[::2, ::2] *= -1
        pattern[1::2, 1::2] *= -1
        self._stim1 = visual.RadialStim(win=self.window, tex=pattern, pos=[18, -5],
                                        size=8, radialCycles=2, texRes=256, opacity=1)  
        self._stim2 = visual.RadialStim(win=self.window, tex=pattern*(-1), pos=[-18, -5],
                                        size=8, radialCycles=1, texRes=256, opacity=1)
        # fixation = visual.GratingStim(win=self.window, size=0.2, pos=[0, 0], sf=0.2, color=[1, 0, 0], autoDraw=True)

        # Generate the possible ssvep frequencies based on monitor refresh rate
        def get_possible_ssvep_freqs(frame_rate, stim_type="single"):
            
            max_period_nb = int(frame_rate / 6)
            periods = np.arange(max_period_nb) + 1
            
            if stim_type == "single":
                freqs = dict()
                for p1 in periods:
                    for p2 in periods:
                        f = frame_rate / (p1 + p2)
                        try:
                            freqs[f].append((p1, p2))
                        except:
                            freqs[f] = [(p1, p2)]

            elif stim_type == "reversal":
                freqs = {frame_rate / p: [(p, p)] for p in periods[::-1]}

            return freqs

        def init_flicker_stim(frame_rate, cycle, soa):
            
            if isinstance(cycle, tuple):
                stim_freq = int (frame_rate / sum(cycle))
                n_cycles = int(soa * stim_freq)
            
            else:
                stim_freq = int(frame_rate / cycle)
                cycle = (int(cycle), int(cycle))
                n_cycles = int((soa * stim_freq) / 2)

            return {"cycle": cycle, "freq": stim_freq, "n_cycles": n_cycles}

        # Set up stimuli
        frame_rate = np.round(self.window.getActualFrameRate())  # Frame rate, in Hz
        freqs = get_possible_ssvep_freqs(frame_rate, stim_type="reversal")
        cycle1 = int(frame_rate/self.freq1)
        cycle2 = int(frame_rate/self.freq2)
        self.stim_patterns = [
        init_flicker_stim(frame_rate, cycle1, self.soa),
        init_flicker_stim(frame_rate, cycle2, self.soa),
        ]
        
        print(
            (
                "\nFlickering frequencies (Hz): {}\n".format(
                    [self.stim_patterns[0]["freq"], self.stim_patterns[1]["freq"]]
                )
            )
        )


        return [
            init_flicker_stim(frame_rate, cycle1, self.soa),
            init_flicker_stim(frame_rate, cycle2, self.soa),
        ]

    def present_stimulus(self, idx, trial):
        
        # Select stimulus frequency
        ind = self.trials["parameter"].iloc[idx]

        # Push sample
        # replace with pushing dependent on key input
        # if self.eeg:
        #     timestamp = time()
        #     if self.eeg.backend == "muselsl":
        #         marker = [self.markernames[ind]]
        #     else:
        #         marker = self.markernames[ind]
        #     self.eeg.push_sample(marker=marker, timestamp=timestamp)

        # Present flickering stim
        # for _ in range(int(self.stim_patterns[ind]["n_cycles"])):
        #     self._stim1.setAutoDraw(True)
        #     for _ in range(int(self.stim_patterns[ind]["cycle"][0])):
        #         self.window.flip()
        #     self._stim1.setAutoDraw(False)
        #     self._stim2.setAutoDraw(True)
        #     for _ in range(self.stim_patterns[ind]["cycle"][1]):
        #         self.window.flip()
        #     self._stim2.setAutoDraw(False)
        # pass

            # Number of frames to run the loop for the longer of the two cycles
        # Example adjustment if self.stim_patterns contains cycle counts for multiple stimuli
        max_cycles = max([pattern["n_cycles"] for pattern in self.stim_patterns])

        
        # Separate cycle counts for each stimulus
        cycle1_frames = self.stim_patterns[ind]["cycle"][0]
        cycle2_frames = self.stim_patterns[ind]["cycle"][1]

        # Frame counters for each stimulus
        frame_counter1 = 0
        frame_counter2 = 0

        # Run the loop for the maximum number of cycles
        for _ in range(max_cycles):
            if frame_counter1 < cycle1_frames:
                self._stim1.setAutoDraw(True)
            else:
                self._stim1.setAutoDraw(False)

            if frame_counter2 < cycle2_frames:
                self._stim2.setAutoDraw(True)
            else:
                self._stim2.setAutoDraw(False)

            # Increment frame counters
            frame_counter1 = (frame_counter1 + 1) % (2 * cycle1_frames)
            frame_counter2 = (frame_counter2 + 1) % (2 * cycle2_frames)

            # Flip the window to update the display
            self.window.flip()

        # Ensure both stimuli are turned off after flashing
        self._stim1.setAutoDraw(False)
        self._stim2.setAutoDraw(False)
        self.window.flip()