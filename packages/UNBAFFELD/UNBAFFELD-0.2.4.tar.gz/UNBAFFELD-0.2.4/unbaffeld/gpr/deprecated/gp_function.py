#!/usr/bin/env python3
"""This module defines the abstract function class
for Gaussian Process Regression testing. The function can be used
both to define a prior mean, as well as define the length scale for a
non-stationary kernel, like the Gibbs kernel.

In general a function should be able to evaluate itself,
as well as evaluate it's derative and potentially it's integral.

A funcion stores it's hyperparameters as well as gives them names.

A function has methods to get and set the hyperparameters.
"""

from abc import ABC, abstractmethod
import numpy as np


class GpFunctionClass(ABC):
    def __init__(self, hyper_parameters, hyper_names, function_type):
        self._hp = np.array(hyper_parameters)
        self._hp_names = hyper_names
        self._type = function_type

    def print_data(self):
        print(f"Function is a {self._type} function.")
        for name, value in zip(self._hp_names, self._hp):
            print(f"The {name} has a value of {value}")

    @abstractmethod
    def eval(self, x, dx=0):
        pass

    def __call__(self, x, dx=0):
        return self.eval(x, dx)

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


class Zero(GpFunctionClass):
    def __init__(self):
        FUNCTION_TYPE = "Zero"
        HP_NAMES = []
        super().__init__([], HP_NAMES, FUNCTION_TYPE)

    def eval(self, x, dx=0):
        return 0.0


class Constant(GpFunctionClass):
    def __init__(self, hyper_parameters=[1.0]):
        FUNCTION_TYPE = "Constant"
        HP_NAMES = [
            "Constant Value",
        ]
        super().__init__(hyper_parameters, HP_NAMES, FUNCTION_TYPE)

    def eval(self, x, dx=0):
        if dx == 0:
            return self._hp[0]
        elif dx == 1:
            return 0.0
        elif dx == -1:
            return self._hp[0] * x
        elif isinstance(dx, int) and dx > 1:
            return 0.0
        else:
            print(f"In function {self._type}.eval methd")
            print(f"No method for dx = {dx}")
            raise ValueError


class Line(GpFunctionClass):
    def __init__(self, hyper_parameters=[-1.0, 1.0]):
        FUNCTION_TYPE = "Line"
        HP_NAMES = ["Line Slope", "Line Intercept"]
        super().__init__(hyper_parameters, HP_NAMES, FUNCTION_TYPE)

    def eval(self, x, dx=0):
        if dx == 0:
            return self._hp[0] * x + self._hp[1]
        elif dx == 1:
            return self._hp[0]
        elif isinstance(dx, int) and dx > 1:
            return 0.0
        else:
            print(f"In function {self._type}.eval methd")
            print(f"No method for dx = {dx}")
            raise ValueError
