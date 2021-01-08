from typing import Tuple, Union, Any, Iterable, Callable
import abc
from functools import reduce
from itertools import chain, takewhile, dropwhile
import operator

ParseResult = Iterable[Tuple[Any, str]]


class Parser(abc.ABC):
    @abc.abstractmethod
    def __call__(self, raw: str) -> ParseResult:
        pass

    def parse(self, raw: str):
        return next(self(raw))

    def parse_strict(self, raw: str):
        (res, rem) = next(self(raw))
        return (list(res), rem)


class AlternateParser(Parser):
    def __init__(self, *parsers: Iterable[Parser]):
        self.parsers = parsers

    def __call__(self, raw: str) -> ParseResult:
        for p in self.parsers:
            yield from p(raw)

    def __or__(self: Parser, other: Parser) -> Parser:
        return AlternateParser(self, other)


Parser.__or__ = AlternateParser.__or__


class SequenceParser(Parser):
    def __init__(self, *parsers: Iterable[Parser]):
        self.parsers = parsers

    def __call__(self: Parser, raw: str) -> ParseResult:
        def f(accumulator: ParseResult, parser: Parser) -> ParseResult:
            for (val, remainder) in accumulator:
                for val_prime, remainder_prime in parser(remainder):
                    yield (chain(val, val_prime), remainder_prime)
        yield from reduce(f, self.parsers, [([], raw)])

    def __rshift__(self: Parser, other: Parser) -> Parser:
        return SequenceParser(self, other)


Parser.__rshift__ = SequenceParser.__rshift__
AlternateParser.__rshift__ = SequenceParser.__rshift__


class Digit(Parser):
    def __call__(self, raw: str) -> ParseResult:
        try:
            yield ((int(raw[0]), ), raw[1:])
        except IndexError:
            pass


class Predicate(Parser):
    def __init__(self, predicate: Callable[[str], bool], transform: Callable[[str], Iterable[Any]] = lambda x: (x, )):
        self.predicate = predicate
        self.transform = transform

    def __call__(self, raw: str) -> ParseResult:
        head = "".join(takewhile(self.predicate, raw))
        tail = "".join(dropwhile(self.predicate, raw))
        if len(head) > 0:
            yield (self.transform(head), tail)


class Natural(Parser):
    def __call__(self, raw: str) -> ParseResult:
        yield from Predicate(str.isdigit, lambda x: (int(x),))(raw)


class Whitespace(Parser):
    def __call__(self, raw):
        yield from Predicate(str.isspace, lambda _: [])(raw)


class Text(Parser):
    def __call__(self, raw):
        yield from Predicate(str.isalpha)(raw)


class Optional(Parser):
    def __init__(self, parser: Parser):
        self.parser = parser

    def __call__(self, raw: str) -> ParseResult:
        try:
            p = self.parser(raw)
            x = next(p)
            yield x
            yield from p
        except StopIteration:
            yield ([], raw)


class Keyword(Parser):
    def __init__(self, keyword):
        self.keyword = keyword

    def __call__(self, raw: str):
        if raw.startswith(self.keyword):
            yield ([self.keyword], raw[len(self.keyword):])


class Floating(Parser):
    p = Natural() >> Keyword(".") >> Natural()

    def __call__(self, raw):
        for ([integer, _, fractional], remainder) in self.p(raw):
            yield((float(f"{integer}.{fractional}"),), remainder)


if __name__ == "__main__":
    """
    p = Natural() >> Whitespace() >> (Natural() | Text()) >> Optional(Digit())
    print(p.parse_strict("123 456"))
    print(p.parse_strict("123 test456"))

    calc = (Floating() | Natural()) >> Optional(Whitespace()) >> (Keyword("+") | Keyword("-") |
                                                                  Keyword("*") | Keyword("/")) >> Optional(Whitespace()) >> (Floating() | Natural())
    while (s := input()):
        ([a, op, b, *rem], _) = calc.parse_strict(s)
        op = {"+": operator.add, "-": operator.sub,
              "*": operator.mul, "/": operator.truediv}[op]
        print(op(a, b))
        if rem:
            print("Couldn't match: ", rem)
    """

    Number = Floating() | Natural()
    Operator = Keyword("+") | Keyword("-") | Keyword("*") | Keyword("/")
    p1 = Number >> Optional(Whitespace())
    p2 = Operator >> Optional(Whitespace()) >> Number >> Optional(Whitespace())
    p2.parsers = (*p2.parsers, Optional(p2))
    p3 = p1 >> p2

    op = {"+": operator.add, "-": operator.sub,
          "*": operator.mul, "/": operator.truediv}

    def f(accu, new):
        if isinstance(new, str):
            return lambda x: op[new](x, accu)
        else:
            return accu(new)
    while (s := input()):
        (lst, _) = p3.parse_strict(s)
        result = reduce(f, lst, lambda x: x)
        print(result)
