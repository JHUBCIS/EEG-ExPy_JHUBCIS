# EEG-ExPy_JHUBCIS

See the original [EEG-ExPy](https://github.com/NeuroTechX/EEG-ExPy) Github page, the [NTX documentation](https://neurotechx.github.io/EEG-ExPy/) page, as well as the the `doc` directory in this repo for main documentations. This readme is compiled by JHUBCIS as an addition to the original documentation.

## Installation

Unless you would like to update the repository, it is recommended to download the repo as a zip file, unpack to a local directory, and run the repo in a `conda` virtual environment with [miniconda](https://docs.anaconda.com/free/miniconda/). Python 3.9.19 should work. To create a named `conda` virtual environment in command line and set it up with all the dependencies, try:

```powershell
cd "[your local directory]\EEG-ExPy_JHUBCIS"

conda create -n "eeg-expy-py3.9" python=3.9 

conda activate "eeg-expy-py3.9"

pip install -r requirements.txt
```

Note that you should replace `[your local directory]` with the directory of where you have actually unpacked the zip file.

The [Unicorn Suite](https://www.gtec.at/product/unicorn-suite/) software is recomended to run this repo with the [Unicorn Hybrid Black](https://www.gtec.at/product/unicorn-hybrid-black/) headset, which only runs on Windows. 🥲

Please refer to the [unicorn-bi](https://github.com/unicorn-bi) Github page by g.tec for more resources and documentation.

Note that the original EEG-ExPy repo is also compatible with many other EEG headsets that are compatible with other operating systems. The EEG-ExPy_JHUBCIS repo may be further updated so that the custom code added by JHUBCIS may be compatible with other EEG headsets supported by the original EEG-ExPy repo.

## Connecting to Unicorn Hybrid Black

To ensure the Unicorn Hybrid Black headset is connected and has good signal quality, it is suggested to use the Unicorn Suite software to vefiry.

To connect for the first time, make sure to activate Unicron Suite using the lisence information provided with your Unicorn Hybrid Black headset. Go to *Unicorn Suite Hybrid Black > Lisences > Add Lisence* and enter the information.

On how to use the Unicorn Suite software to establish connection, you may refer to the [Unicorn Suite Hybrid Black User Manual](https://github.com/unicorn-bi/Unicorn-Suite-Hybrid-Black-User-Manual) on Github or [UnicornSuite.pdf](.\UnicornSuite.pdf) in this repo. Note that the pdf is only the documentation for Unicorn Suite 1.18.00.

However, we have noticed that not every step in the manual is necessary. Often the following steps would be sufficient:

1. insert the bluetooth dongle to your Windows pc
2. Go to *Unicorn Suite Hybrid Black > My Unicorn* and click on the serial number of the headset you want to conect to in the middle panel
3. The headset should be properly connected when it shows up on the third panel in that page

Once the headset is connected, help the user put it on ([here&#39;s a video guide](https://www.youtube.com/watch?v=UVVUJTwvGnw)), and go to Unicorn Recorder or Unicorn Bandpower to test the signal quality.

- After either app is booted, on the right end of the window there will be an icon of the brain with circular cues to indicate the signal quality from each electrode. Green for good, yellow for moderate, and red for bad.

after all setup is complete and signal quality is checked to be good, make sure to close the Unicorn Suite software so that you may access the headset from the code in the repo.

## Streaming from Unicorn Hybrid Black

Run the [run_stream.py](./run_stream.py) in the python virtual environment created for the repo.

The `stream_plot()` function is defined in [eegnb/devices/eeg.py](eegnb/devices/eeg.py), with custom components from [eeg_rt_plot_mpl.py](eegnb\devices\eeg_rt_plot_mpl.py), [rolling_buffer.py](eegnb\devices\rolling_buffer.py), and [EMA_Filters.py](eegnb\devices\EMA_Filters.py). The function allows streaming filtered (bandpass and notch) EEG electrode data from the Unicorn Hybrid Black headset, and saving the streamed data.

First press 'q' to stop stream and save data, then close plot window to end program.

## Running the VisualSSVEP_select Experiment on Unicorn Hybrid Black

Run the [run_experiment.py](./run_expriment.py) in the python virtual environment created for the repo. This is a template that can also be used to run other experiemnts, but is currently set to run the [VisualSSVEP_select](eegnb\experiments\visual_ssvep\ssvep_select.py) Experiment. You may specify `subject_id`, `session_nb`, and `record_duration` as you like.

The experiment collects filtered (bandpass and notch) EEG data while the subject may choose to focus their visual attention on one of the two visual stimuli is the left and right corners of the screen. You may specify the flashing frequency of the left and right stimuli with the `freq1` and `freq2` parameters respectively. See [Multi-frequency steady-state visual evoked potential dataset](https://www.nature.com/articles/s41597-023-02841-5) on how to choose these values.

After the experiment is done, please use the [ssvep_select-clean_data.ipynb](eegnb\experiments\visual_ssvep\ssvep_select-clean_data.ipynb) to clean up the formatting.
