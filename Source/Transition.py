from time import perf_counter
from Source.Eases import linear
from typing import Callable, Tuple


def transition(
    _from: Tuple[float, float] = (0, 0),
    to: Tuple[float, float] = (0, 0),
    delay: float = 0.0,
    duration: float = 1.0,
    ease: Callable = linear,
):
    start = perf_counter() + delay
    vec = tuple(t2 - t1 for t1, t2 in zip(_from, to))
    durFact = 1 / duration

    def aux():
        t = perf_counter()

        # Before animation (delay waiting)
        if t < aux.start:
            return _from
        # During animation

        dt = (t - aux.start) * durFact
        if dt < 1.0:
            mult = ease(dt)
            return tuple(mult * v + f for v, f in zip(vec, _from))
        # After animation
        return to
    
    def setStart(value):
        aux.start = value

    aux.setStart = setStart
    aux.start = start

    return aux
