from enum import Enum


class MODE(Enum):
    MAIN = "main"
    CONFIG = "config"
    CONFIG_IF = "config-if"

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)
