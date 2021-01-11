"""Probability distribution functions"""

import numpy as np
import random as rn


def weibull(xdist, a, b):
    """
    Two parameter Weibull distribution.
    :return:
    """

    y = a/b*(xdist/b)**(a-1)*np.exp(-(xdist/b)**a)

    return y