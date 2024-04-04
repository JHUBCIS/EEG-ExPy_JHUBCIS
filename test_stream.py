import os
from eegnb import generate_save_fn
from eegnb.devices.eeg import EEG

board_name = "unicorn"
experiment = "stream test"
subject_id = 0
session_nb = 0

# Create save file name
save_fn = generate_save_fn(board_name, experiment, subject_id, session_nb)

# define the name for the board you are using and call the EEG object
eeg = EEG(device='unicorn')

# start the stream
eeg.start_stream(save_fn)

# while True:
#     eeg_cur = eeg.get_recent(1)
#     print(eeg_cur)
