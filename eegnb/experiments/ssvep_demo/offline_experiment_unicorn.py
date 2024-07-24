# -*- coding: utf-8 -*-
"""
A script to run a simple offline SSVEP Experiment
"""
# import argparse
# import explorepy
from ssvep import SSVEPExperiment


def main():
    # parser = argparse.ArgumentParser(description="A script to run a simple SSVEP Experiment")
    # parser.add_argument("-n", "--name", dest="name", type=str, help="Name of the device.")
    # parser.add_argument("-f", "--filename", dest="filename", type=str, help="Record file name")
    # args = parser.parse_args()

    """
    Experiment Parameters
    """
    n_blocks = 20           # Number of blocks
    trials_per_block = 5    # Number of total trials = n_blocks * trials_per_block
    target_pos = [(-.8, 0), (.8, 0)]  # Positions of left and right targets
    hints = [u'\u2190', u'\u2192']  # Left arrow, Right arrow
    freqs = [9, 16] # Hz
    scr_rate = 144 # laptop screen refresh rate
    fr_rates = [scr_rate / freq for freq in freqs]

    # exp_device = explorepy.Explore()
    # exp_device.connect(device_name=args.name)
    # exp_device.record_data(file_name=args.filename, file_type='csv')
            

    experiment = SSVEPExperiment(frame_rates=fr_rates, positions=target_pos, hints=hints,
                                 trial_len=6, trials_per_block=trials_per_block, n_blocks=n_blocks,
                                 screen_refresh_rate=scr_rate,
                                 IP = "127.0.0.1", Port = 800
                                 )
    
    
    experiment.run()
    # exp_device.stop_recording()
    # exp_device.disconnect()


if __name__ == '__main__':
    main()
