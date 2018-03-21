#!/usr/bin/env python
"""
Jacqueline Kory Westlund
August 2017
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

import rosbag  # Process bagfiles!
import argparse  # Get command line args.
import os.path  # To split extentions from filenames.
import struct  # For packing the binar audio data so it can be saved.
import wave  # For saving wav files.

from std_msgs.msg import String
from std_msgs.msg import Header
from r1d1_msgs.msg import AndroidAudio

def process_bag(bagfile):
    """ Go through the rosbag file, extract the audio, and save it to a new
    wav file.
    """
    bag = rosbag.Bag(bagfile)
    # Get a filename for our output file.
    filename, _ = os.path.splitext(bagfile)
    filename += ".wav"
    # Open wav file.
    print "Opening wav for writing... {}".format(filename)
    wav_file = wave.open(filename, 'wb')

    print "\n--------------------------------------\n{}".format(bagfile)

    # Set up audio information.
    n_channels = None
    sample_size = None
    sample_rate = None

    for topic, msg, time in bag.read_messages(topics=["/android_audio"]):
        print "Reading topic {}".format(topic)
        if not n_channels or not sample_size or not sample_rate:
            # Get all these from the AndroidAudio message.
            n_channels = msg.nchannels
            sample_size = msg.sample_width
            sample_rate = msg.sample_rate
            print "Audio info:\n\tchannels: {}\n\tsample size: {}\n\tsample " \
                  "rate: {}".format(n_channels, sample_size, sample_rate)
            # Set audio info. We didn't do this earlier because we needed to
            # get all this information about the audio stream first.
            wav_file.setnchannels(n_channels)
            wav_file.setsampwidth(sample_size)
            wav_file.setframerate(sample_rate)

        # Write the incoming audio data to the wav file.
        # (or we could add to a buffer and write the whole thing at the end)
        print "."
        wav_file.writeframes(struct.pack("h"*len(msg.samples), *msg.samples))

    # Done!
    print "Finished processing!"
    wav_file.close()
    bag.close()


if __name__ == '__main__':
    """ Given one or more rosbags, extract the audio from each rosbag, and save
    it to a wav file. Note that this is untested because rosjava is broken, and
    does not embed message type information into the messages, and so rosbag
    can't actually read back the AndroidAudio messages because it can't figure
    out what types things are. But it would probably work.
    """
    PARSER = argparse.ArgumentParser("Given one or more rosbags, extract the "
                                     "audio from each and save to a wav file."
                                     "Requires the AndroidAudio topic.")
    PARSER.add_argument("bagfiles", type=str, nargs="+",
                        help="rosbag files to process")
    ARGS = PARSER.parse_args()

    for bf in ARGS.bagfiles:
        process_bag(bf)
