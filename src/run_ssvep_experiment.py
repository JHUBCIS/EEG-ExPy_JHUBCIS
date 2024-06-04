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
from eegnb.experiments.visual_ssvep.ssvep_select import VisualSSVEP_select
from eegnb.experiments.visual_ssvep.ssvep import VisualSSVEP

# Define some variables
board_name = "unicorn" # board name
experiment_name = "ssvep" # experiment name
subject_id = 0 # test subject id
session_nb = 0 # session number
record_duration = 30  # recording duration in seconds

# generate save path
save_fn = generate_save_fn(board_name, experiment_name, subject_id, session_nb)

# create device object
eeg_device = EEG(device=board_name)

# Experiment type
# experiment = VisualSSVEP(duration=record_duration, eeg=eeg_device, save_fn=save_fn)
experiment = VisualSSVEP_select(duration=record_duration, eeg=eeg_device, save_fn=save_fn, freq1=15, freq2=55) #note that most laptops only support up to 60 Hz. don't go above that

###################################################################################################  
# Run experiment
# ---------------------  
#
experiment.run()

