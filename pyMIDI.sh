#!/bin/bash

## Get the current time
#current_time=$(date '+%Y-%m-%d %H:%M:%S')
## Get the directory of the current script
#script_dir=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
## Write both into a text file
#echo "$current_time $script_dir" >> "/Users/sh/Programming/pyMIDI/output.txt"

# Change directory to the location of this script
cd "$(dirname "$(realpath "${BASH_SOURCE[0]}")")" || exit

uv run pyMIDI.py "$@"