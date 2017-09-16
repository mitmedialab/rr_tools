#!/bin/sh
# Jacqueline Kory Westlund
# September 2017
#
# Cut all lines that occur after a line containing a particular key from a file
# and put them into a new file.

set -e

if [ $# -ne 3 ]; then
    echo "$0: <dir of input files> <output dir> <break key>"
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


for FILE in "$1"/*.txt
do
    echo "Processing $FILE..."
    echo "$3"
    # The second grep sometimes returns -1 (maybe because there are no matches)
    # even when we'd rather the script continue, so swallow the error and move
    # on anyway.
    grep -A 1000 "$3" "$FILE" | grep -v "$3" > "$2/$(basename "$FILE" .txt)-ROBOT.txt" || true

done


