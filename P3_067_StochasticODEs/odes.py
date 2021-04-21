import numpy as np

from collections.abc import Iterable
from functools import wraps
from typing import NamedTuple, Callable, Dict, Any


class IvpSolution(NamedTuple):
    ts: np.array
    ys: np.array


class Ivp(NamedTuple):
    f: Callable[[float, np.array], np.array]
    t_0: float
    y_0: np.array
    problem_params: Dict[str, Any]


def ivp(t_0: float, y_0: np.array, **problem_params):
    return lambda f: Ivp(f, t_0, y_0, problem_params)


def solve_ivp(solver: Callable[[Ivp, Any], IvpSolution], **solver_params):
    def solve(ivp: Ivp):
        return wraps(ivp.f)(lambda: solver(ivp, **solver_params))
    return solve


def eulers_method(ivp: Ivp, t_end, step_size):
    t_0 = ivp.t_0
    steps = round(((t_end - t_0) / step_size))
    ts_ys = np.zeros((steps, ivp.y_0.size + 1))
    ts_ys[0, :] = np.array((ivp.t_0, *ivp.y_0))
    f = ivp.f
    p = ivp.problem_params
    for k in range(steps-1):
        y_k = ts_ys[k, 1:]
        t_k1 = t_0 + k * step_size
        y_k1 = y_k + step_size * f(t_k1, y_k, **p)
        ts_ys[k+1, :] = np.array((t_k1, *y_k1))
    return IvpSolution(ts_ys[:, 0], ts_ys[:, 1:])
