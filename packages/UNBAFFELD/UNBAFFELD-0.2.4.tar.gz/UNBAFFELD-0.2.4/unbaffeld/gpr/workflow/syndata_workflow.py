#!/usr/bin/env python
"""
Workflow script -- just quickly hardcode the parameters required for generating
the profiles for the GPR paper
"""

import syndata
import yaml


scan_n_edge = [0.01, 0.05, 0.10, 0.20]
scan_w_ped = [0.010, 0.015, 0.020]
scan_w_noise = [0.10, 0.15, 0.20, 0.25, 0.33]
scan_shift_noise = [0.00, 0.02, 0.05, 0.10]
scan_n_outliers = [0, 3, 5, 10]
scan_f_outliers = [2.0, 3.0, 4.0]
scan_w_itb = [0.010, 0.015, 0.020]
scan_n_itb = [0.5, 1.0, 1.5]


def gen_hmode():
    """
    H-mode scan
    """
    with open("hmode.yml") as filestr:
        hmode_conf = yaml.load(filestr, Loader=yaml.Loader)

    lmode_conf["itb"] = False
    for n in scan_n_edge:
        hmode_conf["n_edge"] = n
        nlbl = "_n" + str(n)
        for w in scan_w_ped:
            hmode_conf["w_ped"] = w
            wlbl = "_w" + str(w)
            for v in scan_w_noise:
                hmode_conf["w_noise"] = v
                vlbl = "_v" + str(v)
                for s in scan_shift_noise:
                    hmode_conf["shift_noise"] = s
                    slbl = "_s" + str(s)
                    for o in scan_n_outliers:
                        hmode_conf["n_outliers"] = o
                        olbl = "_o" + str(o)
                        for f in scan_f_outliers:
                            hmode_conf["f_outlier"] = f
                            flbl = "_f" + str(f)

                            myprof = syndata.efitAiData(
                                config_file=None, config_dict=hmode_conf
                            )
                            myprof.add_syndata()
                            myprof.add_outliers()
                            fname = (
                                "hmode"
                                + nlbl
                                + wlbl
                                + vlbl
                                + slbl
                                + olbl
                                + flbl
                                + ".h5"
                            )
                            print(fname)
                            myprof.write(fname)

    return


def gen_lmode():
    """
    L-mode scan
    """
    with open("lmode.yml") as filestr:
        lmode_conf = yaml.load(filestr, Loader=yaml.Loader)

    lmode_conf["hd_ped"] = True
    lmode_conf["itb"] = False
    for v in scan_w_noise:
        lmode_conf["w_noise"] = v
        vlbl = "_v" + str(v)
        for s in scan_shift_noise:
            lmode_conf["shift_noise"] = s
            slbl = "_s" + str(s)
            for o in scan_n_outliers:
                lmode_conf["n_outliers"] = o
                olbl = "_o" + str(o)
                for f in scan_f_outliers:
                    lmode_conf["f_outlier"] = f
                    flbl = "_f" + str(f)

                    myprof = syndata.efitAiData(
                        config_file=None, config_dict=lmode_conf
                    )
                    myprof.add_syndata()
                    myprof.add_outliers()
                    fname = "lmode" + vlbl + slbl + olbl + flbl + ".h5"
                    print(fname)
                    myprof.write(fname)

    return


def gen_itb():
    """
    ITB scan
    """
    with open("hmode.yml") as filestr:
        itb_conf = yaml.load(filestr, Loader=yaml.Loader)

    itb_conf["itb"] = True
    for n in scan_n_itb:
        itb_conf["n_itb"] = n
        nlbl = "_n" + str(n)
        for w in scan_w_itb:
            itb_conf["w_itb"] = w
            wlbl = "_w" + str(w)
            for v in scan_w_noise:
                itb_conf["w_noise"] = v
                vlbl = "_v" + str(v)
                for s in scan_shift_noise:
                    itb_conf["shift_noise"] = s
                    slbl = "_s" + str(s)
                    for o in scan_n_outliers:
                        itb_conf["n_outliers"] = o
                        olbl = "_o" + str(o)
                        for f in scan_f_outliers:
                            itb_conf["f_outlier"] = f
                            flbl = "_f" + str(f)

                            myprof = syndata.efitAiData(
                                config_file=None, config_dict=itb_conf
                            )
                            myprof.add_syndata()
                            myprof.add_outliers()
                            fname = (
                                "itb" + nlbl + wlbl + vlbl + slbl + olbl + flbl + ".h5"
                            )
                            print(fname)
                            myprof.write(fname)

    return


def main():
    """
    Set up profiles and write them out
    """
    # gen_hmode()
    gen_lmode()
    # gen_itb()


if __name__ == "__main__":
    main()
