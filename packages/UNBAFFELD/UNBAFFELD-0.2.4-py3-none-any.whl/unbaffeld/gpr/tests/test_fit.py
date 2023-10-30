import numpy as np
import matplotlib.pyplot as plt
import os
import sys

curdir = os.path.dirname(os.path.abspath(__file__))
pardir = os.path.abspath(os.path.join(curdir, ".."))
sys.path.append(pardir)
wfldir = os.path.abspath(os.path.join(pardir, "workflow"))
sys.path.append(wfldir)

from syndata import efitAiData
from gpfit import GPTSFit


def test_syndata_fit():
    myprof = efitAiData(wfldir + "/hmode.yml")
    myprof.add_syndata()
    myprof.add_outliers()
    norm = 1e18
    myprof.profile *= norm
    x = myprof.r
    N = len(x)
    yerr = (1.11 - x) * norm  # np.random.uniform(0.01,2.0,N)
    y = np.zeros(N)
    for i in range(N):
        y[i] = myprof.profile[i] + np.random.normal(0.0, yerr[i])

    # remove first point
    y = np.delete(y, 0)
    x = np.delete(x, 0)
    yerr = np.delete(yerr, 0)
    N = len(x)

    # do fit
    GPRfit = GPTSFit(
        x, y, yerr, method="EmpBayes", outlierMethod="None", plot=False
    )  # yerr=yerr
    m, v = GPRfit.performfit()
    xx = GPRfit.X.flatten()

    samples = GPRfit.getSamples(50)

    params = GPRfit.getHyperparameters()
    pedloc, pedwidth = GPRfit.getPedestalInfo()
    print(params)

    # fig = plt.figure()
    # ax = plt.subplot(111)
    # ax.errorbar(x,y,yerr,marker='o',mfc='black',mec='black',linestyle='')
    # plt.plot(x,y,'ko')
    # ax.plot(xx, m, '-', color='red')
    # ax.plot([params[7],params[7]],[0,np.max(m)],'g--')
    # ax.plot([params[9],params[9]],[0,np.max(m)],'g--')
    # ax.fill_between(xx, m - 2.*np.sqrt(v), m + 2.*np.sqrt(v), color='red', alpha=0.2)
    # ax.plot(xx, samples, 'g-', alpha=0.1)
    # plt.show()

    yp = np.gradient(m, xx)
    ypp = np.gradient(yp, xx)
    pstart = xx[np.argmin(ypp)]
    pend = xx[np.argmax(ypp)]
    print("pedestal width: ", (pend - pstart) / 4.0, GPRfit.pedwid)
    xped = xx[np.argmin(yp)]
    print("pedestal location: ", xped, GPRfit.pedloc)
