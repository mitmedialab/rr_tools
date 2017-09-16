#!/bin/sh
# Jacqueline Kory Westlund
# September 2017
#
# Cut all lines from a file that occur before a line containing a particular
# key, and also remove any lines containing a second key, and put these lines
# into a new file.

set -e

# Use this to get first half of file:
if [ $# -ne 4 ]; then
    echo "$0: <dir of input files> <output dir> <from key> <to key>"
    exit 1
fi

if [ ! -d "$1" ]; then
    echo "$1 is not a directory, but it should be!"
    exit 1
fi

if [ ! -d "$2" ]; then
    echo "$2 is not a directory, but it should be!"
    exit 1
fi

if [ -z "$3" ]; then
    echo "$3 is not a string. Please provide a string to break the file on."
    exit 1
fi

if [ -z "$4" ]; then
    echo "$4 is not a string. Please provide a string to break the file on."
    exit 1
fi

for FILE in "$1"/*.txt
do
    echo "Processing $FILE..."
    echo "$3"

    # Use this to get first half of file:
    # The latter greps sometimes return -1 (maybe because there are no matches)
    # even when we'd rather the script continue, so swallow the error and move
    # on anyway.
    grep -B 1000 "$3" "$FILE" | grep -v "$3" | grep -v "$4" > "$2/$(basename "$FILE" .txt)-FRIEND.txt" || true

done


