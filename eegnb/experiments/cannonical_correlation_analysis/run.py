from CCA import CCAClassifier

# Load the data 
data_path = '~/projects/EEG-ExPy_JHUBCIS/data/cca_eeg_1.csv'
channels = ["PO7_filt","Oz_filt","PO8_filt"]


classifier = CCAClassifier(data_path, channels).process_data()

# Print the results
print("7hz scores: ", classifier[0])



