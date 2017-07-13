''' Compares speech files using mean pitch, mean intensity, and speaking rate.
If on MacOS, create symbolic link to praat by running the following command ln
-s /Applications/Praat.app/Contents/MacOS/Praat /usr/local/bin/praat
'''
import argparse 
import subprocess 
import time 
import sys 
import os

def run_praat(speech_file):
    ''' Runs the speech.wav through a praat script to determine the mean_pitch, 
    mean_intensity, and speaking_rate. Retutns an unparsed string of these values.
    '''
    try:
        output = subprocess.check_output([args.praat, "--run", "audio_analyzer.praat", 
            speech_file])
        return output
    except Exception as e:
        print e
        print "Praat didn't work!"

def praat_parser(output, name):
    ''' Takes the string outputed from the praat script and adds float values 
    rounded to two decimal places to the values dictionary. If an error is raised 
    in praat such that the specified audio file cannot be found, the output file
     will be deleted and the script will close.
    '''
    values = {}
    lines = output.splitlines()
    for line in lines:
        if line == 'Cannot read target file': # this is the error that praat will raise
            print('Unexpected error: %s not found' % name)
            os.remove(output_name) # delete the output
            sys.exit(0) # exit the script
        if line[0:11] == 'Mean pitch:':
            values['mean_pitch'] = round(float(line[12:]), 2)
        if line[0:15] == 'Mean intensity:':
            values['mean_intensity'] = round(float(line[16:]), 2)
        if line[0:14] == 'Speaking rate:':
            values['speaking_rate'] = round(float(line[15:]), 2)
    return values

def write_to_file(line, values, values2):
    ''' Writes the values specified in the header to the output file
    '''
    line1 = line[0] + '\t' + line[1] + '\t' + str(values['mean_pitch']) + '\t' + \
    str(values['mean_intensity']) + '\t' + str(values['speaking_rate']) + '\t'

    line1 += str(values2['mean_pitch'])  + '\t' + str(values2['mean_intensity']) \
    + '\t' + str(values2['speaking_rate']) + '\t'

    line1 += str(values['mean_pitch'] - values2['mean_pitch']) + '\t' + \
    str(values['mean_intensity'] - values2['mean_intensity']) + '\t' + \
    str(values['speaking_rate'] - values2['speaking_rate']) + '\n'

    file.write(line1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Compares speech files using 
        mean pitch, mean intensity, and speaking rate. If on MacOS, create 
        symbolic link to praat by running the following command: 
        ln -s /Applications/Praat.app/Contents/MacOS/Praat /usr/local/bin/praat''')
    parser.add_argument('speech_files', type=str, default='speech_files_sample.txt', 
        help='''Name of text file with speech files to be compared, e.g. 
        "speech_files_sample.txt". Each line contains the name of the first audio
         file followed by a tab and then the second audio file, e.g. "FILE.wav
             FILE2.wav".''')
    parser.add_argument('-i', dest='in_dir', type=str, default="./", 
        help='''Directory containing the first column of audio files. Default is 
        current working directory.''')
    parser.add_argument('-i2', dest='in_dir2', type=str, default="./", 
        help='''Directory containig the second column of audio files. Default is 
        the directory containing the first column of audio files.''')
    parser.add_argument('-praat', dest='praat', type=str, default='praat', 
        help='''Instead of creating a symbolic link to praat on MacOS, you may
        specify its location here.''')

    args = parser.parse_args()
    # if a second audio directory isn't specified, default it to the first
    if args.in_dir2 == "./" and args.in_dir != "./":
        args.in_dir2 = args.in_dir

    # file setup
    output_name = 'output_' + time.strftime("%m%d%y_%H%M%S") + '.txt'
    file = open(output_name, 'w')
    header ='''file1\tfile2\tmean_pitch1\tmean_intensity1\tspeaking_rate1\tmean_pitch2\
    \tmean_intensity2\tspeaking_rate2\tpitch_diff\tintensity_diff\trate_diff\n'''
    file.write(header)

    with open(args.speech_files, 'r') as f:
        for line in f:
            line = line.rstrip().split('\t') # ['test.wav', 'test2.wav']
            # gets output from praat
            output = run_praat(args.in_dir + line[0])
            output2 = run_praat(args.in_dir2 + line[1]) 
            # makes dictionaries from output
            values = praat_parser(output, args.in_dir + line[0])
            values2 =  praat_parser(output2, args.in_dir2 + line[1]) 
            # writes values to file
            print(line)
            write_to_file(line, values, values2) 

    file.close()
    print('Done ---> ' + output_name)










