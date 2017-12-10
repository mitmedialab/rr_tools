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
import os.path
import pandas

def get_descriptives(data):
    """ Get the mean and standard deviation for each column of data.  """
    # The pandas mean function ignores NA, null, and non-numeric data.
    means = data.mean(axis=0)
    # Make the resultant series a dataframe, and append "_mean" to the name of
    # each column in the dataframe so we know that these values are the means
    # of the original columns.
    means = pandas.DataFrame([means], columns=means.index)
    means.rename(columns=lambda x: x + "_mean", inplace=True)
    # Similarly, get the standard deviations, and append "_std" to the name of
    # each column in the dataframe.
    stds = data.std(axis=0)
    stds = pandas.DataFrame([stds], columns=stds.index)
    stds.rename(columns=lambda x: x + "_std", inplace=True)
    return means, stds


def get_descriptives_by_halves(data):
    """ For a given csv file containing Affdex data, cut the data in half and
    compute descriptive statistics for the first half of the data and for the
    second half.
    """
    # First, remove any rows that are all NaN from the file, since they are
    # probably from before and after the part of the data that we care about
    # (e.g. if the video that Affdex was run on started before the person came
    # into camera view or was stopped after the person left the camera view).
    # We set the threshold for dropping rows to 2 because there's always a
    # timestamp that's not NaN, so we need at least one other not-NaN value to
    # justify keeping the row.
    print "Shape: {}".format(data.shape)
    data.dropna(thresh=2, inplace=True)
    print "Shape after removing NaN rows: {}".format(data.shape)
    if data.shape[0] == 0 or data.shape[1] == 0:
        print "Not enough good data for processing!"
        return

    first_time = data.iloc[0, 0]
    last_time = data.iloc[-1, 0]
    print "First row of data is at time: {}".format(first_time)
    print "Last row of data is at time: {}".format(last_time)

    # Since there may have been more NaN rows in one half of the file or the
    # other, we cannot split simply based on which rows is halfway. Instead, we
    # look at the timestamps. The halfway point is halfway between the first
    # row with data and the last row with data. Then we find which row
    # corresponds to this time by looking for a row with a timestamp equal to
    # or greater than that time.
    half_time = first_time + ((last_time - first_time) / 2)
    print "Half time: {}".format(half_time)
    for index, row in data.iterrows():
        # Timestamps are in the first column.
        if row[0] >= half_time:
            half_row = index
            break

    # Then get mean, std for each half of the data. Rename appropriately so we
    # know what the columns are.
    start_means, start_stds = get_descriptives(data.iloc[0:half_row - 1])
    start_means.rename(columns=lambda x: x + "_first", inplace=True)
    start_stds.rename(columns=lambda x: x + "_first", inplace=True)
    end_means, end_stds = get_descriptives(data.iloc[half_row:-1])
    end_means.rename(columns=lambda x: x + "_second", inplace=True)
    end_stds.rename(columns=lambda x: x + "_second", inplace=True)
    return start_means, start_stds, end_means, end_stds


def get_csv_stats(file_name):
    """ For a given csv file containing Affdex data, read it in and compute
    various descriptive statistics for each Affdex score. The first line of the
    csv file is the header. Each row thereafter contains data, which may be
    numbers or strings.  Strings may be "nan" or "unknown", or may contain
    data, since Affdex can return information about features such as gender,
    ethnicity, and age.
    """
    # Read in the data.
    data = pandas.read_csv(file_name, sep=',')

    # Remove columns we don't care about (i.e. glasses, age, ethnicity, etc).
    data.drop(data.columns[[3, 4, 5, 6, 7]], axis=1, inplace=True)

    # Get descriptives: mean and standard deviation.
    print "Getting overall means and standard deviations..."
    overall_means, overall_stds = get_descriptives(data)
    print "Computing descriptives by halves..."
    means1, stds1, means2, stds2 = get_descriptives_by_halves(data)

    # Append everything together and return it.
    all_data = overall_means.join([overall_stds, means1, stds1, means2, stds2])
    return all_data


if __name__ == '__main__':
    """ Main function. Get args from the command line, iterate through CSVs,
    and write out the results.
    """
    # Args are:
    # A  of text files to process.
    # An output filename for saving the results.

    PARSER = argparse.ArgumentParser("Given a list of csv files containing"
                                     "columns of Affdex data, compute mean"
                                     "scores and print the results to a CSV.")
    PARSER.add_argument("-o, --outfile", type=str, default="affdex-stats.csv",
                        dest="outfile", help="""The name of a file to save the
                        results to. Default is \"affdex-stats.csv\".""")
    PARSER.add_argument("infiles", type=str, nargs="+", help="""One or more
                        CSV files to process. Assumes all CSVs have the exact
                        same format.""")
    ARGS = PARSER.parse_args()
    print "Got args: {}".format(ARGS)

    ALL_STATS = pandas.DataFrame()
    for infile in ARGS.infiles:
        base, ext = os.path.splitext(os.path.basename(infile))
        print "Processing {}...".format(base)
        basef = pandas.DataFrame([base], columns=["ParticipantID"])
        if ext == ".csv":
            stats = get_csv_stats(infile)
            stats = stats.join([basef])
            HEADER = stats.columns.values.tolist()
            ALL_STATS = ALL_STATS.append(stats, ignore_index=True)
            print "{} ---> Done".format(base)

    # Write the statistics out to a CSV file.
    print ALL_STATS
    ALL_STATS.to_csv(path_or_buf=ARGS.outfile, sep="\t", encoding="utf-8",
            index=False)
