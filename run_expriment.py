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
from eegnb.experiments.visual_ssvep.ssvep_select import VisualSSVEP_select
# from eegnb.experiments.visual_ssvep.ssvep import VisualSSVEP

# Define some variables
board_name = None # board dfname
experiment_name = "ssvep_select" # experiment name
subject_id = 0 # test subject id
session_nb = 0 # session number
record_duration = 120  # recording duration in seconds

# generate save path
save_fn = generate_save_fn(board_name, experiment_name, subject_id, session_nb)

# create device object
eeg_device = EEG(device=board_name)

# Experiment type
# experiment = VisualSSVEP(duration=record_duration, eeg=eeg_device, save_fn=save_fn)
'''for more details on which frequencies to select, see https://www.nature.com/articles/s41597-023-02841-5'''
experiment = VisualP300(duration=record_duration, eeg=eeg_device, save_fn=save_fn, freq1=7, freq2=23, bp_fc_high = 60, bp_fc_low = 1, n_fc = 60) #note that most laptops only support up to 60 Hz. don't go above that

###################################################################################################  
# Run experiment
# ---------------------  
#
experiment.run()

