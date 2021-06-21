

from inspect import signature
from typing import Callable, Any, Optional, Union, Optional
from functools import wraps
from operator import add


def curry(func_or_n: Union[int, Callable]):
    """ Curry a function (potentially only a certain number of times)
    Args:
        if `func_or_n` is `Callable`, curry it completely
    """
    def curry_n(func_to_curry: Callable, n: Optional[int]) -> Callable:
        """
        Args:
            `n`: If `n` is `None` curry completely
        """
        # get all arguments names
        sig = signature(func_to_curry).parameters
        args = list(sig.keys())
        # args_with_default = [(arg, val.kind.value) for ( # TODO: handle optionals
        #     arg, val) in sig.items() if val.default != val.empty]
        if len(args) <= 1:
            return func_to_curry
        else:
            extra_args = ", ".join(args[1:])
            all_args = ", ".join(args)
            loc = locals().copy()
            # we define a new function that takes only the first parameter
            # those returns a function of only x1 and x2
            if n is None:
                recursive_curry_decorator = "@curry"
            else:
                # we're currently in the process of currying so the returned function
                # will already be curried - thus we check for `n <= 1` rather than 0.
                recursive_curry_decorator = "#" if n <= 1 else f"@curry({n - 1})"
            exec(f"""
# we create a new function that just serves as a scope to capture the func_to_curry
def scope(func_to_curry=func_to_curry):
    # the curried function will only take a single argument
    @wraps(func_to_curry)
    def curried_func({args[0]}):
        # define a curried replacement function that takes all the remaining arguments
        {recursive_curry_decorator}
        def internal_func({extra_args}):
            return func_to_curry({all_args})
        return internal_func
    return curried_func
curried_func = scope()
""", globals(), loc)
            return loc["curried_func"]
    if type(func_or_n) is int:
        return lambda f: curry_n(f, func_or_n)
    else:
        return curry_n(func_or_n, None)


def f(a, b, c, d):
    return (a + b * c) % d


f1 = curry(f)
f2 = curry(1)(f)
f3 = curry(2)(f)
print(f1(1)(2)(3)(4), (1+2*3) % 4)
print(f2(1)(2, 3, 4), (1+2*3) % 4)
print(f3(1)(2)(3, 4), (1+2*3) % 4)

# doesn't influence the function


@curry
def g(x): return x + 5


print(g(2), 2+5)

""" *args and **kwargs aren't handled correctly yet
@curry(1)
def h(x, *args): return x + sum(*args)
h(1)(2,3,4) # doesn't work
"""

""" The `curry`-decorator allows us to write a version of partial that is quite a bit simpler than the
one in functools.
"""


def partial(f, *args):
    curried_f = curry(len(args))(f)
    for arg in args:
        curried_f = curried_f(arg)
    return curried_f


print(partial(add, 2)(5), 2+5)
print(partial(f, 1, 2)(3, 4), f(1, 2, 3, 4))

"""
We could also define a `curry` decorator where we don't specify the number of times to curry
and simply take `*args` and dynamically decide whether we have enough arguments to call the
base function already. This would simplify the implementation quite a bit but probably have
an impact on runtimes and may increase the chance for user-side bugs where the function is
called with an incorrect number of parameters.
"""
