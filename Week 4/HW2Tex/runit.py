import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt

import sys
sys.path.append('./')
from solvers import *

# create synthetic dataset
np.random.seed(123)
m = 10  # number of measurements
n = 10  # number of variables
k = 10   # number of nonzero variables
s = 0.05 # measurements noise level


A_cs = np.random.randn(m, n)
x_cs = np.zeros(n)
x_cs[np.random.choice(range(n), k, replace=False)] = np.random.choice([-1.0, 1.0], k)
x_cs = np.random.rand(m)
b_cs = A_cs.dot(x_cs) + s*np.random.randn(m)
#
lam_cs = 0.1*norm(A_cs.T.dot(b_cs), np.inf)

# define the function, prox and the beta constant
def func_f_cs(x):
    # TODO: complete the function
    Ax = A_cs@x
    b = b_cs
    return (0.5)*np.sum((Ax - b)**2)

def func_g_cs(x):
    # TODO: complete the function
    # return lam_cs*norm(x, 1)
    return 0

def grad_f_cs(x):
    # TODO: complete the gradient of the smooth part
    A = A_cs
    Ax = A@x
    b = b_cs
    return A.T@(Ax - b)

def prox_g_cs(x, t):
    # TODO: complete the prox of 1 norm
    def mapfunc(y):
        return y- np.sign(y) if abs(y) > lam_cs*t else 0
    vecFunc = np.vectorize(mapfunc)
    #return vecFunc(x)
    return x

##==GRADED==##
# TODO: what is the beta value for the smooth part
beta_f_cs = norm(A_cs.T@A_cs, 2)


# apply the proximal gradient descent solver
x0_cs_pgd = np.zeros(x_cs.size)

##==GRADED==##
# x_cs_pgd should be (mostly empty) numpy vector of shape (n, )
x_cs_pgd, obj_his_cs_pgd, err_his_cs_pgd, exit_flag_cs_pgd = \
    optimizeWithPGD(x0_cs_pgd, func_f_cs, func_g_cs, grad_f_cs, prox_g_cs, beta_f_cs)

print(obj_his_cs_pgd)
