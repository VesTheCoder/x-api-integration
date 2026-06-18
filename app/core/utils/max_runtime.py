from time import perf_counter


def has_exceeded_max_runtime(started_at: float, max_runtime_sec: int | None) -> bool:
    """
    Check whether the configured runtime limit has been reached.
    """
    if max_runtime_sec is None:
        return False
    return perf_counter() - started_at >= max_runtime_sec
