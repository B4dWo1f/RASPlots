#!/bin/bash
dirscript=`dirname $0`

FOLDER='Documents/RASP/DATA/w2'

time $dirscript/data.py

time $dirscript/cool_plot.py $HOME/$FOLDER/SC2/
time $dirscript/cool_plot.py $HOME/$FOLDER/SC2+1/
time $dirscript/cool_plot.py $HOME/$FOLDER/SC4+2/
time $dirscript/cool_plot.py $HOME/$FOLDER/SC4+3/

echo "Done!"
