# Takes three arguments, the first a text file with timestamps [1], the second 
# is the directory that has the audio files and timestamps [2], and the third 
# the directory that you want the cut audio files to be exported to [3]
# [1] text file format: AUDIO_FILE_NAME HH:MM:SS HH:MM:SS

import sys
from pydub import AudioSegment

def cut_audio(parsed):
    #parsed: AUDIO_FILE START STOP
    audio_file = parsed[0]
    audio = AudioSegment.from_wav(in_path + audio_file)
    cut = audio[cvt_time(parsed[1]):cvt_time(parsed[2])]
    #create name
    file_num = get_num(audio_file)
    name = audio_file[0:-4] + '_cut_%d' % file_num + '.wav'
    #export to output folder
    cut.export(out_path + name, format="wav")
    
def cvt_time(time):
    #HH:MM:SS to milli-seconds
    secs = int(time[0:2])*60*60 + int(time[3:5])*60 + int(time[6:])
    return secs * 1000

def get_num(audio_file):
    if audio_file in num:
        num[audio_file] += 1
        return num[audio_file]
    else:
        num[audio_file] = 1
        return num[audio_file]

if __name__ == '__main__':
    #AUDIO FILE
    file = sys.argv[1]
    #~/Workspace/data/output/ for example
    in_path = sys.argv[2]
    out_path = sys.argv[3]
    #keeps track of how many times each audio file has been split for naming purposes
    num = {}
    with open(in_path + file, 'r') as f:
        for line in f:
            line = line.rstrip() 
            parsed = line.split()
            print(parsed)
            cut_audio(parsed)
            

