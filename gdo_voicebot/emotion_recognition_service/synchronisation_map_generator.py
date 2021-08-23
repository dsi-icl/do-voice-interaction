import csv
import os
import sys
import time
from pathlib import Path
sys.path.append(".")

from aeneas.audiofile import AudioFile
from aeneas.exacttiming import TimeInterval, TimeValue
from aeneas.executetask import ExecuteTask
from aeneas.task import Task

from helper import get_pathlist_from_dir, development_msg, TRANSCRIPT_DIR, SYNCHRONISATION_MAPPING_DIR


''' GG
def execute_task(directory, filename):
    development_msg('****************** Entering execute_task() *******************')
    development_msg('directory = ' + directory)
    development_msg('filename = ' + filename)
    development_msg('Creating task object')
    # Create Task object
    config_string = u"task_language=deu|is_text_type=mplain|os_task_file_format=csv|os_task_file_levels=3"
    task = Task(config_string=config_string)
    task.audio_file_path_absolute = directory + filename + '.wav'
    task.text_file_path_absolute = directory + filename + '.txt'
    task.sync_map_file_path_absolute = "%s/%s.csv" % (SYNCHRONISATION_MAPPING_DIR, filename)
    development_msg('Processing task')
    # Process Task
    ExecuteTask(task).execute()
    development_msg('Output sync map to file')
    # output sync map to file
    task.output_sync_map_file()


def trim_audio(audio_file, sent, time_to_shift):
    development_msg('****************** Entering trim_audio() *******************')
    development_msg('audio_file = ' + audio_file)
    development_msg('sent = ' + str(sent))
    audio = AudioFile(file_path=AUDIO_DIR + audio_file + '.wav')
    audio.read_properties()
    audio.read_samples_from_file()
    
    # Extract sentence information
    start, end, transcript = sent
    start = int(start) - int(time_to_shift) # actual start time relative to audio segment XX_XX.wav
    end = int(end) - int(time_to_shift)
    start = format((start/1000), '.4f') # convert micro second to second and limit to 4 decimal places
    end = format((end/1000), '.4f')
    start = TimeValue(start) 
    end = TimeValue(end)
    time_interval = TimeInterval(start, end)
    development_msg('start = ' + str(start))
    development_msg('end = ' + str(end))
    development_msg('transcript = ' + transcript)
    development_msg('time_interval = ' + str(time_interval))

    # Trim audio by sentence
    audio.trim(begin=start, length=time_interval.length)
    assert audio.audio_length - time_interval.length < 0.001

    fo = audio_file + '_' + str(int(time.time()))
    audio.write(SYNCHRONISATION_MAPPING_DIR + fo + '.wav')

    with open(SYNCHRONISATION_MAPPING_DIR + fo + '.txt', 'w') as tmp_transcript:
        tmp_transcript.write(transcript)
    
    return fo


def load_transcript(filepath):
    with open(filepath, newline='') as csvfile:
        #reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        reader = csv.reader(csvfile)

        sentences = []
        for row in reader:
            development_msg(row)

            # skip the first line
            if row == ['start', 'end', 'segment_id', 'word']:
                continue

            #transcript = row[2].strip('\'')  # Strip '' at beginning & end
            transcript = row[3] # adjusted the field number to match the MuSe samples - mifu
            punctuation = '!"#$%&\'()*+,-./:;=?@[\\]^_`{|}~'  # Exclude <>
            transcript_clean = transcript.translate(str.maketrans('', '', punctuation))
            words = transcript_clean.lower().split()
            
            if transcript != '<filler>' and transcript_clean != '':
                sentences.append([row[0], row[1], transcript_clean])
    development_msg('Successfully setences created')
    development_msg(sentences)
    return sentences
'''

def clean_word(word):
    word = word.lower()
    
    punctuation = '!"#$%&\'()*+,-./:;=?@[\\]^_`{|}~'  # Exclude <>
    word = word.translate(str.maketrans('', '', punctuation))
    
    return word

''' GG
def delete_segmentation(tmp):
    for ext in ['.wav', '.txt', '.csv']:
        os.remove(SYNCHRONISATION_MAPPING_DIR + tmp + ext)
'''

def mapping_generator():
    (Path(SYNCHRONISATION_MAPPING_DIR)).mkdir(exist_ok=True)

    clipfolders = get_pathlist_from_dir(TRANSCRIPT_DIR)
    development_msg('clip folders:\n')
    development_msg(clipfolders) # list of folders for different reviews
    for folder in clipfolders:
        clipname = folder.rsplit('/')[-1] # i.e. folder name e.g. 201
        print('Creating synchronisation map for ' + clipname + ' and saving in ' + SYNCHRONISATION_MAPPING_DIR)
        (Path(SYNCHRONISATION_MAPPING_DIR) / clipname).mkdir(exist_ok=True) # create a folder dedicated to this review if it does not exist already 
        
        segmentlist = get_pathlist_from_dir(TRANSCRIPT_DIR + clipname)
        development_msg('segment list:\n')
        development_msg(segmentlist)

        for sid, segment in enumerate(segmentlist):
            segmentname = segment.rsplit('/')[-1][:-4] # i.e. segment name e.g. 201_1
            
            fo = open(SYNCHRONISATION_MAPPING_DIR + clipname + '/' + segmentname + '.csv', 'w') # store the segment csv in the created folder
            print('Working on ' + segmentname)

            cnt = 1

            with open(segment) as tmp:
                for _, row in enumerate(csv.reader(tmp)):

                    # avoid unpacking rows from segment transcriptions files if it does not have 4 cols (start, end, id, word) as it will give an error when we attempt to unpack
                    if len(row) != 4:
                        print('Skipping segment ' + segmentname + ' entirely as the transcription does not contain exactly 4 cols (start, end, id, word)')
                        break # move onto the next segment e.g. 201_2 if there are no 4 items to unpack from row

                    start, end, id, word = row # the id here is useless but extract anyway

                    if _ == 0 or row == ['start', 'end', 'segment_id', 'word']:
                        continue # skip the field names
                    if _ == 1:
                        time_to_shift = start # save the first start time in this segment
                    
                    word = clean_word(word).lower()
                    
                    if word == '<filler>' or word == '':
                        continue # skip this row as it is empty

                    # adjust time
                    start = int(start) - int(time_to_shift) # adjust time to make it relative to the start of audio segment XX_XX.wav
                    end = int(end) - int(time_to_shift)
                    # convert to match SEWA time
                    start = format((start/1000), '.4f') # convert micro second to second and limit to 4 decimal places
                    end = format((end/1000), '.4f')

                    id = segmentname + 'w' + str(cnt) # new id
                    
                    new_row = ";".join([id, str(start), str(end), word])
                    fo.write(new_row + '\n')
                    cnt += 1 
            fo.close()

            if cnt == 1:
                # newly created csv is empty
                print('Removing ' + segmentname + ' as there were no mapping entry')
                os.remove(SYNCHRONISATION_MAPPING_DIR + clipname + '/' + segmentname + '.csv')


if __name__ == '__main__':
    mapping_generator()
