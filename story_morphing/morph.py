#! /opt/local/bin/python2.7
#
# Jacqueline Kory Westlund
# May 2017

import argparse
import nltk
from rake_nltk import RakeKeywordExtractor
import text_utils

class StoryMorpher():
    """ Given a story, generate a morphed version that is similar but not
    identical to the original.
    """

    def __init__(self):
        self.noun_tags = ["NN", "NNP"]
        self.verb_tags = ["VB", "VBP", "VBD"]

    def get_keywords(self, text):
        print("Finding keywords...")
        # Remove some punctuation that we dont need.
        text = text.replace('\"', '')
        rake = RakeKeywordExtractor()
        return rake.extract(text)

    def pick_key_nouns(self, keywords):
        print("Finding key nouns...")
        keys = self._pick_key_pos(keywords, self.noun_tags)
        return keys

    def pick_key_verbs(self, keywords):
        print("Finding key verbs...")
        keys = self._pick_key_pos(keywords, self.verb_tags)
        return keys

    def _pick_key_pos(self, keywords, pos):
        keys = []
        # Pick keywords that are only one word and the indicated part of speech.
        for word in keywords:
            if len(word.split()) == 1:
                tag = nltk.pos_tag([word])
                if tag[0][1] in pos:
                    keys.append(tag[0])
        return keys


    def morph(self, text):
        # Split into sentences.
        sentences = text.split(".")
        print("Sentences:\n{}".format(sentences))

        # Get keywords.
        keywords = self.get_keywords(text)
        print(keywords)

        # Select some keywords that are only one word long and nouns.
        key_nouns = self.pick_key_nouns(keywords)
        print(key_nouns)

        # Select some keywords that are verbs.
        key_verbs = self.pick_key_verbs(keywords)
        print(key_verbs)


        # Robot's stories always start with "I'll tell a story about..." and
        # then "Once upon a time...".
        # Thus, if "I'll tell a story about..." isn't there, add it; if it is,
        # replace with a new version, where we pick a keyword or two to add in
        # as the "about".
        about = "I think you told a story like this last time. It's about" + \
                (" a " if key_nouns[0][1] == "NN" else " ") + \
                key_nouns[0][0]

        #TODO if tell a story about not in [0] need to find and replace instead
        if "tell a story about" in text.lower():
            sentences[0] = about
        else:
           sentences.insert(0, about)

        # Then add "once upon a time" if it isn't there.
        once_upon = "Once upon a time, there was " + \
                (" a " if key_nouns[0][1] == "NN" else " ") + \
                key_nouns[0][0]

        #TODO if once upon a time not in [1] need to find and replace instead
        if "once upon a time" in text.lower():
            sentences[1] = once_upon
        else:
            sentences.insert(1, once_upon)



        # Replace some keywords with other similar words.

        # Any other morphing or additions.


        # Could replace some specific phrases with similar phrases: "and then",
        # "next", etc?

        # Leave stopwords / function words mostly entact so LSM score is high.
        # Get LSM score with receptiviti to verify.

        new_text = ". ".join(sentences)
        return new_text



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Given a story, generate a
            morphed version that is similar but not identical to the original.
            ''')
    parser.add_argument('story', type=str, nargs=1, action='store',
            help="text file containing a story")
    parser.add_argument('outdir', type=str, nargs=1, action='store',
            help="directory for saving output files, such as the morphed story")
    # TODO optional number of stories, generate output for each?

    # Get arguments.
    args = parser.parse_args()

    # Get participant ID, session number, and story number from filename.
    pid, session, story_num = text_utils.extract_info_from_filename(args.story[0])

    # Read in story text.
    text = text_utils.get_file_contents(args.story[0])
    print("Story text:\n---\n{}\n---".format(text))

    # Morph story.
    story_morpher = StoryMorpher()
    new_text = story_morpher.morph(text)

    # Print out final morphed story.
    print("New story text:\n---\n{}\n---".format(new_text))


