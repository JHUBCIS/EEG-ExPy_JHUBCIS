from CCA import CCAClassifier

# Load the data 
data_path = '/Users/malcolmkrolick/Documents/GitHub/EEG-ExPy_JHUBCIS/data/cca_eeg_1.csv'
channels = ["z_filt","PO7_filt","Oz_filt","PO8_filt"]


classifier = CCAClassifier(data_path, channels)



