from typing import Callable, Any


def toName(stage: str):
    return stage.replace("Stages/", "").replace(".bin", "")


def clamp(n, a, b):
    return min(max(n, a), b)


def tryit(target: Callable, args: Any = None, exc: Any = None):
    try:
        if args is None:
            return target()
        return target(args)
    except:
        return exc
