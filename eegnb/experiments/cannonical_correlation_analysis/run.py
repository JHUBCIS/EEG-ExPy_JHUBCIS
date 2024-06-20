from CCA import CCAClassifier
import numpy as np

# Load the data 
data_path = '../../../data/what.csv'
channels = ["PO7_filt","Oz_filt","PO8_filt"]

# Check arrays

#print(CCAClassifier(data_path, channels, "filled_stim").load_data().head())


classifier = CCAClassifier(data_path, channels, "filled_stim", sliding_window_size=50)

# Print the results
print("Accuracy: ", classifier.get_accuracy())



