import math
import os
import time
from typing import Any, Iterable, List, Sized

BarConfig = {"disable loading bar": False}


def compute_lagrange_esimate(n: int, y: List[float], m: int) -> float:
    """
    given three data points we compute the lagrangian interpolation
    using points n-2, n-1 and n, with values y=y1,y2,y3 and evaluate at m

    Args:
        n: indicates the x-axis of the data
        y: indicates the y-axis values
        m: where shall we interpolate
    """
    x = range(n - len(y) + 1, n + 1)
    p = []
    for i in range(len(y)):
        p.append(
            y[i]
            * math.prod([(m - x[j]) / (x[i] - x[j]) for j in range(len(y)) if i != j])
        )
    return sum(p)


class ProgressBar:
    def __init__(
        self,
        iterable: Iterable,
        total_steps: int = -1,
        base_str: str = "loop",
        interpolation: int = 1,
    ) -> None:
        self.interpolation = interpolation
        self.iterable = iter(iterable)
        if isinstance(iterable, Sized):
            self.total_steps = len(iterable) if total_steps < 0 else total_steps
        else:
            self.total_steps = 0
        self.base_str = base_str
        self.progress_bar_size = self.get_size() - (36 - (21 - len(self.base_str)))
        self.current_progression = 0
        self.suffix_length = 11
        self.start_time = time.time()
        self.previous_time_steps: List[float] = []

    def __len__(self) -> int:
        return self.total_steps

    def get_size(self):
        try:
            width = os.get_terminal_size().columns
        except:
            width = 80
        return width

    def linear_interpolation(self) -> float:
        one_step_duration = (time.time() - self.start_time) / (
            max(self.current_progression, 1)
        )
        remaining_steps = self.total_steps - (self.current_progression)
        remaining_time = one_step_duration * remaining_steps
        return remaining_time

    def quadratic_interpolation(self) -> float:
        current_time_step = time.time() - self.start_time
        self.previous_time_steps.append(current_time_step)
        if len(self.previous_time_steps) == self.interpolation + 1:
            self.previous_time_steps.pop(0)
        if len(self.previous_time_steps) >= 3:
            remaining_time = (
                compute_lagrange_esimate(
                    n=self.current_progression,
                    y=self.previous_time_steps,
                    m=self.total_steps,
                )
                - current_time_step
            )
        else:
            one_step_duration = current_time_step / (max(self.current_progression, 1))
            remaining_time = one_step_duration * (
                self.total_steps - (self.current_progression)
            )
        return remaining_time

    def get_remaining_time(self) -> str:
        if self.interpolation <= 2:
            remaining_time = self.linear_interpolation()
        elif self.interpolation > 2:
            remaining_time = self.quadratic_interpolation()
        else:
            raise ValueError(
                f"requested interpolation is not supported ({self.interpolation})."
                "\nPlease use a postive integer"
            )
        return time.strftime("%H:%M:%S", time.gmtime(remaining_time))

    def runtime(self) -> str:
        duration = time.time() - self.start_time
        return time.strftime("%H:%M:%S", time.gmtime(duration))

    def update_bar_size(self) -> None:
        if (
            self.get_size() - (3 + len(self.base_str) + self.suffix_length)
            != self.progress_bar_size
        ):
            self.progress_bar_size = self.get_size() - (
                3 + len(self.base_str) + self.suffix_length
            )

    def build_prefix(self) -> str:
        base_string = f"\r[{self.base_str}]"
        return base_string

    def build_bar(self, progression_complete: bool) -> str:
        if progression_complete:
            bar = f"|" + "█" * self.progress_bar_size + "|"
        else:
            percentage = int(
                self.progress_bar_size * self.current_progression / self.total_steps
            )
            bar = (
                f"|"
                + "█" * percentage
                + " " * (self.progress_bar_size - percentage)
                + "|"
            )
        return bar

    def build_suffix(self, progression_complete: bool) -> str:
        if progression_complete:
            return self.runtime()
        else:
            return self.get_remaining_time()

    def __iter__(self):
        return self

    def __next__(self, *args: Any, **kwds: Any) -> Any:
        progression_complete = self.current_progression >= self.total_steps
        base_string = self.build_prefix()
        suffix = self.build_suffix(progression_complete=progression_complete)
        self.update_bar_size()
        bar = self.build_bar(progression_complete=progression_complete)
        if not BarConfig["disable loading bar"]:
            print(
                f"\r{base_string} {bar} {suffix}",
                end="" if not progression_complete else "\n",
            )
        if progression_complete:
            raise StopIteration
        output = next(self.iterable)
        self.current_progression += 1
        return output


if __name__ == "__main__":
    a = list(range(15))
    for i in ProgressBar(a):
        pass
    print("last value", i)
    print("---")
    for i in ProgressBar(a, total_steps=10):
        pass
    print("last value", i)
    BarConfig["disable loading bar"] = True
    print("---")
    for i in ProgressBar(a, total_steps=10):
        pass
    print("last value", i)
    BarConfig["disable loading bar"] = False
    print("---")
    for i in ProgressBar(a, total_steps=10):
        pass
    print("last value", i)

# python -m src.loadingpy.basic_bar
