# rr_tools

Tools for analysis and processing for the relational robot project.

## Build and Run

### Setup and dependencies

- pydub v0.19.0
    - `pip install`, see github.com/jiaaro/pydub for info.
    - Used to edit audio files in `audio_cutter.py`.
    - MIT license
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


## Reporting Bugs

Please report all bugs and issues on the [rr_tools github issues
page](https://github.com/mitmedialab/rr_tools/issues).
