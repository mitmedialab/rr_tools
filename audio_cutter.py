# Takes three arguments, the first a text file with timestamps [1], the second 
# is the directory that has the audio files and timestamps [2], and the third 
# the directory that you want the cut audio files to be exported to [3]
# [1] text file format: AUDIO_FILE_NAME HH:MM:SS HH:MM:SS

import argparse
from pydub import AudioSegment

def cut_audio(line):
    ''' cuts the audio file at the specified start and stop times,
    and then exports to the desiginated output folder
    line format: [AUDIO_FILE_NAME, START, STOP]
    '''
    audio_file_name = line[0]
    audio = AudioSegment.from_wav(args.in_dir + audio_file_name)
    cut = audio[cvt_time(line[1]):cvt_time(line[2])]
    #create name for cut audio file
    file_num = get_num(audio_file_name)
    cut_name = audio_file_name[0:-4] + '_cut_%d' % file_num + '.wav'
    #export to output folder
    cut.export(args.out_dir + cut_name, format="wav")
    
def cvt_time(time):
    ''' converts time format from HH:MM:SS to milli-seconds
    '''
    secs = int(time[0:2])*60*60 + int(time[3:5])*60 + int(time[6:])
    return secs * 1000

def get_num(audio_file_name):
    ''' keeps track of how many times each audio file has been split for naming purposes
    '''
    if audio_file_name in num:
        num[audio_file_name] += 1
        return num[audio_file_name]
    else:
        num[audio_file_name] = 1
        return num[audio_file_name]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Cuts .wav files at specified start 
        and stop times''')
    parser.add_argument('timestamps_file', help='''name of text file with timestamps, "timestamps.txt",
        each line lists the audio file followed by the start and stop times seperated by tabs 
        ex. my_file.wav    HH:MM:SS    HH:MM:SS''')
    parser.add_argument('in_dir', help='directory containing audio and timestamp files')
    parser.add_argument('out_dir', help='directory where cut .wav files will be exported')
    
    args = parser.parse_args()
    
    #num keeps track of how many times each audio file has been split for naming purposes
    num = {}
    with open(args.in_dir + args.timestamps_file, 'r') as f:
        for line in f:
            line = line.rstrip().split('\t')
            print(line)
            cut_audio(line)
            

