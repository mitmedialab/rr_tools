#! /opt/local/bin/python2.7
"""
The above line is for Mac OSX. If you are running on linux, you may need:
/usr/bin/env python

Jacqueline Kory Westlund
September 2017
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
import nltk

if __name__ == "__main__":
    """ Main function. Get args from the command line, count up words and
    utterances, and print out the results.
    """
    # Args are:
    # A tag for tagging the output columns.
    # A list of text files to process.

    PARSER = argparse.ArgumentParser("""Given a list of text files, get the
                                     word count, line count, utterance count,
                                     and print the results. """)
    PARSER.add_argument("-t, --tag", type=str, default="", dest="tag",
                        help="""Tag for tagging output columns.""")
    PARSER.add_argument("-d, --delimiter", type=str, default="_",
                        dest="delimiter", help="""Delimiter to use to split the
                        filename in order to get a participant ID (PID) out of
                        the filename (usually - or _). Assumes the PID is the
                        first element in the filename. Default underscore_.""")
    PARSER.add_argument("infiles", type=str, nargs="+", help="""One or more
                        text files to process""")

    ARGS = PARSER.parse_args()

    print "filename\tpid\t{}_response\t{}_word_count\t{}_sent_count".format(
        ARGS.tag, ARGS.tag, ARGS.tag)

    # For each text file, count words and sentences, and print the output to
    # the screen.
    for infile in ARGS.infiles:

        # Open text file and read in text.
        with open(infile) as f:
            filename = os.path.splitext(os.path.basename(infile))[0]
            pid = filename.split(ARGS.delimiter)[0]
            text = f.read()

        # Response: are there any words? (0 or 1).
        response = 1 if text else 0
        # Word count: how many words are there?
        # Tokenize and count.
        words = nltk.word_tokenize(text)
        word_count = len(words)
        # Utterance/sentence count: How many sentences are there?
        sents = nltk.sent_tokenize(text)
        sent_count = len(sents)

        # Print the counts.
        print "{}\t{}\t{}\t{}\t{}".format(filename, pid, response, word_count,
                                          sent_count)
