import argparse
import subprocess
# if on MacOS, creat symbolic link by running the following command in terminal
# ln -s /Applications/Praat.app/Contents/MacOS/Praat /usr/local/bin/praat

try:
	x = subprocess.check_output(["praat", "--run", "audio_analyzer.praat", "test.wav"])
	print(x)
except Exception as e:
	print e
	print "Praat didn't work!"
