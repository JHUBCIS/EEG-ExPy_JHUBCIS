"""
ssvep run experiment
===============================

This example demonstrates the initiation of an EEG stream with eeg-expy, and how to run 
an experiment. 

"""

###################################################################################################  
# Setup
# ---------------------  
#  
# Imports
from eegnb import generate_save_fn
from eegnb.devices.eeg import EEG
# from eegnb.experiments import VisualN170
from eegnb.experiments.visual_ssvep.ssvep_new import VisualSSVEP

# Define some variables
board_name = "unicorn" # board name
experiment_name = "ssvep" # experiment name
subject_id = 0 # test subject id
session_nb = 0 # session number
record_duration = 120 # recording duration

# generate save path
save_fn = generate_save_fn(board_name, experiment_name, subject_id, session_nb)

# create device object
# eeg_device = EEG(device=board_name)

# Experiment type
experiment = VisualSSVEP(duration=record_duration, eeg=None, save_fn=save_fn, freq1 = 1, freq2 = 20, n_trials = 1, iti = 0, soa = 120.0, jitter = 0)

###################################################################################################  
# Run experiment
# ---------------------  
#
experiment.run()

# Saved csv location
print("Recording saved in", experiment.save_fn)
