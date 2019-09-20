#!/bin/bash
BASEDIR=$(dirname "$0")


# Download data
$BASEDIR/data.py

# Plot maps
$BASEDIR/davinci.py > $HOME/davinci.out 2> $HOME/davinci.err

# Make timelapses
$BASEDIR/timelapses.py > $HOME/timelapses.out 2> $HOME/timelapses.err
