# rr_tools

Tools for analysis and processing for the relational robot project.

## Build and Run

These tools were built and tested with:
- pydub v0.19.0
  - `pip install`, see github.com/jiaaro/pydub for info
  - used to edit audio files in `audio_cutter.py`
  - MIT license
- praat
  - install from www.fon.hum.uva.nl/praat/
  - used to analyze audio files in `audio_comparer.py`
  - if on MacOS, create symbolic link to praat by running the following command:
  - `ln -s /Applications/Praat.app/Contents/MacOS/Praat /usr/local/bin/praat`

## audio_cutter

`usage: audio_cutter.py [-h] [-i IN_DIR] [-o OUT_DIR] timestamps_file`

Cuts .wav files at specified start and stop times. Requires a .txt file to
detail this information.

positional arguments:
- `timestamps_file`  Name of the text file with timestamps, e.g.
  "timestamps_sample.txt". Each line of the file lists an audio file
  name followed by start and stop times seperated by tabs,
  e.g. `audio_sample.wav HH:MM:SS HH:MM:SS`

optional arguments:
- `-h`, `--help`     show this help message and exit
- `-i IN_DIR`        Directory containing audio and timestamp files. Default is
  current working directory.
- `-o OUT_DIR`       Directory where cut .wav files will be exported. Default is
  current working directory.

## audio_comparer

`usage: audio_comparer.py [-h] [-i IN_DIR] [-i2 IN_DIR2] speech_files`

Compares speech files using mean pitch, mean intensity, and speaking rate. 

positional arguments:
- `speech_files`  Name of text file with speech files to be compared, e.g.
  "speech_files_sample.txt". Each line contains the name of the
  first audio file followed by a tab and then the second audio
  file, e.g. 'FILE.wav FILE2.wav'.

optional arguments:
- `-h`, `--help`     show this help message and exit
- `-i IN_DIR`        Directory containing the first row of audio files. Default is
  current working directory.
- `-i2 IN_DIR2`   Directory containig the second row of audio files. Default is
  the directory containing the first row of audio files.


## Reporting Bugs

Please report all bugs and issues on the [rr_tools github issues
page](https://github.com/mitmedialab/rr_tools/issues).
