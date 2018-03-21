#!/bin/sh
# Jacqueline Kory Westlund
# December 2017
# Change "nan" to "NaN" in all files provided to this script. Mutates the files
# and does not make a backup first.

sed -i "" -e "s/nan/NaN/g" $@
