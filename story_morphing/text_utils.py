#! /opt/local/bin/python2.7
#
# Jacqueline Kory Westlund
# May 2017

import os
import re
import json

def extract_info_from_filename(filename):
        """ Extract participant ID, session number, and story number from a
        filename. Assumes filenames follow the pattern
        "studycode-session#-participantID-story#.txt".
        """
        print("Extracting story meta-info... " + filename)
        parts = filename.split('-')
        pid = parts[2]
        story_num = re.findall(r'\d+', parts[len(parts)-1])[0]
        print("ParticipantID: {}\nsession: {}\nstory: {}".format(pid,
                parts[1], story_num))
        return pid, parts[1], story_num


def get_file_contents(filename):
    """ Read in the contents of a text file. """
    with open(filename, mode='r') as f:
        text = f.read()
    return text;



