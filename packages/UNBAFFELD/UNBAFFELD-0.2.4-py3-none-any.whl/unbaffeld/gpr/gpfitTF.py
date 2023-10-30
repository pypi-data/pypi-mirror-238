#!/usr/bin/env python3.7
"""
Class that uses Gaussian Process Regression to perform a fit of Thomson
scattering data found in provided .h5 files.
"""

import argparse
import h5py
import numpy as np
import matplotlib.pyplot as plt

import gpflow as GPflow
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability import distributions as tfd
from gpflow.optimizers import NaturalGradient
from gpflow import set_trainable

# import syndata
# import importlib.util
# spec = importlib.util.spec_from_file_location("efitAiData",
#                                                "./synthetic_data/syndata.pyc")
# efitAiData = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(efitAiData)


class GPTSFit(object):
    """
    A class for performing Gaussian-process regression in one dimension for
    Thomson scattering profiles.  Gaussian-process regression (GPR) is a
    non-parametric regression technique, which can fit arbitrarily spaced data
    in any number of dimensions.
    :param datafile: \
        The name and path of the h5 file that contains the Thomson data.
    :param method: \
        The method to use for the fit. Options are: EmpBayes, MCMC
    :param outlierMethod: \
        The method for handling outliers. Options are: None, StudentT, Detect
    :param plot: \
        Option to show plots. Options are True/False
    """

    def __init__(
        self, xx, yy, yerr=None, method="EmpBayes", outlierMethod="None", plot=False
    ):
        # store the input parameters
        self.optmethod = method
        self.outliermethod = outlierMethod
        self.plot = plot
        self.normalize = True

        # read datafile to store data
        self.x = np.array(xx).flatten()
        self.y = np.array(yy).flatten()
        if yerr is not None:
            self.dataerrors = True
            self.yerr = np.array(yerr).flatten()
        else:
            self.dataerrors = False
            self.yerr = np.zeros(len(self.y))

        if self.normalize:
            self.y0 = np.max(self.y)
            self.y /= self.y0
            self.yerr /= self.y0
            self.m0 = np.mean(self.y)
            self.y -= self.m0

        # add a point at psi=0 if it doesn't exist
        if self.x[0] > 0.0:
            self.x = np.insert(self.x, 0, [0.0])
            self.y = np.insert(self.y, 0, [self.y[0]])
            self.yerr = np.insert(self.yerr, 0, [self.yerr[0]])

        if plot:
            plt.errorbar(self.x, self.y, self.yerr)
            plt.show()

        self.x = self.x[:, None]
        self.y = self.y[:, None]
        self.yerr = self.yerr[:, None]

        # new axis for fit
        self.X = np.linspace(0.0, np.max(self.x), 200)
        self.X = self.X[:, None]

        # GPflow settings
        GPflow.config.set_default_float(np.float64)
        GPflow.config.set_default_jitter(1e-8)
        self.f64 = GPflow.utilities.to_default_float

        # setup the kernel
        k1 = GPflow.kernels.Matern52(lengthscales=1.0)
        k2 = GPflow.kernels.Matern52(lengthscales=0.1)
        self.kernel = GPflow.kernels.ChangePoints(
            [k1, k2, k1], locations=[0.95, 1.0], steepness=50.0
        )

        # setup likelihood
        if self.outliermethod == "StudentT":
            self.likelihood = MyStudentT(1.0, 1.5)
        else:
            if self.dataerrors:
                # self.likelihood = GPflow.likelihoods.Gaussian(variance=self.yerr)
                self.likelihood = HeteroskedasticGaussian()
            elif self.optmethod == "MCMC":
                self.likelihood = GPflow.likelihoods.Gaussian()
            else:
                self.likelihood = GPflow.likelihoods.Gaussian(
                    scale=GPflow.functions.Polynomial(degree=4)
                )

        # setup the model
        if self.optmethod == "MCMC":
            self.model = GPflow.models.GPMC(
                (self.x, self.y), self.kernel, self.likelihood
            )  # np.hstack([self.y, self.yerr])), \
        elif self.optmethod == "EmpBayes":
            if self.outliermethod == "StudentT":
                print("Cannot use non-gaussian likelihood w/ emperical Bayes")
                raise ValueError
            if self.dataerrors:
                self.model = GPflow.models.VGP(
                    (self.x, np.hstack([self.y, self.yerr])),
                    kernel=self.kernel,
                    likelihood=self.likelihood,
                    num_latent_gps=1,
                )
            else:
                self.model = GPflow.models.GPR(
                    (self.x, self.y),
                    self.kernel,
                    likelihood=self.likelihood,
                    mean_function=None,
                )

        else:
            print("Model choice not valid. Must be EmpBayes or MCMC.")
            return

        # setup priors for kernel, likelihood, etc.
        self.model.kernel.locations = [self.f64(0.95), self.f64(1.0)]
        self.model.kernel.steepness = self.f64(50.0)
        self.model.kernel.kernels[0].variance.prior = tfd.Gamma(
            self.f64(1.0), self.f64(2.0)
        )
        self.model.kernel.kernels[1].variance.prior = tfd.Gamma(
            self.f64(1.0), self.f64(2.0)
        )
        self.model.kernel.kernels[0].lengthscales.prior = tfd.Uniform(
            low=self.f64(0.001), high=self.f64(5.0)
        )
        self.model.kernel.kernels[1].lengthscales.prior = tfd.Uniform(
            low=self.f64(0.001), high=self.f64(5.0)
        )

        if self.outliermethod == "StudentT":
            self.model.likelihood.scale.prior = tfd.Gamma(self.f64(1.0), self.f64(2.0))
            self.model.likelihood.df.prior = tfd.Uniform(
                low=self.f64(1.0), high=self.f64(30.0)
            )
        # else:
        #     #self.model.likelihood.variance = np.max(self.yerr)
        #     if (not self.dataerrors):
        #         self.model.likelihood.variance.prior = tfd.Gamma(self.f64(1.), self.f64(2.))# tfd.Uniform(low=self.f64(1.0),high=self.f64(30.0)) #tfd.Uniform(low=self.f64(1e-4),high=self.f64(2.)) #

    @tf.function
    def run_chain_fn(self):
        return tfp.mcmc.sample_chain(
            num_results=self.num_samples,
            num_burnin_steps=self.num_burnin_steps,
            current_state=self.hmc_helper.current_state,
            kernel=self.adaptive_hmc,
            trace_fn=lambda _, pkr: pkr.inner_results.is_accepted,
        )

    def __gpflowfit(self):
        if self.dataerrors:
            natgrad = NaturalGradient(gamma=1.0)
            adam = tf.optimizers.Adam()

            set_trainable(self.model.q_mu, False)
            set_trainable(self.model.q_sqrt, False)

            for _ in range(ci_niter(100)):
                natgrad.minimize(
                    self.model.training_loss, [(self.model.q_mu, self.model.q_sqrt)]
                )
                adam.minimize(self.model.training_loss, self.model.trainable_variables)

            mean, var = self.model.predict_f(self.X)
            if self.normalize:
                mean += self.m0
                mean *= self.y0
                var *= self.y0 * self.y0
        else:
            # optimize hyperparameters
            opt = GPflow.optimizers.Scipy()
            opt_logs = opt.minimize(
                self.model.training_loss,
                self.model.trainable_variables,
                options=dict(maxiter=3000),
            )

            mean, var = self.model.predict_f(self.X)
            if self.normalize:
                mean += self.m0
                mean *= self.y0
                var *= self.y0 * self.y0

        # print_summary(self.model)
        return np.array(mean[:, 0]), np.array(var[:, 0])

    def __gpflowfitMCMC(self):
        # get initial guess at parameters
        optimizer = GPflow.optimizers.Scipy()
        maxiter = ci_niter(3000)
        _ = optimizer.minimize(
            self.model.training_loss,
            self.model.trainable_variables,
            options=dict(maxiter=maxiter),
        )

        # Run the MCMC
        self.num_burnin_steps = ci_niter(500)
        self.num_samples = ci_niter(2000)

        # Note that here we need model.trainable_parameters,
        # not trainable_variables - only parameters can have priors!
        self.hmc_helper = GPflow.optimizers.SamplingHelper(
            self.model.log_posterior_density, self.model.trainable_parameters
        )

        hmc = tfp.mcmc.HamiltonianMonteCarlo(
            target_log_prob_fn=self.hmc_helper.target_log_prob_fn,
            num_leapfrog_steps=10,
            step_size=0.01,
        )

        self.adaptive_hmc = tfp.mcmc.SimpleStepSizeAdaptation(
            hmc,
            num_adaptation_steps=int(0.8 * self.num_burnin_steps),
            target_accept_prob=self.f64(0.75),
            adaptation_rate=0.1,
        )  #

        samples, _ = self.run_chain_fn()
        self.samples = samples
        f_samples = []
        for i in range(0, self.num_samples, 50):
            for var, v_samples in zip(self.hmc_helper.current_state, samples):
                var.assign(v_samples[i])
            if self.normalize:
                f = self.model.predict_f_samples(self.X, 1)
                f += self.m0
                f *= self.y0
                f_samples.append(f)
        f_samples = np.vstack(f_samples)
        return np.mean(f_samples[:, :, 0], 0), np.var(f_samples[:, :, 0], 0)

    def performfit(self):
        success = False
        jitter = 1.0e-10
        while not success:
            GPflow.config.set_default_jitter(jitter)
            try:
                if self.dataerrors:
                    self.model = GPflow.models.VGP(
                        (self.x, np.hstack([self.y, self.yerr])),
                        kernel=self.kernel,
                        likelihood=self.likelihood,
                        num_latent_gps=1,
                    )
                else:
                    self.model = GPflow.models.GPR(
                        (self.x, self.y),
                        self.kernel,
                        likelihood=self.likelihood,
                        mean_function=None,
                    )
                if self.optmethod == "MCMC":
                    self.mean, self.variance = self.__gpflowfitMCMC()
                else:
                    self.mean, self.variance = self.__gpflowfit()
                success = True
            except:
                success = False
                jitter *= 10.0
                print("fit failed, changing jitter to ", jitter)
                self.mean = np.zeros(self.X.size)
                self.variance = np.zeros(self.X.size)
                self.dataerrors = False
                if jitter > 1e-2:
                    break

        self.err = np.sqrt(np.abs(self.variance)) / 2.0

        if self.plot:
            plt.plot(self.x, self.y, "o", label="data")
            plt.plot(self.X, self.mean, "r-", label="mean fit")
            plt.legend()
            plt.show()

        plt.plot(self.x, self.y0 * (self.y + self.m0), "o", label="data")
        plt.plot(self.X, self.mean, "r-", label="mean fit")
        plt.legend()
        plt.savefig("fit.png", dpi=300)
        plt.close()

        # fit the pedestal location and width
        xx = self.X.flatten()
        xwin = np.where((xx < 1.05) * (xx > 0.9))
        xx = xx[xwin]
        yp = np.gradient(self.mean.flatten()[xwin], xx)
        ypp = np.gradient(yp, xx)
        self.pedloc = xx[np.argmin(yp)]
        self.pedwid = np.abs(xx[np.argmax(ypp)] - xx[np.argmin(ypp)]) / 4.0

        return self.mean, self.variance

    def getSamples(self, N):
        # get N sample fits from the model
        f_samples = []
        if self.optmethod == "MCMC":
            for i in range(0, self.num_samples, self.num_samples // N):
                for var, v_samples in zip(self.hmc_helper.current_state, self.samples):
                    var.assign(v_samples[i])
                f = self.model.predict_f_samples(self.X, 1)
                f_samples.append(f)
            f_samples = np.vstack(f_samples)
        else:
            f_samples = self.model.predict_f_samples(self.X, N)

        if self.normalize:
            f_samples += self.m0
            f_samples *= self.y0

        return np.array(f_samples[:, :, 0]).T

    # TODO:  Put this into a utility module that both routines can share
    def writeData(self, filename, time, dataname):
        # name for group for fit data
        fitstring = "_fit_" + self.optmethod + "_" + self.outliermethod
        vfitstring = "_fit_variance_" + self.optmethod + "_" + self.outliermethod
        pfitstring = "_fit_psi_" + self.optmethod + "_" + self.outliermethod
        pedfitstring = "_fit_ped_" + self.optmethod + "_" + self.outliermethod
        widfitstring = "_fit_wid_" + self.optmethod + "_" + self.outliermethod

        # open file
        self.openh5file = h5py.File(filename, "a")

        # write mean, variance, profile, and axis
        grpnm = "thomson_scattering/profiles/" + time
        if grpnm in self.openh5file:
            h5fit = self.openh5file[grpnm]
        else:
            h5fit = self.openh5file.create_group(grpnm)

        try:
            del h5fit[dataname + fitstring]
        except:
            pass

        try:
            del h5fit[dataname + vfitstring]
        except:
            pass

        try:
            del h5fit[dataname + pfitstring]
        except:
            pass

        try:
            del h5fit[dataname + widfitstring]
        except:
            pass

        try:
            del h5fit[dataname + pedfitstring]
        except:
            pass

        h5fit[dataname + fitstring] = self.mean.T.flatten()
        h5fit[dataname + vfitstring] = self.err.T.flatten()
        h5fit[dataname + pfitstring] = self.X.T.flatten()
        h5fit[dataname + widfitstring] = self.pedwid
        h5fit[dataname + pedfitstring] = self.pedloc
        self.openh5file.close()


def main():
    """
    Read profile from provided .h5 file and fit.
    """
    parser = argparse.ArgumentParser(usage="%prog [options]")
    parser.argument_option(
        "-d",
        "--data",
        dest="input_data_file",
        default=None,
        help="h5 data file containing Thomson profile",
    )
    parser.argument_option(
        "-m",
        "--method",
        dest="method",
        default="MCMC",
        help="method to choose hyperparameter values: MCMC or EmpBayes",
    )
    parser.argument_option(
        "-o",
        "--outliers",
        dest="outliermethod",
        default="StudentT",
        help="method for handling outliers: None, StudentT, or Detect",
    )
    parser.argument_option(
        "-p",
        "--plot",
        dest="plot",
        default="False",
        help="flag to show plots: True or False",
    )
    args = parser.parse_args()

    GPRfit = GPTSFit(
        args.input_data_file, args.method, args.kernel, args.outliermethod, True
    )
    _, _ = GPRfit.performfit()  # EmpBayes


# Define custom likelihood classes
from gpflow.likelihoods.base import ScalarLikelihood
from gpflow.base import Parameter
from gpflow.utilities import positive
from gpflow import logdensities


class HeteroskedasticGaussian(GPflow.likelihoods.Likelihood):
    def __init__(self, **kwargs):
        # this likelihood expects a single latent function F, and two columns in the data matrix Y:
        super().__init__(1, latent_dim=1, observation_dim=2, **kwargs)

    def _log_prob(self, F, Y):
        # log_prob is used by the quadrature fallback of variational_expectations and predict_log_density.
        # Because variational_expectations is implemented analytically below, this is not actually needed,
        # but is included for pedagogical purposes.
        # Note that currently relying on the quadrature would fail due to https://github.com/GPflow/GPflow/issues/966
        Y, NoiseVar = Y[:, 0], Y[:, 1]
        return GPflow.logdensities.gaussian(Y, F, NoiseVar)

    def _variational_expectations(self, Fmu, Fvar, Y):
        Y, NoiseVar = Y[:, 0], Y[:, 1]
        Fmu, Fvar = Fmu[:, 0], Fvar[:, 0]
        return (
            -0.5 * np.log(2 * np.pi)
            - 0.5 * tf.math.log(NoiseVar)
            - 0.5 * (tf.math.square(Y - Fmu) + Fvar) / NoiseVar
        )

    # The following two methods are abstract in the base class.
    # They need to be implemented even if not used.

    def _predict_log_density(self, Fmu, Fvar, Y):
        raise NotImplementedError

    def _predict_mean_and_var(self, Fmu, Fvar):
        raise NotImplementedError


class MyStudentT(ScalarLikelihood):
    def __init__(self, scale=1.0, df=3.0, **kwargs):
        """
        :param scale float: scale parameter
        :param df float: degrees of freedom
        """
        super().__init__(**kwargs)
        self.df = Parameter(df, transform=positive())
        self.scale = Parameter(scale)

    def _scalar_log_prob(self, F, Y):
        return logdensities.student_t(Y, F, self.scale, self.df)

    def _conditional_mean(self, F):
        return F

    def _conditional_variance(self, F):
        var = (self.scale**2) * (self.df / (self.df - 2.0))
        return tf.fill(tf.shape(F), tf.squeeze(var))


class LogisticLikelihood(ScalarLikelihood):
    def __init__(self, scale=1.0, **kwargs):
        """
        :param scale float: scale parameter
        """
        super().__init__(**kwargs)
        self.scale = Parameter(scale, transform=positive())

    def _scalar_log_prob(self, F, Y):
        z = (Y - F) / self.scale
        norm = -tf.math.log(self.scale)
        return z - 2 * tf.math.log(1 + tf.math.exp(z)) + norm

    def _conditional_mean(self, F):
        return F

    def _conditional_variance(self, F):
        var = (self.scale**2) * (tf.math.pi**2 / 3.0)
        return tf.fill(tf.shape(F), tf.squeeze(var))


class LaplaceLikelihood(ScalarLikelihood):
    def __init__(self, scale=1.0, **kwargs):
        """
        :param scale float: scale parameter
        """
        super().__init__(**kwargs)
        self.scale = Parameter(scale, transform=positive())

    def _scalar_log_prob(self, F, Y):
        ll = logdensities.laplace(Y, F, self.scale)
        return ll

    def _conditional_mean(self, F):
        return F

    def _conditional_variance(self, F):
        var = 2 * self.scale**2
        return tf.fill(tf.shape(F), tf.squeeze(var))


if __name__ == "__main__":
    main()
