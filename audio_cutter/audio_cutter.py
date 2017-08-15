# Takes three arguments, the first a text file with timestamps [1], the second 
# is the directory that has the audio files and timestamps [2], and the third 
# the directory that you want the cut audio files to be exported to [3]
# [1] text file format: AUDIO_FILE_NAME HH:MM:SS HH:MM:SS

import argparse
import os
from pydub import AudioSegment

def cut_audio(line):
    ''' cuts the audio file at the specified start and stop times,
    and then exports to the desiginated output folder
    line format: [AUDIO_FILE_NAME, START, STOP]
    '''
    audio_file_name = line[0]
    file_type = audio_file_name[-4:]

    if file_type == '.wav':
        audio = AudioSegment.from_wav(args.in_dir + audio_file_name)
        cut = audio[cvt_time(line[1]):cvt_time(line[2])]
        #create name for cut audio file
        file_num = get_num(audio_file_name)
        cut_name = audio_file_name[0:-4] + '_cut_%d' % file_num + '.wav'
        #export to output folder
        cut.export(args.out_dir + cut_name, format="wav")
        print('---> ' + cut_name + '\n')
    elif file_type == '.mp3':
        audio = AudioSegment.from_mp3(args.in_dir + audio_file_name)
        cut = audio[cvt_time(line[1]):cvt_time(line[2])]
        #create name for cut audio file
        file_num = get_num(audio_file_name)
        cut_name = audio_file_name[0:-4] + '_cut_%d' % file_num + '.mp3'
        #export to output folder
        cut.export(args.out_dir + cut_name, format="mp3")
        print('---> ' + cut_name + '\n')
    else:
        #error, incompatible file type
        print('**** ' + audio_file_name + ' caused an error')
        print('**** ' + file_type + ' incompatible file type')
        print('**** skipping file\n')
        
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
    parser = argparse.ArgumentParser(description='''Cuts .wav and .mp3 files at specified start 
        and stop times. Requires a .txt file to detail this information. ffmpeg is needed to cut .mp3's''')
    parser.add_argument('timestamps_file', type=str, default='timestamps_sample.txt', help='''Name 
        of the text file with timestamps, e.g. "timestamps_sample.txt". Each line of the file lists an audio file followed by 
        start and stop times seperated by tabs, e.g. "audio_sample.wav    HH:MM:SS    HH:MM:SS"''')
    parser.add_argument('-i', dest='in_dir', type=str, default="./", help='Directory containing audio and timestamp files. Default is current working directory.')
    parser.add_argument('-o', dest='out_dir', type=str, default="./", help='Directory where cut .wav files will be exported. Default is current working directory.')
    
    args = parser.parse_args()

    #provides helpful information in terminal
    info = '\nTimestamps file: %s\nInput direcory: %s\nOutput directory: %s\n' % (args.timestamps_file, args.in_dir, args.out_dir)
    print(info)

    #num keeps track of how many times each audio file has been split for naming purposes
    num = {}
    with open(args.in_dir + args.timestamps_file, 'r') as f:
        for line in f:
            line = line.rstrip().split('\t')
            print(line)
            cut_audio(line)



            

