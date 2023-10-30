#!/usr/bin/env python3
"""This module defines the abstract kernel class
for Gaussian Process Regression testing.

I general a kernel should be able to evaluate itself,
as well as evaluate it's derative and potential it's integral.

A kernel stores it's hyperparameters as well as gives them names.

A kernel has methods to get and set the hyperparameters.
"""

from abc import ABC, abstractmethod
import numpy as np


class KernelClass(ABC):
    def __init__(self, hyper_parameters, hyper_names, kernel_type):
        self._hp = np.array(hyper_parameters)
        self._hp_names = hyper_names
        self._type = kernel_type

    def print_data(self):
        print(f"Kernel is a {self._type} kernel")
        for name, value in zip(self._hp_names, self._hp):
            print(f"The {name} has a value of {value}")

    @abstractmethod
    def eval(self, x1, x2, dx1=0, dx2=0):
        pass

    def __call__(self, x1, x2, dx1=0, dx2=0):
        return self.eval(x1, x2, dx1, dx2)

    def set_hp(self, key, value):
        if isinstance(key, int):
            self._hp[key] = value
        elif key in self._hp_names:
            self._hp[self._hp_names.index(key)] = value
        else:
            print(f"{key} is not a reconized hp name")
            raise (KeyError)

    def get_hp(self, key=None):
        if key is None:
            return self._hp
        elif key in self._hp_names:
            return self._hp[self._hp_names.index(key)]
        else:
            print(f"{key} is not a reconized hp name")
            raise (KeyError)

    def get_hp_names(self):
        return self._hp_names


class SquareExp(KernelClass):
    def __init__(self, hyper_parameters=np.array([1.0, 1.0])):
        KERNEL_TYPE = "square exponential"
        HP_NAMES = [
            "square exponential variance",
            "square exponential variance correlation length",
        ]
        super().__init__(hyper_parameters, HP_NAMES, KERNEL_TYPE)

    def eval(self, x1, x2, dx1=0, dx2=0):
        if [dx1, dx2] == [0, 0]:
            return self.eval_kernel(x1, x2)
        elif [dx1, dx2] == [1, 0]:
            return self.eval_dx1(x1, x2)
        elif [dx1, dx2] == [0, 1]:
            return self.eval_dx2(x1, x2)
        elif [dx1, dx2] == [1, 1]:
            return self.eval_dx1dx2(x1, x2)
        else:
            print(f"In kernel {self._type}.eval methd")
            print(f"No method for dx1 = {dx1} and dx2 = {dx2}")
            raise ValueError

    def eval_kernel(self, x1, x2):
        return self._hp[0] ** 2 * np.exp(-((x1 - x2) ** 2) / (2 * self._hp[1] ** 2))

    def eval_dx1(self, x1, x2):
        kernel = self.eval_kernel(x1, x2)
        return kernel * (x1 - x2) / self._hp[1] ** 2

    def eval_dx2(self, x1, x2):
        return -1.0 * self.eval_dx1(x1, x2)

    def eval_dx1dx2(self, x1, x2):
        kernel = self.eval_kernel(x1, x2)
        return (1.0 - (x1 - x2) ** 2 / self._hp[1] ** 2) * kernel / self._hp[1] ** 2


class TwoSquareExp(KernelClass):
    def __init__(self, hyper_parameters=np.array([1.0, 1.0, 0.1, 0.1])):
        KERNEL_TYPE = "two square exponential"
        HP_NAMES = [
            "first square exponential variance",
            "first square exponential variance correlation length",
            "second square exponential variance",
            "second square exponential variance correlation length",
        ]
        super().__init__(hyper_parameters, HP_NAMES, KERNEL_TYPE)

    def eval(self, x1, x2, dx1=0, dx2=0):
        if [dx1, dx2] == [0, 0]:
            return self.eval_kernel(x1, x2)
        elif [dx1, dx2] == [1, 0]:
            return self.eval_dx1(x1, x2)
        elif [dx1, dx2] == [0, 1]:
            return self.eval_dx2(x1, x2)
        elif [dx1, dx2] == [1, 1]:
            return self.eval_dx1dx2(x1, x2)
        else:
            print(f"In kernel {self._type}.eval methd")
            print(f"No method for dx1 = {dx1} and dx2 = {dx2}")
            raise ValueError

    def eval_kernel(self, x1, x2):
        val = self._hp[0] ** 2 * np.exp(
            -((x1 - x2) ** 2) / (2 * self._hp[1] ** 2)
        ) + self._hp[2] ** 2 * np.exp(-((x1 - x2) ** 2) / (2 * self._hp[3] ** 2))
        return val

    def eval_dx1(self, x1, x2):
        ker1 = self._hp[0] ** 2 * np.exp(-((x1 - x2) ** 2) / (2 * self._hp[1] ** 2))
        ker2 = self._hp[2] ** 2 * np.exp(-((x1 - x2) ** 2) / (2 * self._hp[3] ** 2))
        val = ker1 * (x1 - x2) / self._hp[1] ** 2 + ker2 * (x1 - x2) / self._hp[3] ** 2
        return val

    def eval_dx2(self, x1, x2):
        return -1.0 * self.eval_dx1(x1, x2)

    def eval_dx1dx2(self, x1, x2):
        ker1 = self._hp[0] ** 2 * np.exp(-((x1 - x2) ** 2) / (2 * self._hp[1] ** 2))
        ker2 = self._hp[2] ** 2 * np.exp(-((x1 - x2) ** 2) / (2 * self._hp[3] ** 2))
        val = (1.0 - (x1 - x2) ** 2 / self._hp[1] ** 2) * ker1 / self._hp[1] ** 2 + (
            1.0 - (x1 - x2) ** 2 / self._hp[3] ** 2
        ) * ker2 / self._hp[3] ** 2
        return val
