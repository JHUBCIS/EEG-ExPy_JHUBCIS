# Imports
import os
from eegnb import generate_save_fn
from eegnb.devices.eeg import EEG
from eegnb.experiments.visual_n170 import n170
from eegnb.analysis.utils import load_data

# Define some variables
board_name = 'muse'
# board_name = 'cyton'
experiment = 'visual_n170'
session = 999
subject = 999 # a 'very British number'
record_duration=120

# Initiate EEG device
eeg_device = EEG(device=board_name)

# Create output filename
save_fn = generate_save_fn(board_name, experiment, subject)

# Run experiment
n170.present(duration=record_duration, eeg=eeg_device, save_fn=save_fn)

# Load recorded data
raw = load_data(subject, session, board_names, experiment)