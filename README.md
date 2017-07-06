# rr_tools

Tools for analysis and processing for the relational robot project.

## Build and Run

These tools were built and tested with:
- pydub v0.19.0
  - `pip install`, see github.com/jiaaro/pydub for info
  - used to edit audio files in `audio_cutter.py`
  - MIT license

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

## Reporting Bugs

Please report all bugs and issues on the [rr_tools github issues
page](https://github.com/mitmedialab/rr_tools/issues).
