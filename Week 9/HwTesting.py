import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('./')
from solvers import *

np.random.seed(123)
m = 20
n = 10
l = np.zeros(n)
u = np.ones(n)
#
A  = np.random.randn(m, n)
xt = -np.random.rand(n)
b  = A.dot(xt)

#==GRADED==#
# TODO: create C and d used for the solver
C = np.concatenate((np.eye(n), -np.eye(n)), axis=0)
d = np.concatenate((u, -l), axis=0)

#==GRADED==#
x0_ip = 0.5*(l + u)
x_ip, obj_his_ip, err_his_ip, exit_flag_ip = optimizeWithIP(x0_ip, A, b, C, d)

fig, ax = plt.subplots(1, 2, figsize=(12,5))
ax[0].plot(obj_his_ip)
ax[0].set_title('function value')
ax[1].semilogy(err_his_ip)
ax[1].set_title('optimality condition')
fig.suptitle('Interior Point on Quadratic over Box')