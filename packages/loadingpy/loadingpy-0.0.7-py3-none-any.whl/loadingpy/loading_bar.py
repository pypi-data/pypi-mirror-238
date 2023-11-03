from typing import Any, Iterable, Optional

from .colored_bar import ColoredBar


class pybar(ColoredBar):
    def __init__(
        self,
        iterable: Iterable,
        monitoring: Optional[Any] = None,
        naming: Optional[Any] = None,
        total_steps: int = -1,
        base_str: str = "loop",
        interpolation: int = 1,
        color: str = "green",
    ) -> None:
        """
        creates a progress bar for a python iterable.

        Args:
            iterable: python object that can be iterated over
            monitoring [OPTIONAL]: a python object (or list of python objects) that will be printed after each iteration
                using the following format f'{monitoring}'. IF they are updated during the loop, make sure to
                update inplace, in order to see the changes
            naming [OPTIONAL]: if you want to add a descritpion prefix to the monitoring variables
            total_steps [OPTIONAL]: number of iterations to perform (if you set it to a lower value than the length of the iterable,
                then the process will stop after the given total_steps)
            base_str [OPTIONAL]: prefix description of the loop we are iterating over
            color [OPTIONAL]: which color to use for the loading bar
        """
        super().__init__(iterable, total_steps, base_str, interpolation, color)
        self.monitoring = monitoring
        self.naming = naming
        self.description: Optional[str] = None
        if isinstance(self.monitoring, (list, tuple)) and isinstance(
            self.naming, (list, tuple)
        ):
            assert len(self.naming) == len(self.monitoring)

        self.handle_monitoring()

    def set_description(self, description: Optional[str] = None) -> None:
        self.description = description

    def handle_naming(self) -> int:
        if self.naming is None:
            return 0
        if isinstance(self.naming, (list, tuple)):
            return sum([len(name) + 1 for name in self.naming])
        else:
            return len(self.naming) + 1

    def handle_monitoring(self) -> None:
        if self.description is not None:
            self.suffix_length = 11 + 3 + len(self.description)
        elif self.monitoring is not None:
            if isinstance(self.monitoring, (list, tuple)):
                self.suffix_length = (
                    11
                    + 2
                    + sum([len(f"{e}") + 1 for e in self.monitoring])
                    + self.handle_naming()
                )
            else:
                self.suffix_length = (
                    11 + 3 + len(f"{self.monitoring}") + self.handle_naming()
                )

    def build_monitoring_str(self) -> str:
        if not isinstance(self.monitoring, (list, tuple)):
            if self.naming is not None:
                return f"{self.naming}:{self.monitoring}"
            else:
                return f"{self.monitoring}"
        output = ""
        if self.naming is not None:
            for e, n in zip(self.monitoring, self.naming):
                output += f"{n}:{e}" + " "
        else:
            for e in self.monitoring:
                output += f"{e}" + " "
        output = output[:-1]
        return output

    def build_suffix(self, progression_complete: bool) -> str:
        suffix = super().build_suffix(progression_complete=progression_complete)
        if self.description is not None:
            suffix = f"{suffix} | {self.description}"
        elif self.monitoring is not None:
            suffix = f"{suffix} | {self.build_monitoring_str()}"
        self.handle_monitoring()
        return suffix
