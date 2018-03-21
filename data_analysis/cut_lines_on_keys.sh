#!/bin/sh
# Jacqueline Kory Westlund
# September 2017
#
# Cut each line after a line containing a particular key and save all those
# lines to a new file. The lines we care about are tagged with a word followed
# by a semicolon, so remove that word and the semicolon and just keep what's
# after it.

set -e

# Use this to cut each line after a particular key.
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

for FILE in "$1"/*.csv
do
    echo "Processing $FILE..."
    echo "$3"
    # The second grep sometimes return -1 (maybe because there are no matches)
    # even when we'd rather the script continue, so swallow the error and move
    # on anyway.
    grep -A 1 --no-group-separator "$3" "$FILE" | grep -v "$3" | cut -d ";" -f 2- > "$2/$(basename "$FILE" .txt)-$3.txt" || true

done


