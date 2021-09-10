
import csv
import numpy as np

PATH_TO_PARTITION_FILE = './MuSe-CAR/partition.csv'

train = [] 
devel = [] 
test = [] 

with open(PATH_TO_PARTITION_FILE, 'r') as tmp:
    next(tmp) # skip header
    for row in csv.reader(tmp):
        clipname, set = row
        if set == 'train':
            train.append(clipname)
        elif set == 'devel':
            devel.append(clipname)
        elif set == 'test':
            test.append(clipname)
        else:
            print('This folder does not belong to any set, please double-check the hard coded parition')
            exit(-1)

print('The original paritition provided by MuSe-CaR is:\n')
print('train = ' + str(train)) # 166 clips
print('devel = ' + str(devel)) # 62 clips
print('test = ' + str(test)) # 64 clips - this equals the number of clips without valid labels as counted in clips_without_labels.py


print('Since we have no access to the test set (As MuSe keeps it for fair evaluation) so we will create a new partition by shuffling the development set and splitting in half to create a devel and test set so that we can evaluate ourselves')
print('')

devel = np.array(devel) # convert list to np array
np.random.shuffle(devel) # shuffle
devel, test = devel[:len(devel)//2], devel[len(devel)//2:] # split in half
devel, test = devel.tolist(), test.tolist() # convert it back to list

print('The new paritition is:\n')
print('TRAIN_FILES = ' + str(train))
print('DEVEL_FILES = ' + str(devel))
print('TEST_FILES = ' + str(test))

# Now simply copy and paste the output (new parition) to label_distribution_analysis.py to analyse