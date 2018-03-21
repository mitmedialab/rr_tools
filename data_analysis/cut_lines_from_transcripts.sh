#!/bin/sh
# Jacqueline Kory Westlund
# August 2017
#
# For the provided file:
# - Remove "Tega" and "Experimenter" lines from transcripts.
# - Remove the word "Child:" and any stuff in [brackets].
#
# To run on a lot of files in fish:
# for file in *.txt
#     ./cut_lines_from_transcripts.sh $file > outdir/(basename $file)
# end
#

grep -h -v -e "^Tega" $1 | grep -v -e "^Experimenter" | sed -e "s/^Child://" -e "s/\[.*\]//g"
