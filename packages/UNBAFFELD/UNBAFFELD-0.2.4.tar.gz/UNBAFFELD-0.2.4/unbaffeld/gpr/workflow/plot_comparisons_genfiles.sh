#!/bin/sh

./gpfit_file.py -S -p ../data/diii-d/169958_profiles.h5
mkdir noAxis
mv DIII-D_169958_summary.txt gpr_DIII-D_169958_*.*  noAxis

./gpfit_file.py -a -S -p ../data/diii-d/169958_profiles.h5
mkdir axis
mv DIII-D_169958_summary.txt gpr_DIII-D_169958_*.*  axis

./gpfit_file.py -o varyErrors -a -S -p ../data/diii-d/169958_profiles.h5
mkdir varyErrors
mv DIII-D_169958_summary.txt gpr_DIII-D_169958_*.*  varyErrors

./gpfit_file.py -f 2.0 -o varyErrors -a -S -p ../data/diii-d/169958_profiles.h5
mkdir increaseError
mv DIII-D_169958_summary.txt gpr_DIII-D_169958_*.*  increaseError
