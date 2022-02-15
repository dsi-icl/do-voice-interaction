# Emotion Recognition Service

This repository was developed to provide an emotion detection feature to the DO voicebot.
The method was inspired by and built using [`Speech Emotion Recognition using Semantic Information`](https://arxiv.org/pdf/2103.02993.pdf) (ICASSP 2021) and the original code can be found ['here'](https://github.com/glam-imperial/semantic_speech_emotion_recognition).

## Requirements

Set up a virtual environment and install the below:
1. Python 3.7 (3.8 does not allow Tensorflow 1.4, which is required for this model).
2. Make sure ffmpeg, ffprobe and espeak are installed and available from the command line.


## Installing libraries (NO need to do this if you're running from Docker)
1. Run pip install -r requirements.txt
2. It is possible that you might run into an issue with Aeneas. In that case, install the below individually and do step 1 again. The order is important.
tensorflow==1.14.0 
tensorflow-gpu==1.14.0
numpy==1.18.5 
aeneas==1.7.3.0
3. If you are still experiencing an issue, check you have ffmpeg, ffprobe and espeak are installed and available from the command line.


## Preparation

### Obtain MuSe-CaR dataset
1. Request MuSe-CAR 2020 (in-the-wild) dataset.
2. Check that the folder structure matches the strcucture used for the code (check the report).
3. Place the MuSe-CAR folder in this directory.
Note) At the time of writing MuSe-CAR 2021 is already available, however the structure/ number of samples may not match the current codebase.

### Get all necessary binaries
1. Download the binaries ['here'](https://imperialcollegelondon.box.com/s/wzqo3zm3v4kcvrukyli5gdw3gx7uiklw).
2. Place them all in this folder.


## Steps for Preprocessing/Training/Evluation

### Synchronisation mapping
Run synchronisation_map_generator.py to generate synchromisation mapping (csv) of the transcript words to time stamp of when the word is played in the corresponding audio file.

### Preprocess labels
Run label_generator.py to preprocess labels to condense the separately provided arousal and valence data (into timestamp/arousal/valence).

### (optional) Design a new partition
This is needed if you do not want to to use the partition (check the report).
Run parition_generator.py
This takes the parition.csv file given by MuSe (this should be place in the MuSe-Car directory) and reads the current paritition and lists them in order. It then generates a new parition by taking the devel set, shuffles it and splits it into two parts: devel and test. MuSe only makes train and devel sets available and keeps test hidden for fair evaluation.
To analyse the feature distribution of the split, copy and paste the output (new parition) to label_distribution_analysis.py and run. This will output the distrbution curves across the three new sets (normalised and non-normalised).

### Generate Tfrecords
Run data_generator.py to create tfrecords that merges the synchronisation mapping (csv), labels (csv) and the actual audio frames from raw audio (wav).

### Training
Run train.py
If this is the first time running training, you will see a folder created called checkpoints.
The default parameters are the final hyperparameters used in the report.
You can also specify your own using the flags.
By default, the train session saves a checkpoint every 2 mins. This can be changed using SAVE_INTERVAL_SECS. These will save checkpoints that follows the namin convention 'model.ckpt-8188'. You will find that there are 3 files starting with this name. '8188' refers to the number of training steps at the time of saving the checkpoint - this value will be used when running the evaluation. You can also change how often you want to calculate the summary via SAVE_SUMMARY_SECS.

By default train.py is GPU enabled, it can also be ran on non-GPU device with this setting, however the speed may be worse than if you were to disable GPU to begin with. To do disable GPU, set the flag --device -1

To see the training history (e.g. hyperparameters and settings) see log_train.txt.

### Evaluate
Run eval.py 
You must specify:
#### 1. portion (--portion)
Select either train, devel or test, which refer to the 3 directories in the tfrecords directory. The evaluation will be carried out on the selected portion only. Generally you want either devel or test for this.
#### 2. checkpoint directory (--checkpoint)
Specify the relative path to the directory that holds the checkpoints e.g. './checkpoint_final'.
#### 3. steps (--steps)
Specify the number of steps to pinpoint exactly which checkpoint file to use e.g. 8188 if the checkpoint name starts with 'model.ckpt-8188'.

By default train.py is GPU enabled, it can also be ran on non-GPU device with this setting, however the speed may be worse than if you were to disable GPU to begin with. To do disable GPU, set the flag --device -1

To see the evaluation history (e.g. portions and settings) see log_eval.txt.

### Terminal Outputs
During development, it may be useful to turn on develpment_msg(), which is used through out this codebase. Simply uncomment the line, print(content), in helper.py to see all the outputs. E.g. shapes of vectors, filenames currently being processed etc.

## Tips
For Mac, always have .DS_STORE files removed! Run find . -name ".DS_Store" -delete on the project directory to remove them in all subfolders.