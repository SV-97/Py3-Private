from itertools import islice
from fractions import Fraction


class RelativeDict():
    """
    Ordered collection that allows "normal" dict-like indexing as well as "relative" indexing.
    Example:
    ```
        a = RelativeDict((("a", 1), ("b", 2), ("c", 3)))
        a["b"] == 2
        a["b", 1] == a["c"]
        a["b", -1] == a["a"]
    ```
    """

    def __init__(self, items):
        self.vals = [value for _, value in items]
        self.indices = {key: idx for idx, (key, _) in enumerate(items)}

    def __getitem__(self, key):
        if type(key) == tuple and len(key) == 2:
            k = self.indices[key[0]] if type(key[0]) != int else key[0]
            return self.vals[k + key[1]]
        elif type(key) == int:
            return self.vals[key]
        else:
            return self.vals[self.indices[key]]

    def __setitem__(self, key, val):
        if type(key) == tuple and len(key) == 2:
            k = self.indices[key[0]] if type(key[0]) != int else key[0]
            self.vals[k + key[1]] = val
        elif type(key) == int:
            self.vals[key] = val
        else:
            self.vals[self.indices[key]] = val

    def items(self):
        return [(key, self.vals[self.indices[key]]) for key in self.indices.keys()]


def drop(it, n):
    return islice(it, n, None)


class TimeUnit():
    def __init__(self, name, up_factor=None, down_factor=None):
        self.name = name
        self.up_factor = Fraction(up_factor) if up_factor is not None else None
        self.down_factor = Fraction(
            down_factor) if down_factor is not None else None

    def __str__(self): return ", ".join(
        f"{key} : {val}" for key, val in vars(self).items())


def str_units(units):
    return " = ".join(f"{u.name} / {u.down_factor}" for u in units)


factors = (
    ("millenia", 10),
    ("centuries", 100),
    ("years", 365),
    ("days", 24),
    ("hours", 60),
    ("minutes", 60),
    ("seconds", 60),
    ("millis", 1000),
    ("micros", 1000),
    ("nanos", None))

sorted_unit_names = [name for name, _ in factors]

units = [TimeUnit(name, down_factor=fac) for name, fac in factors]
for i, unit in enumerate(drop(units, 1)):
    unit.up_factor = Fraction(1, units[i].down_factor)


class BigTimeDelta():
    """
    Class for big time-spans (similar to datetime.timedelta)

    Todo:
        * implement cascading for negative values (probably by reducing everything
            to a base unit (e.g. nanos) and then cascading upwards)
        * deduplicate cascading
        * add more methods like `in_nanos` - maybe generate them automatically
    """

    def __init__(self, *, millenia=0, centuries=0, years=0, days=0, hours=0, minutes=0, seconds=0, millis=0, micros=0, nanos=0):
        l = locals()
        to_do = RelativeDict([(name, l[name]) for name in sorted_unit_names])
        done = RelativeDict([(name, None) for name in sorted_unit_names])

        for unit in units[:-1]:  # cascade downwards
            name = unit.name
            done[name] = int(to_do[name])
            to_do[name, 1] += unit.down_factor * \
                (to_do[name] - done[name])
        done["nanos"] = Fraction(to_do["nanos"])

        for unit in reversed(units[1:]):  # cascade upwards
            name = unit.name
            next_down_factor = 1/unit.up_factor
            if done[name] >= next_down_factor:
                too_much = done[name]
                done[name, -1] += unit.up_factor * too_much
                done[name] = 0

        for name, val in done.items():
            setattr(self, name, val)

    def __format__(self, format_spec):
        if format_spec != "":
            return ", ".join(f"{float(val):{format_spec}} {name}" for name, val in vars(self).items() if val != 0)
        else:
            return ", ".join(f"{val:{format_spec}} {name}" for name, val in vars(self).items() if val != 0)

    def __str__(self):
        return ", ".join(f"{val} {name}" for name, val in vars(self).items() if val != 0)

    def __repr__(self):
        return ", ".join(f"{val} {name}" for name, val in vars(self).items())

    @property
    def in_nanos(self):
        val = RelativeDict([(name, getattr(self, name))
                            for name in sorted_unit_names])
        for unit in units[:-1]:  # cascade downwards
            name = unit.name
            val[name, 1] += unit.down_factor * val[name]
        return val["nanos"]


if __name__ == "__main__":
    t = BigTimeDelta(years=0.1, millis=0.1, nanos=5000)
    print(t)
