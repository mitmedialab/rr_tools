#! /opt/local/bin/python2.7
#
# Create people for a list of IDs in a text file, add content for each person
# from text files, and get back LIWC profile.
#
# Modified from the sample code from Receptiviti (author: Abdul Gani).
# Author: Jacqueline Kory Westlund, May 2017
# TODO: Some file paths, file names, and directories are hard-coded in; ideally
# these would be passed as arguments instead.

import requests
import json
import glob, os
import re

def v(verbose, text):
    if verbose:
        print text

class Receptiviti():
    def __init__(self, server, api_key, api_secret, verbose=False):
        """
        initialise a Receptiviti object

        :type server: str
        :type api_key: str
        :type api_secret: str
        """

        self.server = server
        self.api_key = api_key
        self.api_secret = api_secret
        self.verbose = verbose

    #''' GET /person '''
    def get_person_id(self, person):
        v(self.verbose, 'getting person: {}'.format(person))
        headers = self._create_headers()
        params = {
            'person_handle': person
        }
        response = requests.get('{}/v2/api/person'.format(self.server),
                headers=headers, params=params)
        if response.status_code == 200:
            matches = response.json()
            if len(matches) > 0:
                return matches[0]['_id']
        return None

    def _create_headers(self, more_headers={}):
        headers = dict()
        headers.update(more_headers)
        headers['X-API-KEY'] = self.api_key
        headers['X-API-SECRET-KEY'] = self.api_secret
        return headers

    #''' POST /person '''
    def create_person(self, person):
        v(self.verbose, 'Creating person: {}'.format(person))
        headers = self._create_headers({'Content-Type': 'application/json',
            'Accept': 'application/json'})
        data = {
            'name': person,
            'person_handle': person,
            'gender': 0
        }
        response = requests.post('{}/v2/api/person'.format(self.server),
                headers=headers, data=json.dumps(data))
        v(self.verbose, "Response: {}".format(response.status_code))
        v(self.verbose, "Response: {}".format(response.json()))
        if response.status_code == 200:
            return response.json()['_id']
        else:
            # See if person already exists, and if so, get their id instead.
            v(self.verbose, 'Did not create {}, trying to get instead'.format(person))
            return self.get_person_id(person)
        return None

    #''' GET /person/{id}/profile '''
    def get_person_profile(self, person_id, tags):
        v(self.verbose, 'Get person profile for {}'.format(person_id))
        p = { 'content_tags': tags }
        headers = self._create_headers()
        response = requests.get('{}/v2/api/person/{}/profile'.format(self.server,
            person_id), headers=headers, params=p)
        v(self.verbose, "Response: {}".format(response.status_code))
        if response.status_code == 200:
            return response.json()
        return None


    def add_lsm_content(self, person_id, content, recipient_id):
        v(self.verbose, 'Add content for {}'.format(person_id))
        headers = self._create_headers({'Content-Type': 'application/json',
            'Accept': 'application/json'})
        data = {
            'language_content': content,
            'recipient_id': recipient_id,
            'content_source': 6
        }
        response = requests.post('{}/v2/api/person/{}/contents'.format(self.server,
            person_id), headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()['_id']
        return None


    #''' POST /person/{id}/contents '''
    def add_content(self, person_id, content, tags, handle):
        v(self.verbose, 'Add content for {}'.format(person_id))
        headers = self._create_headers({'Content-Type': 'application/json',
            'Accept': 'application/json'})
        data = {
            'language_content': content,
            'content_source': 0,
            'content_tags': tags,
            'content_handle': handle
        }
        response = requests.post('{}/v2/api/person/{}/contents'.format(self.server,
            person_id), headers=headers, data=json.dumps(data))
        v(self.verbose, "Response: {}".format(response.status_code))
        if response.status_code == 200:
            return response.json()['_id']
        return None

    def get_lsm_score(self, id1, id2):
        v(self.verbose, 'Get score for {} vs {}'.format(id1, id2))
        headers = self._create_headers({'Accept': 'application/json'})
        params = {
            'person1': id1,
            'person2': id2
        }
        response = requests.get('{}/v2/api/lsm_score'.format(self.server),
                headers=headers, params=params)
        if response.status_code == 200:
            return response.json()['lsm_score']
        return None

    def analyse(self, person1_name, person1_content, person2_name, person2_content):
        id1 = self.get_person_id(person1_name)
        if id1 is None:
            id1 = self.create_person(person1_name)

        id2 = self.get_person_id(person2_name)
        if id2 is None:
            id2 = self.create_person(person2_name)

        if self.add_lsm_content(id1, person1_content,
                id2) is None or self.add_lsm_content(id2, person2_content, id1) is None:
            print('Failed to add content')
        else:
            return self.get_lsm_score(id1, id2)


''' Create a person for each ID in the provided file. '''
def create_people_from_ids(filename):
   # Create a person for each provided ID.
    persons = {}

    # Check whether we already have a text file with this information saved and
    # if so read that instead of doing so many get requests.
    try:
        with open("liwc-persons.txt") as json_file:
            persons = json.load(json_file)
            return persons
    except Exception as e:
        print(e)

    # Open file with list of IDs for reading and get the list.
    try:
        fh = open(filename, "r")
        pids = fh.readlines()
        for pid in pids:
            pid = pid.rstrip()
            # Create person, get back and save the weird hash id.
            print("Creating " + pid + " ...")
            persons[get_pid(pid)] = receptiviti.create_person(get_pid(pid))
            print("Got id: " + persons[get_pid(pid)])
        return persons
    except IOError as e:
        print("Cannot open file: " + filename)

def get_file_contents(filename):
        with open(filename, mode='r') as f:
            text = f.read()
        return text;

def add_file_contents(filenames):
    # Iterate over files and upload content with appropriate tags to each
    # person.
    for f in filenames:
        # Extract participant ID and session number from filenames. Also check
        # whether the file belongs to a robot. Assumes filenames follow the
        # pattern "studycode-session#-participantID-r-story#.txt" (where the -r
        # is optional and denotes that this is a robot file).
        print("Reading " + f)
        parts = f.split('-')
        pid = parts[2]
        # Append an 'r' to the id if this is a robot file.
        pid += 'r' if parts[3] is 'r' else ''
        session_half = "first" if int(re.findall(r'\d+', parts[1])[0]) <= 4 else "second"
        story_num = re.findall(r'\d+', parts[len(parts)-1])[0]

        print(pid + " " + parts[1] + " " + story_num)

        # Add the content of this file to the person.
        receptiviti.add_content(persons[get_pid(pid)], \
                get_file_contents("stories/" + f), \
                [parts[1], session_half, story_num], f.replace('.txt', ''))


# We have to create new persons for the receptiviti api because they don't let
# you delete persons.... so if you upload the wrong stuff or with the wrong tags
# it's far easier to just create new people with new names.
def get_pid(pid):
    return "p" + str(pid)


if __name__ == '__main__':
    import argparse

    description = '''Get the LIWC scores for a speaker. Pass in a list of files
    for speakers. Each filename is used to get the participant and session, used
    to tag the content. The participant is used to create the speakers via the
    Receptiviti API, and also used with the session number to get scores.
    '''

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--server', type=str, help='server to use for analysis',
            default='https://app.receptiviti.com')
    parser.add_argument('--verbose', '-v', help='verbose output', action='store_true')
    parser.add_argument('key', type=str, help='API key')
    parser.add_argument('secret', type=str, help='API secret key')
    parser.add_argument('pids', type=str, help='file containing list of pids')
    parser.add_argument('dir1', type=str, help='dir containing files containing\
            text for the speakers, with filenames containing participant IDs \
            and session numbers')

    args = parser.parse_args()

    # Create receptiviti object.
    receptiviti = Receptiviti(args.server, args.key, args.secret, args.verbose)

    # Get list of files.
    os.chdir(args.dir1)
    filenames = glob.glob("*.txt")
    os.chdir("..")

    # Create a person for each provided ID.
    persons = create_people_from_ids(args.pids)

    # Dump to file as json, for later.
    with open("liwc-persons.txt", 'w') as f:
        json.dump(persons, f)

    # Add file content for each person.
    add_file_contents(filenames)

    # Get profile for each person.
    for p in persons:
        # Get profile for each session.
        for i in range(1,9):
            session = "session" + str(i)
            res = receptiviti.get_person_profile(persons[p], [session])
            # Get json back and save to file.
            with open("liwc-results/sr2-" + p + "-" + session + ".txt", 'w') as f:
                json.dump(res, f)

        # Get profile for first half (session 1-4) vs. second (sessions 5-8).
        res = receptiviti.get_person_profile(persons[p], ["first"])
        # Get json back and save to file.
        with open("liwc-results/sr2-" + p + "-first.txt", 'w') as f:
            json.dump(res, f)

        res = receptiviti.get_person_profile(persons[p], ["second"])
        # Get json back and save to file.
        with open("liwc-results/sr2-" + p + "-second.txt", 'w') as f:
            json.dump(res, f)


