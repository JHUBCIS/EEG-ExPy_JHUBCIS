from CCA import CCAClassifier
import numpy as np

# Load the data 
data_path = '/Users/malcolmkrolick/Documents/GitHub/EEG-ExPy_JHUBCIS/data/what.csv'
channels = ["PO7_filt","Oz_filt","PO8_filt"]


classifier = CCAClassifier(data_path, channels, "filled_stim")

# Print the results
print("7hz scores: ", classifier.get_accuracy())



