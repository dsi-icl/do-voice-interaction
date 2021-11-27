import csv

def preprocess_pauses(sent):
    sent = sent.replace('...', ' (pause) ')
    sent = sent.replace('..', ' (pause) ')
    return sent.replace('--', ' (pause) ')

def preprocess_fillers(sent):
    sent = sent.replace(' uhm ', ' (um) ')
    sent = sent.replace(' uhmm ', ' (um) ')
    sent = sent.replace(' um ', ' (um) ')
    sent = sent.replace(' uh ', ' (uh) ')
    sent = sent.replace(' uhh ', ' (uh) ')
    return sent

def preprocess_shortcuts(sent):
    sent = sent.replace("don't", "do not")
    sent = sent.replace("cant't", "can not")
    sent = sent.replace("isn't", "is not")
    sent = sent.replace("aren't", "are not")
    sent = sent.replace("couldn't", "could not")
    sent = sent.replace("wouldn't", "would not")
    sent = sent.replace("won't", "will not")
    sent = sent.replace("I'm", "I am")
    sent = sent.replace("i'm", "i am")
    sent = sent.replace("she's", "she is")
    sent = sent.replace("he's", "he is")
    sent = sent.replace("we're", "we are")
    sent = sent.replace("they're", "they are")
    sent = sent.replace("you're", "you are")
    sent = sent.replace("it's", "it is")
    sent = sent.replace("that's", "that is")
    sent = sent.replace("wasn't", "was not")
    sent = sent.replace("weren't", "were not")
    sent = sent.replace("hasn't", "has not")
    sent = sent.replace("haven't", "have not")
    sent = sent.replace("doesn't", "does not")

    return sent

def get_filler_dicts():
    movie_file = open("movie_lines.tsv", "r")
    tsvreader = csv.reader(movie_file, delimiter="\t")

    predecessors = {}
    successors = {}

    for line in tsvreader:
        if len(line) >= 5:
            sent = line[4]
            sent = sent.lower().strip('?!.')
            sent = preprocess_shortcuts(sent)
            sent = preprocess_pauses(sent)
            sent = preprocess_fillers(sent)
            sent = ' '.join(sent.split())
            sent = '(start) ' + sent + ' (end)'
            words = sent.split()

            for idx in range(1, len(words) - 1):
                if words[idx] == '(pause)' or words[idx] == '(uh)' or words[idx] == '(um)':
                    predecessors[(words[idx], words[idx+1])] = (predecessors[(words[idx], words[idx+1])] if (words[idx], words[idx+1]) in predecessors else 0) + 1
                    successors[(words[idx-1], words[idx])] = (successors[(words[idx-1], words[idx])] if (words[idx-1], words[idx]) in successors else 0) + 1

    return predecessors.items(), successors.items()
