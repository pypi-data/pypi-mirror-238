#!/usr/bin/env python3
"""This module defines the abstract gaussian process regression class
for Gaussian Process Regression testing.

"""

from abc import ABC, abstractmethod
import numpy as np
import gp_function as gpf


class GprClass(ABC):
    def __init__(
        self, type, xs, data, data_l, noise, kernel, mean=None, constraints=None
    ):
        self._type = type
        self._xs = np.array(xs)
        self._nxs = len(self._xs)
        self._solved = False
        self._log_evidence = None
        self._obj_hp_map = {}

        if isinstance(data, list):
            self._data = np.array(data)
        elif isinstance(data, np.ndarray):
            self._data = data
        else:
            print("Data in GprClass init is of unknown type")
            raise ValueError
        self._ndata = len(self._data)

        if isinstance(data_l, list):
            self._data_l = np.array(data_l)
        elif isinstance(data, np.ndarray):
            self._data_l = data_l
        else:
            print("Data_l in GprClass init is of unknown type")
            raise ValueError

        if self._ndata != len(self._data_l):
            print("Length of data does not match length of data_l")
            raise ValueError

        if np.size(noise) == 1:
            self._sigma_n = noise * np.identity(self._ndata)
        elif len(noise.shape) == 1:
            if len(noise) == self._ndata:
                self._sigma_n = noise * np.identity(self._ndata)
            else:
                print("Length of data and measured noise are incompatiable")
                raise ValueError
        elif noise.shape == (self._ndata, self._ndata):
            self._sigma_n = noise
        else:
            print("Length of data and measured noise are incompatiable")
            raise ValueError

        self._kernel = kernel
        if mean is None:
            self.mean = gpf.Zero()
        else:
            self._mean = mean

        hp = list(self._kernel.get_hp()) + list(self._mean.get_hp())
        hp_names = self._kernel.get_hp_names() + self._mean.get_hp_names()

        self._hp_dict = dict(zip(hp_names, hp))

        if constraints is not None:
            pass

    def print_data(self):
        print(f"Gaussian process regression is of type {self._type}.")
        for key, value in self._hp_dict.items():
            print(f"The {key} has a value of {value}")

    @abstractmethod
    def eval(self):
        pass

    def __call__(self):
        return self.eval()

    def set_hp(self, key, value):
        if key in self._hp_dict:
            self._hp_dict[key] = value
        else:
            print(f"{key} is not a reconized hp name")
            raise (KeyError)
        if key in self._mean.get_hp_names():
            self._mean.set_hp(key, value)
        if key in self._kernel.get_hp_names():
            self._kernel.set_hp(key, value)
        self._solved = False

    def get_hp(self, key=None):
        if key is None:
            return self._hp_dict.items()
        elif key in self._hp_dict:
            return self._hp_dict[key]
        else:
            print(f"{key} is not a reconized hp name")
            raise (KeyError)

    def get_hp_names(self):
        return self._hp_dict.keys()

    def get_kss(self):
        self._kss = np.array([[self._kernel(i, j) for i in self._xs] for j in self._xs])

    def get_kls(self):
        self._kls = np.array(
            [[self._kernel(i, j) for i in self._data_l] for j in self._xs]
        ).T

    def get_kll(self):
        self._kll = np.array(
            [[self._kernel(i, j) for i in self._data_l] for j in self._data_l]
        )

    def get_mean_l(self):
        self._mean_l = np.array([self._mean(i) for i in self._data_l])

    def get_mean_s(self):
        self._mean_s = np.array([self._mean(i) for i in self._xs])

    def set_objective_map(self, hp_list=None):
        self._obj_hp_map = {}
        initial_hp = []
        if hp_list is None:
            for idx, key in enumerate(self._hp_dict.keys()):
                self._obj_hp_map[key] = idx
                initial_hp.append(self._hp_dict[key])
        else:
            idx = 0
            for key in hp_lish:
                if key in self._hp_dict:
                    self._obj_hp_map[key] = idx
                    initial_hp.append(self._hp_dict[key])
                    idx += 1
                else:
                    print(f"Key {key} is not a reconized hyperparameter")
                    raise KeyError
        return np.array(initial_hp)

    def objective(self, hyper_parameters):
        if self._obj_hp_map == {}:
            self.set_objective()
        for key, value in self._obj_hp_map.items():
            self.set_hp(key, hyper_parameters[value])
        self.eval()
        return -1.0 * self._log_evidence


class GaussianLikelihood(GprClass):
    def __init__(self, xs, data, data_l, noise, kernel, mean=None, constraints=None):
        GPR_TYPE = "Gaussian Likelihood"
        self._EPS = 1.0e-6
        super().__init__(GPR_TYPE, xs, data, data_l, noise, kernel, mean, constraints)

    def solve(self):
        self.get_kss()
        self.get_kls()
        self.get_kll()
        self.get_mean_l()
        self.get_mean_s()

        mat_invs = np.linalg.inv(self._sigma_n + self._kll)
        self._post_mean = self._mean_s + np.dot(
            np.dot(self._kls.T, mat_invs), (self._data - self._mean_l)
        )
        self._post_cov = self._kss - np.dot(np.dot(self._kls.T, mat_invs), self._kls)
        self._post_cov_fac = np.linalg.cholesky(
            self._post_cov + self._EPS * np.identity(self._nxs)
        )
        self._log_evidence = -0.5 * (
            self._ndata * np.log(2 * np.pi)
            + np.log(np.linalg.det(self._sigma_n + self._kll))
            + np.dot(
                np.dot(self._data - self._mean_l, mat_invs), self._data - self._mean_l
            )
        )

        self._solved = True

    def eval(self):
        """Returns the posterior mean"""
        if not self._solved:
            self.solve()
        return self._post_mean

    def sample(self, rng=None):
        pass

    def n_sigma(self, n=2):
        pass
