# heat_core.py
import numpy as np
from sympy import sympify, symbols, lambdify

metals = {
    'copper': 1.17e-4,
    'aluminum': 9.7e-5,
    'iron': 2.3e-5,
    'steel': 1.4e-5,
    'gold': 1.27e-4,
    'silver': 1.65e-4
}

def setup_matrices(nx, r):
    # Implicit matrix
    M_imp = np.zeros((nx, nx))
    for i in range(1, nx-1):
        M_imp[i, i-1] = -r / 2
        M_imp[i, i] = 1 + r
        M_imp[i, i+1] = -r / 2
    M_imp[0, 0] = 1 + r
    M_imp[0, 1] = -r
    M_imp[nx-1, nx-1] = 1 + r
    M_imp[nx-1, nx-2] = -r

    # Explicit matrix
    M_exp = np.zeros((nx, nx))
    for i in range(1, nx-1):
        M_exp[i, i-1] = r / 2
        M_exp[i, i] = 1 - r
        M_exp[i, i+1] = r / 2
    M_exp[0, 0] = 1 - r
    M_exp[0, 1] = r
    M_exp[nx-1, nx-1] = 1 - r
    M_exp[nx-1, nx-2] = r

    return M_imp, M_exp

def compute_next_u(u, M_imp, M_exp):
    return np.linalg.solve(M_imp, M_exp @ u)

def parse_initial_condition(init_expr, L):
    x_sym, L_sym = symbols('x L')
    expr = sympify(init_expr)
    expr = expr.subs(L_sym, L)
    f = lambdify(x_sym, expr, modules='numpy')
    return f