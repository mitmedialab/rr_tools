#!/usr/bin/env python
"""
Jacqueline Kory Westlund
July 2018
The MIT License (MIT)

Copyright (c) 2017 Personal Robots Group

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse  # Get command line args.
from os import listdir  # To list files in a directory.
from os.path import isfile, join  # To only get files and not other dirs.
import signal  # For SIGINT.
import subprocess  # To open new processes.


if __name__ == '__main__':
    """ Given a playing rosbag with AndroidAudio messages, subscribe to the
    'android_audio' topic, collect all the audio, and save it to a wav file.
    """
    PARSER = argparse.ArgumentParser(
        "Given AndroidAudio messages in a rosbag, listen on the android_audio "
        "topic for audio, collect it, and save it to a wav file with the "
        "specified name. Listen on the rr/state topic for interaction state "
        "messages that tell us when we want to split the audio into new files."
        "You should start roscore, then start this node, and then play the "
        "rosbag.")
    PARSER.add_argument("rosbag_dir", type=str, nargs=1,
                        help="Directory of rosbags",)
    ARGS = PARSER.parse_args()

    ROSBAGS = [join(ARGS.rosbag_dir, f) for f in listdir(ARGS.rosbag_dir) if
               isfile(join(ARGS.rosbag_dir, f))]

    for bag in ROSBAGS:
        # Get the participant name and the session number for naming output.
        outfile = bag[0:6] + "-sd.txt"
        # Start the audio collector.
        collector_process = subprocess.Popen([
            "/Users/robots/projects/rr_tools/data_analysis/cut_audio_from_rosbag.py",
            outfile])
        # Play the rosbag.
        play_process = subprocess.Popen(["rosbag", "play", "-r", "18", bag])
        play_process.wait()

        # When the rosbag finishes, stop the audio collector.
        collector_process.send_signal(signal.SIGINT)
