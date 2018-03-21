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

import argparse  # Get command line args.
import os.path  # To split extentions from filenames.
import struct  # For packing the binar audio data so it can be saved.
import wave  # For saving wav files.
import rospy  # All the ROS stuff.
from r1d1_msgs.msg import AndroidAudio  # Subscribing to this to get audio.


def on_android_audio_msg(msg):
    """ When we get an AndroidAudio message, write the binary audio data to a
    wav file. If we don't have the audio info yet, save it, and set up the wav
    file.
    """
    # Write the incoming audio data to the wav file.
    # (or we could add to a buffer and write the whole thing at the end)
    print "."
    wav_file.writeframes(struct.pack("h"*len(msg.samples), *msg.samples))


def main():
    """ Given a playing rosbag with AndroidAudio messages, subscribe to the
    'android_audio' topic, collect all the audio, and save it to a wav file.
    """
    parser = argparse.ArgumentParser("Given AndroidAudio messages in a rosbag,"
                                     " listen on the 'android_audio' topic for"
                                     " audio, collect it, and save it to a wav"
                                     " file with the specified name. You "
                                     "should start roscore, then start this "
                                     "node, and then play the rosbag.")
    parser.add_argument("outfile", type=str, nargs=1,
                        help="Filename to save audio to.",)
    args = parser.parse_args()

    # Check that we got a .wav filename for the output file.
    filename, ext = os.path.splitext(args.outfile[0])
    if ".wav" not in ext:
        filename += ".wav"
    else:
        filename = args.outfile[0]

    # Open wav file.
    print "Opening wav for writing... {}".format(filename)
    global wav_file
    wav_file = wave.open(filename, 'wb')

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
    wav_file.setnchannels(n_channels)
    wav_file.setsampwidth(sample_size)
    wav_file.setframerate(sample_rate)

    # Initialize ROS node.
    rospy.init_node('rr_audio_reader', anonymous=False)
    # Use r1d1_msgs/AndroidAudio to get incoming audio stream from the
    # robot's microphone or a standalone android microphone app.
    rospy.Subscriber('android_audio', AndroidAudio, on_android_audio_msg)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        wav_file.close()
        print "Finished processing!"


if __name__ == '__main__':
    main()
