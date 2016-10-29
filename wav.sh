#!/bin/bash
#
# Converts a sound file to a wave of a predefined format.
#

INPUT_FILE=$1
OUTPUT_FILE=$2

# output file format
RATE="44100"
CHANNELS="1"
SAMPLE_SIZE="16"
ENCODING="signed-integer"

sox $INPUT_FILE \
--rate $RATE \
--channels $CHANNELS \
--bits $SAMPLE_SIZE \
--encoding $ENCODING \
--type wav \
$OUTPUT_FILE
