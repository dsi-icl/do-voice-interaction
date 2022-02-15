import sys
from pathlib import Path
sys.path.append(".")

from helper import get_pathlist_from_dir, AROUSAL_DIR, VALENCE_DIR, PROCESSED_LABEL_DIR

def label_generator():
    # create a folder if it does not exist already
    (Path(PROCESSED_LABEL_DIR)).mkdir(exist_ok=True)

    arousalfiles = get_pathlist_from_dir(AROUSAL_DIR)
    valencefiles = get_pathlist_from_dir(VALENCE_DIR)

    # iterate through all the label files e.g. 220, 221
    for arousalfile, valencefile in zip(arousalfiles, valencefiles):
        clipname = arousalfile.rsplit('/')[-1][:-4] # i.e. filename e.g. 220
        print('Creating processed labels for ' + clipname + ' and saving in ' + PROCESSED_LABEL_DIR)
        
        # create a subfolder if it does not exist already 
        (Path(PROCESSED_LABEL_DIR) / clipname).mkdir(exist_ok=True) 

        with open(arousalfile) as arousal, open(valencefile) as valence:
            next(arousal) # skip headers
            next(valence) # skip headers

            prev_seg_id = -1
            # iterate each entry in both arousal and valence label file
            for row_a, row_v in zip(arousal, valence):

                time_a, value_a, seg_id_a = row_a.split(',',-1)
                time_v, value_v, seg_id_v = row_v.split(',',-1)

                assert seg_id_a == seg_id_v
                assert time_a == time_v
                
                # first row of a segment
                if seg_id_a != prev_seg_id:
                    fo = open(PROCESSED_LABEL_DIR + clipname + '/' + clipname + '_' + seg_id_a[:-1] + '.csv', 'w')
                    print('Working on ' + clipname + '_' + seg_id_a[:-1])
                    time_to_shift = time_a
                    prev_seg_id = seg_id_a
                
                adjusted_timestamp = int(time_a) - int(time_to_shift)
                # convert micro second to second and limit to 4 decimal places
                adjusted_timestamp = format((adjusted_timestamp/1000), '.4f')

                new_row = ";".join([adjusted_timestamp, value_a, value_v])
                fo.write(new_row + '\n')
        

if __name__ == '__main__':
    label_generator()