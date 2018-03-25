#!/usr/bin/env python
"""
Jacqueline Kory Westlund
March 2018
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
import os.path  # To split extentions from filenames.
import struct  # For packing the binar audio data so it can be saved.
import wave  # For saving wav files.
import rospy  # All the ROS stuff.
from r1d1_msgs.msg import AndroidAudio  # Subscribing to this to get audio.
from rr_msgs.msg import InteractionState  # Know when to collect audio.


def on_android_audio_msg(msg):
    """ When we get an AndroidAudio message, write the binary audio data to a
    wav file. If we don't have the audio info yet, save it, and set up the wav
    file.
    """
    # Write the incoming audio data to the wav file.
    # (or we could add to a buffer and write the whole thing at the end)
    if WAV_FILE and RECORD:
        WAV_FILE.writeframes(struct.pack("h"*len(msg.samples), *msg.samples))


def on_state_msg(msg):
    """ When we receive InteractionState messages, use the current state info
    to determine whether we want to save audio to a new file or not.
    """
    global RECORD
    print "Got state message: {}".format(msg.state)
    if "start child story retell" in msg.state or \
            "start child story create" in msg.state:
        print "Start recording!"
        RECORD = True
        setup_audio_file()
    elif "end child story retell" in msg.state or \
            "end child story create" in msg.state:
        RECORD = False
        print "Stop recording!"
        if WAV_FILE:
            WAV_FILE.close()
        print "Finished processing!"


def setup_audio_file():
    """ Open a wav file for recording. """
    # Open wav file.
    print "Opening wav for writing... {}".format(FILENAME)
    global WAV_FILE
    WAV_FILE = wave.open(FILENAME, 'wb')

    # Set up audio information.
    # These are the defaults for the ROS AndroidAudio message when published by
    # Tega. If you don't want to use the defaults, you can get this information
    # from the AndroidAudio message later.
    n_channels = 1
    sample_size = 2
    sample_rate = 44100

    print "Audio info:\n\tchannels: {}\n\tsample size: {}\n\tsample " \
          "rate: {}".format(n_channels, sample_size, sample_rate)
    # Set audio info for the wav file.
    print "Setting up wav file for writing..."
    WAV_FILE.setnchannels(n_channels)
    WAV_FILE.setsampwidth(sample_size)
    WAV_FILE.setframerate(sample_rate)


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
    PARSER.add_argument("outfile", type=str, nargs=1,
                        help="Filename to save audio to.",)
    ARGS = PARSER.parse_args()

    # We don't start out recording audio.
    RECORD = False
    WAV_FILE = None

    # Check that we got a .wav filename for the output file.
    FILENAME, EXT = os.path.splitext(ARGS.outfile[0])
    if ".wav" not in EXT:
        FILENAME += ".wav"
    else:
        FILENAME = ARGS.outfile[0]
    print "will save file to {}".format(FILENAME)

    # Initialize ROS node.
    rospy.init_node('rr_audio_reader', anonymous=False)
    # Use r1d1_msgs/AndroidAudio to get incoming audio stream from the
    # robot's microphone or a standalone android microphone app.
    AUDIO_SUB = rospy.Subscriber('android_audio', AndroidAudio,
                                 on_android_audio_msg)
    STATE_SUB = rospy.Subscriber('rr/state', InteractionState,
                                 on_state_msg)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        if WAV_FILE:
            WAV_FILE.close()
        print "Finished processing!"
