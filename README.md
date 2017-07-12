# rr_tools

Tools for analysis and processing for the relational robot project.

## Build and Run

### Setup and dependencies

- pydub v0.19.0
  - `pip install`, see github.com/jiaaro/pydub for info
  - used to edit audio files in `audio_cutter.py`
  - MIT license
- praat
  - install from www.fon.hum.uva.nl/praat/
  - used to analyze audio files in `audio_comparer.py`
  - if on MacOS, create symbolic link to praat by running the following command:
  - `ln -s /Applications/Praat.app/Contents/MacOS/Praat /usr/local/bin/praat`
- nltk
    - Used for the story morpher.
    - Apache License.

### Version notes
These tools were built and tested with:
- Python 2.7.6

## audio_cutter

### Usage
`python audio_cutter.py [-h] [-i IN_DIR] [-o OUT_DIR] timestamps_file`

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
- `-o OUT_DIR`       Directory where cut .wav files will be exported. Default
  is current working directory.

## audio_comparer

### Usage
`python audio_comparer.py [-h] [-i IN_DIR] [-i2 IN_DIR2] speech_files`

Compares speech files using mean pitch, mean intensity, and speaking rate. 

positional arguments:
- `speech_files`  Name of text file with speech files to be compared, e.g.
  "speech_files_sample.txt". Each line contains the name of the
  first audio file followed by a tab and then the second audio
  file, e.g. 'FILE.wav FILE2.wav'.

optional arguments:
- `-h`, `--help`     show this help message and exit
- `-i IN_DIR`        Directory containing the first column of audio files. Default is
  current working directory.
- `-i2 IN_DIR2`   Directory containig the second column of audio files. Default is the directory containing the first column of audio files.
- `-praat PRAAT`  Instead of creating a symbolic link to praat on MacOS, you may specify its location here.


## Story morphing

Given a text file containing a story, generate a new story that has some
modifications from the first, or generate a story from a template using key
features detected from the first story.

Currently, the morphed story is printed out (perhaps later it could saved to
a new text file).

### Usage
`python morph.py [-h] story outdir`

positional arguments:
- `story`: text file containing a story
- `outdir`: directory for saving output files, such as the morphed story

optional arguments:
- `-h`, `--help`: show this help message and exit

## LIWC analysis

[LIWC](http://liwc.wpengine.com/) is a program for Linguistic Inquiry and Word
Count that does all sorts of interesting text analysis. The [API user
manual](http://www.receptiviti.ai/receptiviti-api-user-manual/) has information
about the output you can get. Note that to use the API, you either need the
free trial or a license.

The scripts we have so far were developed for a particular dataset with
particular naming conventions for files, participant IDs, and session numbers.
Some work needs to be done to generalize these scripts for other datasets.

### Usage
`python run-liwc.py [-h] [--server SERVER] [--verbose] key secret pids dir1`

Get the LIWC scores for a speaker. Pass in a list of files for speakers. Each
filename is used to get the participant and session, used to tag the content.
The participant is used to create the speakers via the Receptiviti API, and
also used with the session number to get scores.

positional arguments:
    - `key`: API key
    - `secret`: secret key
    - `pids`: file containing list of pids
    - `dir1`: dir containing files containing text for the speakers, with
      filenames containing participant IDs and session numbers

optional arguments:
    - `-h`, `--help`: show this help message and exit
    - `--server SERVER`: server to use for analysis
    - `--verbose`, `-v`: verbose output

### Analyze LIWC

`python analyze-liwc.py [-h] indir outdir`

Process the LIWC scores for a set of people. Provide a list of filenames for
files containing JSON LIWC output from Receptiviti.

positional arguments:
    - `indir`: dir containing files containing JSON LIWC Receptiviti output,
      with filenames containing participant IDs and session numbers
    - `outdir`: dir where we should save output files after the analysis is
      complete

optional arguments:
    - `-h`, `--help`: show this help message and exit

## Reporting Bugs

Please report all bugs and issues on the [rr_tools github issues
page](https://github.com/mitmedialab/rr_tools/issues).
