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


def clean_word(word):
    word = word.lower()
    
    punctuation = '!"#$%&\'()*+,-./:;=?@[\\]^_`{|}~'  # Exclude <>
    word = word.translate(str.maketrans('', '', punctuation))
    
    return word


def mapping_generator():
    (Path(SYNCHRONISATION_MAPPING_DIR)).mkdir(exist_ok=True)

    clipfolders = get_pathlist_from_dir(TRANSCRIPT_DIR)
    development_msg('clip folders:\n')
    development_msg(clipfolders) # list of folders for different reviews
    for folder in clipfolders:
        clipname = folder.rsplit('/')[-1] # i.e. folder name e.g. 201
        print('Creating synchronisation map for ' + clipname + ' and saving in ' + SYNCHRONISATION_MAPPING_DIR)
        # create a folder dedicated to this review if it does not exist already 
        (Path(SYNCHRONISATION_MAPPING_DIR) / clipname).mkdir(exist_ok=True)
        
        segmentlist = get_pathlist_from_dir(TRANSCRIPT_DIR + clipname)
        development_msg('segment list:\n')
        development_msg(segmentlist)

        for sid, segment in enumerate(segmentlist):
            segmentname = segment.rsplit('/')[-1][:-4] # i.e. segment name e.g. 201_1
            
            # store the segment csv in the created folder
            fo = open(SYNCHRONISATION_MAPPING_DIR + clipname + '/' + segmentname + '.csv', 'w')
            print('Working on ' + segmentname)

            cnt = 1

            with open(segment) as tmp:
                for _, row in enumerate(csv.reader(tmp)):

                    # avoid unpacking rows from segment transcriptions files 
                    # if it does not have 4 cols (start, end, id, word) 
                    # as it will give an error when we attempt to unpack
                    if len(row) != 4:
                        print('Skipping segment ' + segmentname + ' entirely as the transcription does not contain exactly 4 cols (start, end, id, word)')
                        break # move onto the next segment e.g. 201_2 if there are no 4 items to unpack from row

                    start, end, id, word = row

                    if _ == 0 or row == ['start', 'end', 'segment_id', 'word']:
                        continue # skip the field names
                    if _ == 1:
                        # save the first start time in this segment
                        time_to_shift = start 
                    
                    word = clean_word(word).lower()
                    
                    # skip this row as it is empty
                    if word == '<filler>' or word == '':
                        continue

                    # adjust time to make it relative to the start of audio segment XX_XX.wav
                    start = int(start) - int(time_to_shift)
                    end = int(end) - int(time_to_shift)

                    # convert to match SEWA time
                    # convert micro second to second and limit to 4 decimal places
                    start = format((start/1000), '.4f')
                    end = format((end/1000), '.4f')

                    id = segmentname + 'w' + str(cnt) # new id
                    
                    new_row = ";".join([id, str(start), str(end), word])
                    fo.write(new_row + '\n')
                    cnt += 1 
            fo.close()

            # remove created synchronisation mapping file if empty
            if cnt == 1:
                print('Removing ' + segmentname + ' as there were no mapping entry')
                os.remove(SYNCHRONISATION_MAPPING_DIR + clipname + '/' + segmentname + '.csv')


if __name__ == '__main__':
    mapping_generator()
