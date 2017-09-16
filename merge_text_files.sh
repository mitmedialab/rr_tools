#!/bin/sh
# Jacqueline Kory Westlund, Randy Westlund
# September 2017
#
# This script does a FULL OUTER JOIN on all *.txt files in the provided
# directory. The input files themselves must be sorted, but with the header at
# the top. Results are written to stdout. The output will be space-delimited.

set -e

# The string to use in place of missing values.
NULL=""

if [ $# -ne 1 ]; then
    echo "$0: <dir of input files>"
    exit 1
fi

if [ ! -d "$1" ]; then
    echo "$1 is not a directory, but it should be!"
    exit 1
fi

# Cut files will go here.
IN_DIR="$(mktemp -d -t rr_merge_files)"
# Joined files will go here.
JOIN_DIR="$(mktemp -d -t rr_merge_files2)"

# Cut out the first column (filenames) because we don't want it.
for F in "$1"/*.txt; do
    cut -f 2- -- "$F" \
        > "$IN_DIR/$(basename -- "$F")"
done

# Build an index of all pid numbers. Sort it, but keep the header at the top.
INDEX="$(mktemp -t rr_merge_index)"
echo pid > "$INDEX"
cut -f1 "$IN_DIR"/* | sort -u | grep -v pid >> "$INDEX"

# LEFT JOIN on the index and the input file, taking the three data columns.
for F in "$IN_DIR"/*; do
    join -a 1 -e "$NULL" -o 2.2,2.3,2.4 "$INDEX" "$F" \
        > "$JOIN_DIR/$(basename -- "$F")"
done

# Paste all the joined files together to finish the FULL OUTER JOIN. These are
# the droids we're looking for.
paste -d " " "$INDEX" "$JOIN_DIR"/*

# Clean up.
rm -r "$IN_DIR" "$JOIN_DIR" "$INDEX"
