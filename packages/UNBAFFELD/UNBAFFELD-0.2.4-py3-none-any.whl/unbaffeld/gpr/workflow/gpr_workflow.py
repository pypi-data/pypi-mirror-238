#!/usr/bin/env python3.7
"""
Workflow script -- just quickly hardcode the parameters required for generating
the profiles for the GPR paper
"""

import os
import subprocess
import shutil


def main():
    """
    call the fit script with the a set of command line parameters
    """
    methods = ["MCMC", "EmpBayes"]  # ,"EmpBayes"]
    kernels = ["Chelinski", "Leddy"]  # ,"Leddy"
    outliers = ["None", "StudentT"]  # ,"StudentT","Detect"]

    # get all files in directory that end with .h5
    dirname = "./synthetic_data/datafiles/"
    processed_dir = "./synthetic_data/processed_datafiles/"
    ext = ".h5"
    files = [element for element in os.listdir(dirname) if element.endswith(ext)]

    for f in files:
        for m in methods:
            for k in kernels:
                for o in outliers:
                    print(
                        f"Performing fit on file: {f} with method: {m}, "
                        + f"kernel: {k}, and outlier method: {o}"
                    )
                    cmdstr = (
                        "./gp_fit.py -d '"
                        + str(dirname + f)
                        + "' -m '"
                        + str(m)
                        + "' -k '"
                        + str(k)
                        + "' -o '"
                        + str(o)
                        + "' -p False"
                    )
                    print("Calling: " + str(cmdstr))
                    subprocess.call(cmdstr, shell=True)
        shutil.move(dirname + f, processed_dir + f)


if __name__ == "__main__":
    main()
