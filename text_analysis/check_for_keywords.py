#! /opt/local/bin/python2.7
"""
Given a set of keywords or phrases and a list of text files, count how many
times each keyword or phrase appears in each text file.

Jacqueline Kory Westlund, August 2017
"""

import argparse
import os.path
import string
import collections
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

if __name__ == '__main__':
    # Args are a text file containing the keywords or phrases to search for, and
    # the text files to search.
    PARSER = argparse.ArgumentParser("""Given a provided set of keywords or
                                     phrases and list of text files, count how
                                     many times each keyword or phrase appears
                                     in each text file (case-insensitive).""")
    PARSER.add_argument("-e, --exact", default=False, action="store_true",
                        dest="exact", help="""Match words exactly
                        (case-insensitive) vs. lemmatizing first""")
    PARSER.add_argument("keywords", type=str, nargs=1,
                        help="""Text file containing keywords or phrases, one
                        per line""")
    PARSER.add_argument("infiles", type=str, nargs="+", help="""One or more
                        text files to process""")

    ARGS = PARSER.parse_args()

    # Open keyword file and get the list of keywords and phrases.
    with open(ARGS.keywords[0], "r") as f:
        KEYS = f.readlines()
        KEYS = [k.strip().lower().translate(None, string.punctuation) for k in KEYS]

        # If we're not matching exact words, then we want to lemmatize and stem.
        if not ARGS.exact:
            LEMMATIZER = WordNetLemmatizer()
            STEMMER = PorterStemmer()
            # If a keyword or phrase has multiple words (i.e. includes spaces)
            # then we need to lemmatize and stem each of those words before
            # putting the phrase back together.
            PROCESSED_KEYS = []
            for key in KEYS:
                kw = nltk.word_tokenize(key)
                kw = [LEMMATIZER.lemmatize(k) for k in kw]
                kw = [STEMMER.stem(k) for k in kw]
                key = " ".join(kw)
                PROCESSED_KEYS.append(key)
            PROCESSED_KEYS.sort()

    # Print a header line with the filename and the keywords and phrases.
    print "filename\t" + "\t".join(PROCESSED_KEYS)

    # For each text file, count how many times each keyword or phrase appears,
    # and print the output to the screen. Probably not the most efficient way of
    # doing this but it works for now.
    for infile in ARGS.infiles:

        # Open text file and read in text.
        with open(infile) as f:
            filename = os.path.splitext(os.path.basename(infile))[0]
            text = f.read().lower()
            # Remove all punctuation and tokenize into words.
            words = nltk.word_tokenize(text.translate(None, string.punctuation))

        # If we're not matching exact words, then we want to lemmatize and stem.
        if not ARGS.exact:
            # Lemmatize the text.
            words = [LEMMATIZER.lemmatize(word) for word in words]
            words = [STEMMER.stem(word) for word in words]

        # For each keyword and phrase, count it.
        # We have to rejoin the words into one string so we can check for
        # phrases (since after word tokenizing all the words are separate
        # elements in the list of words).
        words = " ".join(words)
        key_counter = collections.OrderedDict()
        for key in PROCESSED_KEYS:
            key_counter[key] = words.count(key)

        # Print the counts.
        print filename + "\t" + "\t".join(map(str, key_counter.values()))
