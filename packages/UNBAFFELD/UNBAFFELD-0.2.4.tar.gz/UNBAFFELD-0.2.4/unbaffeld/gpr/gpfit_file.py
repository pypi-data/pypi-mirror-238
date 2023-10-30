#!/usr/bin/env python
"""
Python driving for performing GPR regression on OMAS files that have
data in the `core_profiles` IDS.

Two modes of operation:
   1. Process single file
      o  Include tools for selecting a subset of the time slices
      o  Plotting can be done in this mode
   2. Batch process multiple files
      o In this case, all time selection tools are ignored and all slices
        in all files are generated.
      o This however can include generating batch figures
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np
from gpfit import parse_gpfit, print_gpfit_options, GPTSFit


# nan's can occur in the data
def rm_nan(arr):
    return arr[~np.isnan(arr)]


def get_shotlabel_from_h5(h5in):
    """
    Find the machine and shot to label the root directory
    """
    metagrp = h5in.get("dataset_description/data_entry")
    machine = metagrp["machine"].asstr()[...]
    # Pulse sometimes seems to be a string and somtimes an integer
    try:
        pulse = metagrp["pulse"].asstr()[...]
    except TypeError:
        pulse = str(metagrp["pulse"][()])
    return machine + "_" + pulse


# It is possible that the h5py reads should be in efitai_database
#  but it is not in the default database of time of writing this
def fit_omas_core_profiles(fname, slices, args):
    """ Extract the data from an OMAS-compliant file with the
        data located in the `core_profiles` IDS.
        Returns the x and y to be used in fitting
        :param fname: \
            Name of h5 file to open
    """

    # Bunch of introductory stuff around I/O management
    def gplog(msg):
        """Log function for convenience"""
        if args.save:
            fh.write(msg + "\n")
        print(msg)
        return

    hf = h5py.File(fname, mode="r")
    shotlbl = get_shotlabel_from_h5(hf)
    times = hf.get("/core_profiles/time")[()]
    profiles = hf.get("core_profiles/profiles_1d")
    if args.save:
        fh = open(shotlbl + "_summary.txt", "w")
        gplog(print_gpfit_options(args))
        fh.close()
    else:
        print(print_gpfit_options(args))
    # if plotting, then want the limits to make
    #  sure all plots in a file have the same limits
    namax = 0.0
    tamax = 0.0
    for slice in slices:
        egrp = profiles.get(str(slice) + "/electrons")
        nmax = np.max(rm_nan(egrp.get("density_fit/measured")[()]))
        tmax = np.max(rm_nan(egrp.get("temperature_fit/measured")[()]))
        namax = np.max([nmax, namax])
        tamax = np.max([tmax, tamax])

    # Now do the processing
    for slice in slices:
        time_sec = times[int(slice)]
        time = str(int(time_sec * 1000))  # Use msec for labelling
        if args.save:
            file_prefix = "gpr_" + shotlbl + "_" + time
            fh = open(file_prefix + ".txt", "w")
            h5file_out = "gpr_" + shotlbl + ".h5"
        gplog("\nAnalyzing slice: " + str(slice) + " at time " + time + " ms")
        egrp = profiles.get(str(slice) + "/electrons")
        xn = rm_nan(egrp.get("density_fit/rho_tor_norm")[()])
        yn = rm_nan(egrp.get("density_fit/measured")[()])
        yen = rm_nan(egrp.get("density_fit/measured_error_upper")[()])
        yen *= np.double(args.errorbar_factor)
        xt = rm_nan(egrp.get("temperature_fit/rho_tor_norm")[()])
        yt = rm_nan(egrp.get("temperature_fit/measured")[()])
        yet = rm_nan(egrp.get("temperature_fit/measured_error_upper")[()])
        yet *= np.double(args.errorbar_factor)

        # Sanity check
        if not xn.size == yn.size:
            continue
        if not xt.size == yt.size:
            continue

        # Do not pass in args.plot because we have our own plotting
        density = GPTSFit(
            xn,
            yn,
            yen,
            method=args.method,
            outlierMethod=args.outliermethod,
            constrainAxisGradient=args.constrainAxisGradient,
            constrainEdgeGradient=args.constrainEdgeGradient,
            optimizer=args.optimizer,
        )
        n_mean, n_var = density.performfit()  # EmpBayes
        gplog("  Printing hyperparameters for density fit")
        density.printHyperparameters(indent="\t")
        if args.save:
            ax = "_ax" if args.constrainAxisGradient else ""
            bf = (
                "_f" + str(args.errorbar_factor)
                if not args.errorbar_factor == 1
                else ""
            )
            om = "_" + args.outliermethod if args.outliermethod is not None else ""
            postfix = ax + bf + om
            density.writeData(
                h5file_out, time=time_sec, dataname="density", postfix=postfix
            )

        temperature = GPTSFit(
            xt,
            yt,
            yet,
            method=args.method,
            outlierMethod=args.outliermethod,
            constrainAxisGradient=args.constrainAxisGradient,
            constrainEdgeGradient=args.constrainEdgeGradient,
            optimizer=args.optimizer,
        )
        temperature = GPTSFit(
            xt,
            yt,
            yet,
            method=args.method,
            outlierMethod=args.outliermethod,
            constrainAxisGradient=args.constrainAxisGradient,
            constrainEdgeGradient=args.constrainEdgeGradient,
        )
        t_mean, t_var = temperature.performfit()  # EmpBayes
        gplog("  Printing hyperparameters for temperature fit")
        temperature.printHyperparameters(indent="\t")
        if args.save:
            temperature.writeData(
                h5file_out, time=time_sec, dataname="temperature", postfix=postfix
            )

        gplog("  Summarizing pedestal information:")
        pedloc, pedwidth = density.getPedestalInfo()
        gplog("\tDensity pedestal location: " + str(pedloc))
        gplog("\tDensity pedestal width:    " + str(pedwidth))
        pedloc, pedwidth = temperature.getPedestalInfo()
        gplog("\tTemperature pedestal location: " + str(pedloc))
        gplog("\tTemperature pedestal width:    " + str(pedwidth))

        if args.plot:
            # Plot the samples as well
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
            fig.suptitle(shotlbl + ": " + time + " ms")
            plot_gpfit(density, ax1, "Density", namax, args.no_plot_errorbars, True)
            plot_gpfit(
                temperature, ax2, "Temperature", tamax, args.no_plot_errorbars, True
            )
            # plt.tight_layout()
            if args.save:
                plt.savefig(file_prefix + ".png", dpi=600)
            else:
                plt.show()
        plt.close("all")  # Remove limitation on # of figs

    hf.close
    return


def plot_gpfit(gpobj, ax, label, vmax, no_plot_errorbars, plot_samples):
    """Plot a single GPTSFit object.   This takes in a matplotlib object to allow
    for multiframe layouts
    """
    # setting the global limit for a file is a bit convoluted
    ym = np.format_float_scientific(vmax, precision=0)
    ymax = np.double(ym) + np.double("1e" + ym.split("e")[1])

    ax.set_ylim(0.0, ymax)
    ax.set_title(label)
    if no_plot_errorbars:
        ax.plot(gpobj.xdata, gpobj.ydata, "o", label="data")
    else:
        ax.errorbar(
            gpobj.xdata,
            gpobj.ydata,
            yerr=gpobj.yerrdata,
            linestyle="None",
            marker="o",
            label="data",
        )
    ax.plot(gpobj.X, gpobj.mean, "r-", label="mean fit")
    ax.legend()

    # plot some sample fit curves to give UQ
    if plot_samples:
        samples = gpobj.getSamples(50)
        ax.plot(gpobj.X, samples, "g-", linewidth=0.5, alpha=0.1)

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


def parse_gpfit_file():
    desc = "Perform GPR on h5 data file"
    parser = parse_gpfit(desc)
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
        "-f",
        "--errorbar_factor",
        help="Multiply the error bars by this factor",
        dest="errorbar_factor",
        default=1.0,
    )
    parser.add_argument(
        "-b",
        "--no_plot_errorbars",
        help="Turn off errorbars and plot just the data",
        dest="no_plot_errorbars",
        action="store_true",
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
    parser = parse_gpfit_file()
    args = parser.parse_args()

    if len(args.files) > 1:
        # Need to think about multiprocessing here
        print("Batch processing mode: TODO")
    else:
        fname = args.files[0]
        slices = get_slices(fname, args)
        if slices:
            fit_omas_core_profiles(fname, slices, args)

    return


if __name__ == "__main__":
    main()
