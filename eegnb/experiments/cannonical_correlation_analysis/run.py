from CCA import CCAClassifier
import numpy as np

# Load the data 
data_path = '/Users/malcolmkrolick/Documents/GitHub/EEG-ExPy_JHUBCIS/data/what.csv'
channels = ["PO7_filt","Oz_filt","PO8_filt"]

# Check arrays

#print(CCAClassifier(data_path, channels, "filled_stim").load_data().head())


classifier = CCAClassifier(data_path, channels, "filled_stim", sliding_window_size=50)

# Print the results
print("7hz scores: ", classifier.get_accuracy())



