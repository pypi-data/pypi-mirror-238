.. _quickstart:

Quickstart
==========

Here we demonstrate GPR on data from DIII-D discharge number 169958.  

This data has Thomson scattering data that has already been processed to be put
onto a toroidal flux grid using OMFIT and stored into an IMAS-compatible file 
with the `core_profiles` IDS.   The data is stored in 
`unbaffeld/data/diii-d/169958_profiles.h5`.   For convenience, we will demonstrate
running this from the `unbaffeld/gpr` directory.

The command we use is `unbaffeld/gpr/gpfit_file.py`, which is just a convenient 
wrapper for applying `gpfit.py` to files of this type.

Let's start by examining all of the time slices in this file::

      ➜ gpfit_file.py -l ../data/diii-d/169958_profiles.h5                                                                                                      Time slices in:  ../data/diii-d/169958_profiles.h5
      0, 2.4
      1, 2.5
      2, 2.6
      3, 2.7
      4, 2.8
      5, 2.9
      6, 3.0

In this tutorial, we will use time slice 1 corresponding to `t=2.5 sec`.   
Let's start by doing a naive approach (to see the full list of options, 
use the `-h` flag)::

      ➜ gpfit_file.py -s 1 -p ../data/diii-d/169958_profiles.h5
      GPR Fit options used are:
              Hyperparameter choice method: EmpBayes [EmpBayes]
              Outlier Method: None [None varyErrors]
              Axis Constraint: False [True False]
              Edge Constraint: False [True False]
              Optimizer: bfgs [bfgs diffev]

      Analyzing slice: 1 at time 2500 ms
        Printing hyperparameters for density fit
              kernel1 length scale:  -0.357187406955555
              kernel1 scale:  0.3393577454901789
              kernel2 length scale:  1.3176332758203382
              kernel2 scale:  -5.24934418089969
              kernel3 length scale:  -2.1179052801496003
              kernel3 scale:  -2.1470178263472803
              changepoint 1 location:  0.9594459279357898
              changepoint 2 location:  1.0
        Printing hyperparameters for temperature fit
              kernel1 length scale:  -0.3669944418601537
              kernel1 scale:  -0.5804080348229047
              kernel2 length scale:  -0.5291338194732252
              kernel2 scale:  -5.181269484752381
              kernel3 length scale:  -0.7111624532702242
              kernel3 scale:  -5.181269484752381
              changepoint 1 location:  0.9587705560931057
              changepoint 2 location:  1.15
        Summarizing pedestal information:
              Density pedestal location: 0.9620754907467133
              Density pedestal width:    0.004509728862875234
              Temperature pedestal location: 0.9560625189295463
              Temperature pedestal width:    0.00901945772575044 

You should see a figure like the following.

.. image:: figures/gpr_DIII-D_169958_2500_gpr0.png
    :alt: First GPR figure

This isn't bad, but the density gradient on axis is not zero.   Let's fix that::

     ➜ gpfit_file.py -a -s 1 -p ../data/diii-d/169958_profiles.h5

This gives

.. image:: figures/gpr_DIII-D_169958_2500_gpr1.png
    :alt: Second GPR figure

The density is looking pretty good.  The variations show some wild variations
in the edge, and if you zoom into the top of the pedestal, it looks like there
might be some overfitting.  Let's model the data has having heteroskedatic
noise to see if that prevents the overfitting::

    ➜ gpfit_file.py -o varyErrors -a -s 1 -p ../data/diii-d/169958_profiles.h5

This gives

.. image:: figures/gpr_DIII-D_169958_2500_gpr2.png
    :alt: Third GPR figure

This looks good.    Let's see if the error bars from the files affect the results. 
To do so, we increase the error bars by a factor of 2::

    ➜ gpfit_file.py -f 2.0  -o varyErrors -a -s 1 -p ../data/diii-d/169958_profiles.h5

This gives

.. image:: figures/gpr_DIII-D_169958_2500_gpr3.png
    :alt: Fourth GPR figure

That's interesting, but let's go back and process all of the slices in the
data file while `S` aving the results of each slice to a file::

    ➜ gpfit_file.py -o varyErrors -a -S -p ../data/diii-d/169958_profiles.h5

This produces the following files::

  DIII-D_169958_summary.txt   gpr_DIII-D_169958_2500.png  gpr_DIII-D_169958_2700.txt  gpr_DIII-D_169958_3000.png
  gpr_DIII-D_169958_2000.png  gpr_DIII-D_169958_2500.txt  gpr_DIII-D_169958_2800.png  gpr_DIII-D_169958_3000.txt
  gpr_DIII-D_169958_2000.txt  gpr_DIII-D_169958_2600.png  gpr_DIII-D_169958_2800.txt
  gpr_DIII-D_169958_2400.png  gpr_DIII-D_169958_2600.txt  gpr_DIII-D_169958_2900.png
  gpr_DIII-D_169958_2400.txt  gpr_DIII-D_169958_2700.png  gpr_DIII-D_169958_2900.txt





     

