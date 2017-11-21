#! /opt/local/bin/python2.7
"""
The above line is for Mac OSX. If you are running on linux, you may need:
/usr/bin/env python

Adam Gumbardo and Jacqueline Kory Westlund
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

import argparse
import warnings
import os.path
import csv as csv
import numpy as np

def get_csv_means(file_name):
    """ For a given csv file containing Affdex data, read it in and compute
    the mean score for each Affdex score.
    """
    readdata = csv.reader(open(file_name, 'rb'))
    data = []
    for row in readdata:
        data.append(row)
    header = data.pop(0)

    # Make lists to hold all the scores, and the mean scores.
    scores = []
    averages = []
    # Compute the average of every column and append it to a list.
    for col in (0, len(data[0])):
        for row in (0, len(data)):
            try:
                score = float(data[row][col])
                scores.append(score)
            except ValueError:
                pass
            # Expect to see RuntimeWarnings in this block when you take the
            # nanmean of an empty list.
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                # This is the mean, rounded to 4 decimals.
                averages.append(round(np.nanmean(scores), 4))
            del scores[:]

    # [:-1] because the csvs have an extra comma at the end
    return header[:-1], averages[:-1]


if __name__ == '__main__':
    """ Main function. Get args from the command line, iterate through CSVs,
    and write out the results.
    """
    # Args are:
    # A  of text files to process.
    # An output filename for saving the results.

    PARSER = argparse.ArgumentParser("Given a list of csv files containing"
                                     "columns of data, compute mean scores and"
                                     "print the results.")
    PARSER.add_argument("-o, --outfile", type=str, default="means.csv",
                        dest="outfile", help="""The name of a file to save the
                        results to. Default is \"means.csv\".""")
    PARSER.add_argument("infiles", type=str, nargs="+", help="""One or more
                        CSV files to process. Assumes all CSVs have the exact
                        same format.""")
    ARGS = PARSER.parse_args()
    print "Got args: {}".format(ARGS)

    ALL_MEANS = []
    for infile in ARGS.infiles:
        base, ext = os.path.splitext(os.path.basename(infile))
        if ext == ".csv":
            header, means = get_csv_means(infile)
            means = [base] + means
            print "{} ---> Done".format(base)
            ALL_MEANS.append(means)

    HEADER = ["ParticipantID"] + header
    with csv.writer(open(ARGS.outfile, 'w')) as OUTPUT_CSV:
        print "Writing out results..."
        OUTPUT_CSV.writerow(HEADER)
        for means in ALL_MEANS:
            OUTPUT_CSV.writerow(means)
