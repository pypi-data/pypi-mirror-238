
Gaussian Process Regression
==============================

Introduction
-------------

Traditional method to ``fitting`` a profile :math:`f(\psi)` typically involves
finding a the function that depends on a set of ``parameters`` and
minimizing the error.  For example, one can write :math:`f(\psi) = \sum f_i \alpha_i`,
where :math:`f_i` are the parameters, and :math:`\alpha_i` is the `fitting function`,
and then minimize the error related to the data.  This is the traditional method
of EFIT which uses spline functions for the fitting functions with L-mode
profiles, and splines and a ``tanh`` function for H-mode profiles.  

In the Bayesian view, the process is fundamentally different.  One first
calculates the probability of a function being correct, and the most probable
function is used as that fit.   The advantage of Bayes' theorem in practical
terms is that it easier to compute the probability of the likelihood and prior
distribution than the posterior likelihood.  

The first step that we wish to consider is how to encode the space of all
functions into the prior probability.   Above, we discussed how parameters were used to
parameterize a function.  A similar method is used to explore the distribution
space of the probability functions here.  In PDE's, exploring a functional space
is done using discretizations (e.g., finite difference).  The problem with this
for probability functions is that although we might wish to assume that $\fpsi$
lies within a functional space (e.g., Hilbert space), the data, which is subject
to noise, does not.  Using traditional PDE discretizations would also subject
one to systematic bias in determining the distributions.  Hence, randomized
sampling of the distribution space is generally preferred.  Two methods for
exploring this space are polynomial chaos expansions and stochastic processes.
In both methods, the conversion of the continuum form of the probabilities above
are converted to discrete form. For distributions, *hyperparameters*, denoted $\hyperp$,are
used to explore the probability space for the prior and likelihood functions.

In the context of fitting profiles of fusion data, the discussion of whether a
Gaussian process is stationary or not relates to the characteristic length scale
of the profile, or data, to be inferred.  For H-mode profiles, the short length
scale of the pedestal region motivates the use of non-stationary kernels;
e.g., as used in Chilenski~\cite{chilenski2015}.   Similarly, inferring magnetic
data can be challenging because of rapid changes in the data requiring
non-stationary kernels.
	
The hyperparameters play an important role in GPR, and the choice of
hyperparameters requires special consideration. The simplest approaches is to
pick reasonable values for the hyperparameters that are learned from prior
experiments. In this approach, a large enough data set can overcome a bad choice
of hyperparameters. However, this approach suffers if underlying profile
changes drastically in different experimental regimes or if the amount of
measured data is limited, both of which are case here.  Thus, this approach is
not used in practice.
	
A second approach is the *Empirical Bayesian* where one uses the data to determine 
the optimal hyperparameters.  There is a family of methods in this approach. One method chooses the likelihood
to also be a Gaussian function.  The combination of Gaussian functions in both the likelihood,
and a squared-exponential kernel enables an analytically-tractable method for
maximizing the marginal likelihood.   This method was used in the first introduction of GPR to the.~\cite{svensson2011non}
When the likelihood is not a Gaussian, a closed-form
analytic solution in general is not possible, and one must use numerical methods for this.

A different philosophical approach is the *Full Bayesian* approach in
which the prior distribution is fixed before any data is observed.  In this
approach, the prior and likelihood are still described in terms of
hyperparameters as described above, but the full hyperparameter space is
explored numerically by integrating out the hyperparameters.  Specifically, the
likelihood and prior probability functions in Eq.~\ref{BayesTheorem} are
parameterized in terms of hyperparameters, and then the hyperparameters are
numerically integrated out in a process known as *marginalization*.
There a wide variety of approaches to marginalization or in using partial
approximations to accelerate this integration.   In this paper, we will use
``Markov chain Monte Carlo`` methods (MCMC) to systematically perform the
Bayesian integration.  In the fusion community, Chilenski is a notable paper in
discussion the Full Bayesian technique as well as using non-stationary
hyperparameters.  Empirical Bayesian remains popular however because of the
speed of it as compared to Full Bayesian techniques.  This is discussed in more
detail later.
