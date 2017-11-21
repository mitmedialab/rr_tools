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
    - Used by the story morpher and for text analysis.
    - Apache License.
- graphviz, pygraphviz
    - used by `script_viz.py` to generate graphs.

### Version notes
These tools were built and tested with:
- Python 2.7.6

## audio_cutter

### Usage

`python audio_cutter.py [-h] [-i IN_DIR] [-o OUT_DIR] timestamps_file`

Cuts .wav and .mp3 files at specified start and stop times. Requires a .txt file
to detail this information. ffmpeg is needed to cut .mp3's

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

`python audio_comparer.py [-h] [-i IN_DIR] [-i2 IN_DIR2] [-praat PRAAT] speech_files`

Compares speech files using mean pitch, mean intensity, and speaking rate.

positional arguments:
- `speech_files`  Name of text file with speech files to be compared, e.g.
  "speech_files_sample.txt". Each line contains the name of the
  first audio file followed by a tab and then the second audio
  file, e.g. 'FILE.wav FILE2.wav'.

optional arguments:
- `-h`, `--help`     show this help message and exit
- `-i IN_DIR`        Directory containing the first column of audio files.
  Default is current working directory.
- `-i2 IN_DIR2`   Directory containig the second column of audio files. Default
  is the directory containing the first column of audio files.
- `-praat PRAAT`  Instead of creating a symbolic link to praat on MacOS, you
  may specify its location here.

## csv_means

This script was developed for getting means out of CSVs full of Affdex data.

usage: `python csv_means.py [-h] [-o, --outfile OUTFILE] infiles [infiles ...]`

positional arguments:
- `infiles`: One or more CSV files to process. Assumes all CSVs have the exact
  same format.

optional arguments:
- `-h, --help`: show this help message and exit
- `-o, --outfile OUTFILE`: The name of a file to save the results to. Default
  is "means.csv".

### Usage

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

## Text analysis

So far, we have the following text analysis tools:

### Check for keywords

`usage: check_for_keywords.py [-h] [-e, --exact] keywords infiles [infiles ...]`

Given a provided set of keywords or phrases and list of text files, count how
many times each keyword or phrase appears in each text file (case-
insensitive).

positional arguments:
    - `keywords`: Text file containing keywords or phrases, one per line
    - `infiles`: One or more text files to process

optional arguments:
    - `-h, --help`: show this help message and exit
    - `-e, --exact`: Match words exactly (case-insensitive) vs. lemmatizing first

The output of this script is a tab-delimited table with a header line listing
all the keywords or phrases followed by one line per text file processed with
the count for each keyword or phrase. The sample keyword list and sample texts produce the following output:

> filename	booyah	chunk	friend	massiv	onc upon a time	penguin	potato	slip	snowman hat	the end
> sample-text-01	0	2	2	2	1	2	0	2	0	1
> sample-text-02	0	2	0	2	1	13	0	2	2	1

## Script visualization

`python script_viz.py [-h] script_config script_file mapping`

Given script files and a mapping of audio file names to audio transcripts,
generate a graph of the conversation flow. Outputs both the `.dot` file and
a rendered `.png` file.

positional arguments:
    - `script_config`: TOML script config file.
    - `script_file`: Main script file.
    - `mapping`: CSV file mapping audio file names to the transcript of the
      audio files.

optional arguments:
    - `-h, --help`: show this help message and exit

The script files should follow the format defined by the
[rr_interaction](https://github.com/mitmedialab/rr_interaction) project.
Currently, only the main script will be graphed; any sub-scripts (such as STORY
or REPEATING scripts) will not be included in the graph. For now, you will need
graph those scripts individually.


## Reporting Bugs

Please report all bugs and issues on the [rr_tools github issues
page](https://github.com/mitmedialab/rr_tools/issues).
