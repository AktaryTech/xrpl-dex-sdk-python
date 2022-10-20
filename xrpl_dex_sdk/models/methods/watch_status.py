from typing import Callable, NamedTuple


class WatchStatusParams(NamedTuple):
    # Listener to send balance updates to
    listener: Callable


__all__ = ["WatchStatusParams"]
