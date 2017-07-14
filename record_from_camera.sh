#!/bin/sh

# Ask user to pick video and audio devices to record from.
# Use ffmpeg to record to a file, which by default gets saved in a "rr1-videos"
# directory in the current working directory.

# If any command fails, exit the script.
set -e

# Directory to save videos in.
VID_DIR="rr1-videos"

disp() {
    printf "\033[32m$1\n\033[39m"
}

# We need one argument: the participant ID (used in video filenames).
if [ $# -ne 1 ]; then
    disp "Usage: $0 <participant_id>"
    exit 1
fi

# List devices.
ffmpeg -f avfoundation -list_devices true -i "" 2>&1 \
    | grep "input device" \
    | cut -d " " -f 6-

# Prompt user to pick a device.
disp "Look at the list of devices above. Enter the index of the camera to use"
disp "and index of the audio to use, separated by a :. Example: 0:1"
read DEVICE1

# Make a directory to save the videos in.
mkdir -p $VID_DIR

DATE="$(date +%Y-%m-%d-%H-%M-%S)"
OUT1="$VID_DIR/rr1-$1-$DATE.mp4"
disp "Video will be saved to: $OUT1"


# Record using ffmpeg.
ffmpeg -y -f avfoundation -s 640x480 -r 30 -i $DEVICE1 $OUT1

disp "Video was saved to: $OUT1"



