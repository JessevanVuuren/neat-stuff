from types import TracebackType
import time


class Profiler:
    _measurements: dict[str, float] = {}

    def __init__(self) -> None:
        self._current_key: str
        self._current_time: float

    def __getitem__(self, key: str):
        if (key in Profiler._measurements):
            raise LookupError(f"measurement key: {key} already in use")
        
        self._current_key = key
        return self

    def __enter__(self):
        self._current_time = time.perf_counter()
        return self

    def get(self, key: str, remove:bool=True):
        if (key not in Profiler._measurements):
            raise LookupError(f"measurement for key: {key} not found")

        value = Profiler._measurements[key]
        if (remove):
            del Profiler._measurements[key]
        return value

    def __exit__(self, type_: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> bool | None:
        diff = time.perf_counter() - self._current_time
        Profiler._measurements[self._current_key] = diff
        self._current_time = 0.0
        self._current_key = ""
