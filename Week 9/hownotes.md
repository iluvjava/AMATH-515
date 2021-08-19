### **Some Notes on how to deal with the Coding part of the coding HW**

In the HW we are considering the Lagrangian: 

$$
\mathcal{L}(x, v) =\frac{1}{2}\Vert Ax - b\Vert^2 - v^T(d - Cx) \quad v \ge 0, d - Cx \ge 0
$$

And then we are going to relax the constraint with a variable $\mu$, giving us: 

$$
\nabla \mathcal{L}(x, v) =
\begin{bmatrix}
    -A^T(b - Ax) + C^Tv
    \\
    \text{diag}(v)(d - Cx) - \mu\mathbb{J}
\end{bmatrix} = F_\mu(x, v)
$$

The first constraint is from the primal differential, and the second constraint is from the complementary slackness.

Now, consider the new update for the algorithm, which is going to be: 

$$
\begin{bmatrix}
    \Delta x \\ \Delta v
\end{bmatrix}
=
- \text{Jacobian}^{-1}(F_\mu, x, v)F_\mu(x, v)
$$

And the positivity constraints will be needed to choose a value of $\alpha$ such that: 

$$
\begin{cases}
    v + \alpha \Delta v > 0 \\
    d - C(x + \alpha \Delta x) > 0
\end{cases}
$$

Consider the positivity constraint for the dual variable, which is giving us: 

$$
\alpha \Delta v > -v \implies 
\alpha \begin{Bmatrix}
    > & \Delta v_i > 0
    \\
    < & \Delta v_i < 0
\end{Bmatrix}-v
\implies
\alpha < \frac{-v_i}{\Delta v_i} \quad \forall i: v_i < 0
$$

Similarly:

$$
\alpha < \left(
    \frac{d - Cx}{C\Delta x}
\right)_i \quad \forall i : (C\Delta x)_i > 0
$$

Where division is element-wise operation on the vector, so then, assuming that this works at all[^1]: 

$$
0 < \alpha < \min\left(
    \min\left\lbrace
        \frac{-v_i}{\Delta v_i}: \Delta v_i < 0
    \right\rbrace, 
    \min \left\lbrace
        \left(
            \frac{d - Cx}{C\Delta x}
        \right)_i : (C\Delta x)_i > 0
    \right\rbrace
\right)
$$

And reasonable in this range will be a good choice for keeping the positivity constraints. 

So we don't shoot over the boundary. We are going to assume that process updating the $\mu$ is a job left for creativity. 

The Jacobian is 

$$
\text{Jcobian}(F_\mu; x, v) =
\begin{bmatrix}
    A^TA & C^T
    \\
    \nabla_x[-v\circ (Cx)] & \nabla_v[v\circ (d - Cx)]
\end{bmatrix}
$$

Take note that: 

$$
\nabla_x[-v\circ Cx]= -\text{diag}(v) \nabla_x[Cx] = -\text{diag}(v)C
$$

So the Jacobian can be simplified into:

$$
\text{Jcobian}(F_\mu; x, v) =
\begin{bmatrix}
    A^TA & C^T
    \\
    -\text{diag(v)}C & \text{diag}(d - Cx)
\end{bmatrix}
$$

And the relaxation variable $\mu$ will be given by: 

$$
u^+ = \frac{1}{10} \frac{\langle z^+, s^+\rangle}{\text{len}(z^+)}
$$

---
### **Chambolle Pock**

in the code, there are several quantities compare to what we have in the lectures: 

$$
rx = b - Ax\quad rx^+ = b - Ax^+ \quad rz = c - A^Tz
$$

And the iteration in the code will be different which looks like: 

$$
x^+ = \underset{\gamma, g}{\text{prox}}(x - \gamma (rz))
\quad 
z^+ = \underset{\gamma, h^*}{\text{prox}}(z + \gamma (2rx^+ - rx))
$$

And the primal dual problem format we are addressing here is: 

> $$
> \min_x \left\lbrace
> g(x) + h(Ax - b) + c^Tx 
> \right\rbrace
> =
> \sup_z \left\lbrace
> -b^Tz - h^*(z) - g^*(-A^Tz - c)
> \right\rbrace \tag{1}
> $$

The choice of gamma has to make the pre-conditioner (which is already included into the iteration routine) positive definite, the $P$, pre-conditioner is given as: 

$$
P = \begin{bmatrix}
    \frac{1}{\gamma} I & -A^T \\
    -A & \frac{1}{\gamma}I
\end{bmatrix}
$$

Consider: 
$$
\begin{bmatrix}
    x_1 \\x_2
\end{bmatrix}^T
P
\begin{bmatrix}
    x_1\\ x_2
\end{bmatrix} = 
\begin{bmatrix}
    x_1 \\x_2
\end{bmatrix}^T
\begin{bmatrix}
    \frac{x_1}{\gamma} - A^Tx_2
    \\
    -Ax_1 + \frac{x_2}{\gamma}
\end{bmatrix}
$$

$$
    \frac{x_1^Tx_1}{\gamma} - x_1^TAx_2
    -
    x_2^TAx_1 + \frac{x_2^Tx_2}{\gamma}
    > 0
$$

$$
\frac{\Vert x\Vert^2}{\gamma} - x_1^TAx_2 - x_2^TAx_1 > 0
$$

$$
\frac{\Vert x\Vert^2}{\gamma} > x_1^TAx_2 + x_2^TAx_1
$$

$$
\frac{\gamma}{\Vert x\Vert^2} < (x_1^TAx_2 + x_2^TAx_1)^{-1}
$$

$$
\gamma < \left(
    x_1^TAx_2 + x_2^TAx_1
\right)^{-1}\Vert x\Vert^2
$$



[^1]: slack is always positive, dual variable is always positive, not sure about $\Delta x,\Delta v$ which could complicate things if not well handled. Take notice that $\alpha > 0$ non-the less or else we are not doing newton, we will be doing reverse newton which is bad.