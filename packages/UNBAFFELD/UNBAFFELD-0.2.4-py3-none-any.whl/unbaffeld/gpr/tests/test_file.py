import numpy as np
import matplotlib.pyplot as plt
import os
import sys

file_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(file_dir, ".."))
sys.path.append(parent_dir)
datadir = os.path.abspath(os.path.join(parent_dir, "../data/diii-d"))

import gpfit_file


def test_file_fit():
    # Make sure we generate files in same dir as test file
    start_dir = os.path.abspath(os.curdir)
    os.chdir(file_dir)
    datafile = os.path.join(datadir, "169958_profiles.h5")
    parser = gpfit_file.parse_gpfit_file()
    args = parser.parse_args(datafile)
    args.plot = True
    args.save = True
    args.slice = "1"
    slices = gpfit_file.get_slices(datafile, args)
    gpfit_file.fit_omas_core_profiles(datafile, slices, args)

    # Could do accepted results and more rigorous tests here
    assert os.path.exists("DIII-D_169958_summary.txt")
    assert os.path.exists("gpr_DIII-D_169958_2500.png")
    assert os.path.exists("gpr_DIII-D_169958_2500.txt")

    # Cleanup
    os.remove("DIII-D_169958_summary.txt")
    os.remove("gpr_DIII-D_169958_2500.png")
    os.remove("gpr_DIII-D_169958_2500.txt")
    os.chdir(start_dir)
    return
