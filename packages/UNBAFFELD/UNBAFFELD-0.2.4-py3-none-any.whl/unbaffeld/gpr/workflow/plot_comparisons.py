#!/usr/bin/env python
"""
Plot all a comparisons of all of the density and temperatures in a file saved
by gpfit_file.py
"""

import argparse
import h5py
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

sys.path.append(os.curdir)
from gpfit_file import rm_nan
import eqdb_utils


def get_data(fname):
    """Extract the data from an OMAS-compliant file with the
    data located in the `core_profiles` IDS.
    """
    hf = h5py.File(fname, mode="r")
    times = hf.get("/core_profiles/time")[()]
    slices = np.arange(times.size)
    profiles = hf.get("core_profiles/profiles_1d")
    namax = 0.0
    tamax = 0.0
    # Now get the data
    edata = {}
    for slice in slices:
        time = str(times[int(slice)])
        egrp = profiles.get(str(slice) + "/electrons")
        xn = rm_nan(egrp.get("density_fit/rho_tor_norm")[()])
        yn = rm_nan(egrp.get("density_fit/measured")[()])
        yen = rm_nan(egrp.get("density_fit/measured_error_upper")[()])
        nmax = np.max(yen)
        namax = np.max([nmax, namax])

        xt = rm_nan(egrp.get("temperature_fit/rho_tor_norm")[()])
        yt = rm_nan(egrp.get("temperature_fit/measured")[()])
        yet = rm_nan(egrp.get("temperature_fit/measured_error_upper")[()])
        tmax = np.max(yet)
        tamax = np.max([tmax, tamax])

        edata[time] = {}
        edata[time]["density_rho"] = xn
        edata[time]["density_measured"] = yn
        edata[time]["density_error"] = yen
        edata[time]["density_max"] = namax
        edata[time]["temperature_rho"] = xt
        edata[time]["temperature_measured"] = yt
        edata[time]["temperature_error"] = yet
        edata[time]["temperature_max"] = tamax
    return edata, times


def plot_gpfit_comparisons(profile_file, data_file, slices, args):
    edata, times = get_data(data_file)
    hf = h5py.File(profile_file, mode="r")
    prgrp = hf.get("/thomson_scattering/profiles")
    eqdb_utils.datalist = []
    profile_dict = eqdb_utils.getdbvals(prgrp, [], False)
    for slice in slices:
        time = str(times[int(slice)])
        if time not in edata:
            print(f"Experimental data not found for time: {time}")
            continue
        if time not in profile_dict:
            print(f"GPR fit data data not found for time: {time}")
            continue

        # Create subplots for density and temperature
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        # Not working.
        # ax1.set_ylim(0.0, edata[time]['density_max'])
        ax1.set_title("Density")
        # ax2.set_ylim(0.0, edata[time]['temperature_max'])
        ax2.set_title("Temperature")
        ax1.errorbar(
            edata[time]["density_rho"],
            edata[time]["density_measured"],
            yerr=edata[time]["density_error"],
            linestyle="None",
            marker="o",
            label="Experimental Data",
        )
        ax2.errorbar(
            edata[time]["temperature_rho"],
            edata[time]["temperature_measured"],
            yerr=edata[time]["temperature_error"],
            linestyle="None",
            marker="o",
            label="Experimental Data",
        )
        for prof in ["density_fit", "temperature_fit"]:
            ddict = profile_dict[time][prof]
            ax = ax1 if prof == "density_fit" else ax2
            for pkey in ddict:
                if not pkey.startswith("data"):
                    continue
                gpr_type = "_".join(pkey.split("_")[1:]).strip("_")
                if gpr_type.strip():
                    label = gpr_type
                    refkey = "_" + gpr_type
                else:
                    label = "No constraint. No vary errors"
                    refkey = ""
                ax.plot(ddict["rho_tor" + refkey], ddict["data" + refkey], label=label)
        ax1.legend()
        ax2.legend()
        if args.save:
            cfile = profile_file.rstrip(".h5") + "_" + time + "_comparison.png"
            plt.savefig(cfile, dpi=600)
        else:
            plt.show()
    return


def get_slices(fname, args):
    """
    Choose the slices from single OMAS file
    """
    hf = h5py.File(fname, mode="r")
    time = hf.get("/core_profiles/time")[()]
    hf.close
    t_str = ",".join(str(x) for x in time)
    t_lst = t_str.split(",")

    slice_lst = []
    for ts in t_lst:
        slice_lst.append(str(t_lst.index(ts)))

    if args.list_time:
        print("Time slices in: ", fname)
        [print(s + ",", t) for s, t in zip(slice_lst, t_lst)]
        return None

    slice_select = None
    if args.time:
        # Select times from input
        time_select = args.time.split(",")
        slice_select = []
        for ts in time_select:
            if ts in t_lst:
                slice_select.append(t_lst.index(ts))
            else:
                print("Time ", ts, " not found.")

    if args.slice:
        slice_select = args.slice.split(",")

    if not slice_select:
        slice_select = slice_lst

    return slice_select


def parse_gpr_comparisons(desc=None):
    """Set up parsing the arguments and return the parser.
    This enables other files to use the same parser
    """
    if not desc:
        desc = "Plot comparisons of different GPR methods"

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "files", type=str, nargs="+", help="h5 data file containing Thomson profile"
    )
    parser.add_argument(
        "-S", "--save", dest="save", help="Save plots as figures", action="store_true"
    )
    parser.add_argument(
        "-s",
        "--slice",
        help="Comma delimited list of time slices (integers) select",
        default=None,
    )
    parser.add_argument(
        "-t", "--time", help="Comma delimited list of times select", default=None
    )
    parser.add_argument(
        "-l",
        "--list_time",
        help="List all of the times that have equilibria",
        dest="list_time",
        action="store_true",
    )
    return parser


def main():
    """
    Read profile from provided .h5 file and fit.
    """
    parser = parse_gpr_comparisons()
    args = parser.parse_args()

    if not len(args.files) == 2:
        # Need to think about multiprocessing here
        print(parser.usage())
        return
    else:
        profile_file = args.files[0]
        data_file = args.files[1]
        slices = get_slices(data_file, args)
        if slices:
            plot_gpfit_comparisons(profile_file, data_file, slices, args)

    return


if __name__ == "__main__":
    main()
