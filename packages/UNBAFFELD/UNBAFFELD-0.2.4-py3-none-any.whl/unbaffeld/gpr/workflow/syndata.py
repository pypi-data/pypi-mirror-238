#!/usr/bin/env python
"""
Class that generates analytic parameterized profiles  and then parameterizing
synthetic data around it.
"""

import optparse
import h5py

# from pathlib import Path

# from icecream import ic
import os
from functools import wraps

# import logging
# from rich.logging import RichHandler
import numpy as np
import yaml
import matplotlib.pyplot as plt


# This doesn't work well with matplotlib as somewhere along the way the change
# the logging level to DEBUG
# logging.basicConfig(
#    level="NOTSET",
#    format="%(message)s",
#    datefmt="[%X]",
#    handlers=[RichHandler(rich_tracebacks=True)],
# )


def ealog(func):
    """
    Enable an automatic logger
    """

    @wraps(func)
    def wrapper(self, *args):
        # self._logger.debug("Entering " + func.__name__)
        # print("Entering " + func.__name__)
        return func(self, *args)

    return wrapper


class efitAiData:
    """Main class"""

    def __init__(self, config_file=None, config_dict=None):
        """Set up the profiles.  Can use configuration file (yaml) or a
        dictionary with the parameters"""
        # self._logger = logging.getLogger("rich")

        if config_file:
            if not os.path.exists(config_file):
                print("File does not exist: ", config_file)
                return
            with open(config_file) as filestr:
                config_dict = yaml.load(filestr, Loader=yaml.Loader)
            self._config_root = os.path.splitext(config_file)[0]
        else:
            self._config_root = "syndata"

        # Save the configuration (but make internal)
        self._config_dict = config_dict

        # Some basic sanity checks
        if "profile_type" not in config_dict:
            print("Error in config: require profile_type")
            return

        if config_dict["profile_type"] not in ["Lmode", "Hmode"]:
            print("Do not recognize profile type")
            return

        # Common parameters
        n_o = np.double(config_dict["n_o"])
        n_edge = np.double(config_dict["n_edge"])
        a1 = np.double(config_dict["a1"])
        a2 = np.double(config_dict["a2"])

        # check if we want a high point density in the pedestal
        hdped = config_dict["hd_ped"] if "hd_ped" in config_dict else False

        # 0 -> 1 is the "normalized" in normalized poloidal flux.
        # 1=last closed flux surface
        if not hdped:
            self.r = np.linspace(0, 1.0, int(config_dict["NR"]), endpoint=False)
        else:
            self.r = np.linspace(0, 0.85, int(config_dict["NR"]), endpoint=False)
            self.r = np.append(
                self.r,
                np.linspace(0.85, 1.0, int(config_dict["NR"]), endpoint=False),
            )

        # check if h-mode, if so get parameters
        if config_dict["profile_type"] == "Hmode":
            r_ped = np.double(config_dict["r_ped"])
            w_ped = np.double(config_dict["w_ped"])
            n_ped = np.double(config_dict["n_ped"])

        # check if itb, if so get parameters
        if "itb" not in config_dict:
            has_itb = False
        else:
            has_itb = config_dict["itb"]

        if has_itb is True:
            r_itb = np.double(config_dict["r_itb"])
            w_itb = np.double(config_dict["w_itb"])
            n_itb = np.double(config_dict["n_itb"])

        # fill in SOL r=[1.0,1.1]
        rsol = np.linspace(1.001, 1.1, int(0.1 * len(self.r)))
        self.r = np.append(self.r, rsol)

        # setup function for desired profile
        if config_dict["profile_type"] == "Hmode":
            if has_itb:
                self.fn = (
                    lambda myr: self.__base_profile(myr, n_o, n_edge, a1, a2)
                    + self.__add_ped(myr, r_itb, w_itb, n_itb)
                    + self.__add_ped(myr, r_ped, w_ped, n_ped)
                )
            else:
                self.fn = lambda myr: self.__base_profile(
                    myr, n_o, n_edge, a1, a2
                ) + self.__add_ped(myr, r_ped, w_ped, n_ped)
        else:
            if has_itb:
                self.fn = lambda myr: self.__base_profile(
                    myr, n_o, n_edge, a1, a2
                ) + self.__add_ped(myr, r_itb, w_itb, n_itb)
            else:
                self.fn = lambda myr: self.__base_profile(myr, n_o, n_edge, a1, a2)

        # substitute our r-axis into the function to get the model data profile
        self.profile = self.fn(self.r)

    def __base_profile(self, r, n_o, n_edge, a1, a2):
        # base profile for L-mode - can add pedestals from here for H-mode and ITB
        return np.piecewise(
            r,
            [r < 1.0, r >= 1.0],
            [
                lambda x: (n_o - n_edge) * (1.0 - x**a1) ** a2 + n_edge,
                lambda x: n_edge,
            ],
        )

    # return np.where(r < 1.0, (n_o - n_edge) * (1. - r ** a1) ** a2 + n_edge, n_edge)

    def __add_ped(self, r, r_ped, w_ped, n_ped):
        # pedestal profile at r_ped with width w_ped
        return n_ped * 0.5 * (1.0 - np.tanh((r - r_ped) / (w_ped)))

    @ealog
    def add_syndata(self):
        w_noise = np.double(self._config_dict["w_noise"])
        if "shift_noise" in self._config_dict:
            shift_noise = np.double(self._config_dict["shift_noise"])
        else:
            shift_noise = 0.0
        shift_profile = self.profile * (1.0 + shift_noise)
        self.syndata = np.random.normal(shift_profile, w_noise)

    @ealog
    def add_outliers(self):
        """
        Add some synthetic outliers.  This is done by randomly
        choosing points in the syndata array and making it lie outside of the
        random distribution.
        """
        if "n_outliers" not in self._config_dict:
            return

        n_outliers = int(self._config_dict["n_outliers"])
        if n_outliers == 0:
            return
        if not hasattr(self, "syndata"):
            print("No syndata -- no outlier")
            return

        w_noise = np.double(self._config_dict["w_noise"])
        f_outlier = np.double(self._config_dict["f_outlier"])

        for i in np.random.choice(self.r.size, n_outliers):
            # Keep the sign random
            sign = np.sign(self.syndata[i] - self.profile[i])
            self.syndata[i] = self.profile[i] * (1.0 + sign * f_outlier * w_noise)

    def calc_error(self, x, yfit, method="Pearson"):
        """
        Calculate the error between the supplied fit and the model
        on the provided x-axis - uses Pearson least squares calculation
        """
        if method == "Pearson":
            return np.sum((self.fn(x) - yfit) ** 2 / self.fn(x))
        elif method == "L2Norm":
            return np.sqrt(np.sum((self.fn(x) - yfit) ** 2))
        elif method == "MSE":
            return np.mean((self.fn(x) - yfit) ** 2)
        elif method == "RMSE":
            return np.sqrt(np.mean((self.fn(x) - yfit) ** 2))

    def evaluateFn(self, x):
        """
        Evalulates the underlying profile function on a given axis
        """
        return self.fn(x)

    @ealog
    def plot(self):
        """
        Plot profiles and other data as available
        """
        plt.plot(self.r, self.profile)
        if hasattr(self, "syndata"):
            plt.plot(self.r, self.syndata, "o")
        plt.show()

    @ealog
    def write(self, h5FileName=None):
        """
        write out the data to an hdf5 file
        """
        if not h5FileName:
            h5FileName = self._config_root + ".h5"
        hf = h5py.File(h5FileName, mode="w")
        hf.attrs.create("title", "EFIT-AI Synthetic data")
        # VizSchema is for the Visit vs reader
        dataset = hf.create_dataset("r", data=self.r, dtype="d")
        dataset = hf.create_dataset("profile", data=self.profile, dtype="d")
        dataset = hf.create_dataset("syndata", data=self.syndata, dtype="d")
        dataset.attrs.create("vsType", "variableWithMesh")
        dataset.attrs.create("vsNumSpatialDims", 1)
        dataset.attrs.create("vsLabels", "r")

        # write out conf
        h5conf = hf.create_group("conf")
        for key in self._config_dict:
            h5conf.create_dataset(key, data=self._config_dict[key])

        hf.close()


def main():
    """
    Set up profiles and plot them.
    """
    parser = optparse.OptionParser(usage="%prog [options]")
    parser.add_option(
        "-c",
        "--config",
        dest="config_file",
        default=None,
        help="Yaml file with configuration parameters",
    )
    options, args = parser.parse_args()

    myprof = efitAiData(options.config_file)
    myprof.add_syndata()
    myprof.add_outliers()
    myprof.write()
    myprof.plot()


if __name__ == "__main__":
    main()
