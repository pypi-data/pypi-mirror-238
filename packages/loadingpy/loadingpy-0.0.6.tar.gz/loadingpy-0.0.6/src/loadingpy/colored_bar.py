from typing import Iterable

from .basic_bar import ProgressBar

color_map = {
    "cyan": "\033[96m",
    "blue": "\033[94m",
    "purple": "\033[95m",
    "green": "\033[92m",
    "orange": "\033[93m",
    "red": "\033[91m",
    "white": "\033[0m",
}


class ColoredBar(ProgressBar):
    def __init__(
        self,
        iterable: Iterable,
        total_steps: int = -1,
        base_str: str = "loop",
        interpolation: int = 1,
        color: str = "green",
    ) -> None:
        super().__init__(iterable, total_steps, base_str, interpolation)
        self.color = color

    def build_prefix(self) -> str:
        base_string = f"\r[{color_map[self.color]}{self.base_str}\033[0m]"
        return base_string

    def build_bar(self, progression_complete: bool) -> str:
        if progression_complete:
            bar = (
                f"|{color_map[self.color]}" + "█" * self.progress_bar_size + "\033[0m|"
            )
        else:
            percentage = int(
                self.progress_bar_size * self.current_progression / self.total_steps
            )
            bar = (
                f"|{color_map[self.color]}"
                + "█" * percentage
                + " " * (self.progress_bar_size - percentage)
                + "\033[0m|"
            )
        return bar


if __name__ == "__main__":
    a = list(range(15))
    for i in ColoredBar(a):
        pass
    print("last value", i)
    print("---")
    for i in ColoredBar(a, total_steps=10):
        pass
    print("last value", i)

# python -m src.loadingpy.colored_bar
