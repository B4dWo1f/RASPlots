#!/bin/bash
dirscript=`dirname $0`

FOLDER='Documents/RASP/DATA/w2'

$dirscript/data.py

$dirscript/cool_plot.py $HOME/$FOLDER/SC2/
$dirscript/cool_plot.py $HOME/$FOLDER/SC2+1/
$dirscript/cool_plot.py $HOME/$FOLDER/SC4+2/
$dirscript/cool_plot.py $HOME/$FOLDER/SC4+3/

echo "Done!"
