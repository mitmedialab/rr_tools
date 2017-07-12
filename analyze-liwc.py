#! /opt/local/bin/python2.7
#
# Author: Jacqueline Kory Westlund, May 2017

import json
import glob, os
import re
import argparse

def dump_to_formatted_file(data, filename):
     with open(filename, 'w') as f:
        # Print header.
        # Dive into PIDs...
        for pid, pid_data in sorted(data.items()):

            # For a session under that PID, label PID and session.
            for session, session_data in sorted(pid_data.items()):
                f.write("ParticipantID\tSession")

                # For each item under that session, write out the label...
                for key, value_data in sorted(session_data["liwc_scores"].items()):
                    # Some items will be nested themselves.
                    if isinstance(value_data, dict):
                        for key, value in value_data.items():
                            f.write("\t" + str(key))
                    else:
                        f.write("\t" + str(key))
                for key, value_data in sorted(session_data[ \
                        "receptiviti_scores"]["percentiles"].items()):
                    f.write("\t" + str(key))
                for key, value_data in sorted(session_data[ \
                        "receptiviti_scores"]["raw_scores"].items()):
                    f.write("\t" + str(key))

                # Only print once.
                f.write("\n")
                break
            break


        # For each PID in the data...
        for pid, pid_data in sorted(data.items()):

            # For each session under that PID, write the PID and session.
            for session, session_data in sorted(pid_data.items()):
                f.write(pid + "\t" + session)

                # For each item under that session, write out the value...
                for key, value_data in sorted(session_data["liwc_scores"].items()):
                    # Some items will be nested themselves.
                    if isinstance(value_data, dict):
                        for key, value in value_data.items():
                            f.write("\t" + str(value))
                    else:
                        f.write("\t" + str(value_data))
                for key, value_data in sorted(session_data[ \
                        "receptiviti_scores"]["percentiles"].items()):
                    f.write("\t" + str(value_data))
                for key, value_data in sorted(session_data[ \
                        "receptiviti_scores"]["raw_scores"].items()):
                    f.write("\t" + str(value_data))

                # Add newline between lines.
                f.write("\n")


if __name__ == '__main__':
    description = '''Process the LIWC scores for a set of people. Provide a list
    of filenames for files containing JSON LIWC output from Receptiviti.
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('indir', type=str, help='dir containing files containing\
            JSON LIWC Receptiviti output, with filenames containing participant\
            IDs and session numbers')
    parser.add_argument('outdir', type=str, help='dir where we should save\
            output files after the analysis is complete')

    args = parser.parse_args()


    # To hold participant and robot data, respectively.
    datap = {}
    datar = {}
    datap_halves = {}
    datar_halves = {}
    have_files = False

    # TODO change out/in directory reading to use absolute paths...
    # If there are data files already, read them.
    try:
        os.chdir(args.outdir)
        with open("json-liwc-datar.txt") as json_file:
            datar = json.load(json_file)
        with open("json-liwc-datap.txt") as json_file:
            datap = json.load(json_file)
        with open("json-liwc-datar_halves.txt") as json_file:
            datar_halves = json.load(json_file)
        with open("json-liwc-datap_halves.txt") as json_file:
            datap_halves = json.load(json_file)
        have_files = True
    except Exception as e:
        print(e)

    # If there aren't any data files yet, read in from files to make them:
    if not have_files:
        # Get list of files from the input directory.
        os.chdir("../" + args.indir)
        filenames = glob.glob("*.txt")

        # For each file, read in the JSON array of LIWC output.
        for f in filenames:
            print("Reading " + f)

            # Get participant and session from the filename.
            parts = f.split('-')
            pid = parts[1]
            session = parts[2].replace('.txt','')

            try:
                with open(f) as json_file:
                    contents  = json.load(json_file)
                    # Skip if file is empty.
                    if contents == None or contents == "null" or contents == {}:
                        print(f + " has no contents -- skipping")
                        continue

                    # Make a dictionary of all participant results sorted by PID
                    # and session tag. Make a separate dictionary for robot results.
                    # Make separate dictionaries for the halved results, i.e., first
                    # half (sessions 1-4) vs. second half (session 5-8).
                    elif "first" in session or "second" in session:
                        if 'r' in pid:
                            pid = pid.replace('r', '')
                            if pid not in datar_halves.keys():
                                datar_halves[pid] = {}
                            datar_halves[pid][session] = contents
                        else:
                            if pid not in datap_halves.keys():
                                datap_halves[pid] = {}
                            datap_halves[pid][session] = contents
                    else:
                        if 'r' in pid:
                            pid = pid.replace('r', '')
                            if pid not in datar.keys():
                                datar[pid] = {}
                            datar[pid][session] = contents
                        else:
                            if pid not in datap.keys():
                                datap[pid] = {}
                            datap[pid][session] = contents
                    print("Got " + f)

            except Exception as e:
                print(e)

        # Go to the output directory in preparation for saving results there.
        os.chdir("../" + args.outdir)

    # We have data loaded.
    # Dump as JSON to file so it's faster to load next time.
        with open("json-liwc-datar.txt", 'w') as f:
            json.dump(datar, f)
        with open("json-liwc-datap.txt", 'w') as f:
            json.dump(datap, f)
        with open("json-liwc-datar_halves.txt", 'w') as f:
            json.dump(datar_halves, f)
        with open("json-liwc-datap_halves.txt", 'w') as f:
            json.dump(datap_halves, f)

    # Dump to file for loading into R, specially formatted.
    # PID session liwc#1 liwc#2 ...
    # ... ...     ...    ...
    dump_to_formatted_file(datar, "liwc-datar.txt")
    dump_to_formatted_file(datap, "liwc-datap.txt")
    dump_to_formatted_file(datar_halves, "liwc-datar_halves.txt")
    dump_to_formatted_file(datap_halves, "liwc-datap_halves.txt")

    # Now do analyses.
    # Repeated measures ANOVA first vs second for participants.
    # TODO can't do repeated measures easily in python (can in R...)


    # Correlate s1-8 participant with robot.

