#!/bin/bash


# Download data
$HOME/apps/RASPlot/data.py

# Plot maps
$HOME/apps/RASPlot/davinci.py > $HOME/davinci.out 2> $HOME/davinci.err

# Make timelapses
$HOME/apps/RASPlot/timelapses.py > $HOME/timelapses.out 2> $HOME/timelapses.err
