import sys

from loguru import logger

logger.remove()
logger.add(sys.stdout, level="DEBUG")


class COLOR:
    _COLORS = {
        "RED": "\033[91m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "BLUE": "\033[94m",
        "MAGENTA": "\033[95m",
        "CYAN": "\033[96m",
        "WHITE": "\033[97m",
    }

    _STYLES = {"BOLD": "\033[1m", "UNDERLINE": "\033[4m", "ITALIC": "\033[3m"}

    _RESET = "\033[0m"

    @staticmethod
    def apply_color(text, color):
        return f"{color}{text}{COLOR._RESET}"

    @staticmethod
    def apply_style(text, style):
        return f"{style}{text}{COLOR._RESET}"

    @classmethod
    def red(cls, text):
        return cls.apply_color(text, cls._COLORS["RED"])

    @classmethod
    def green(cls, text):
        return cls.apply_color(text, cls._COLORS["GREEN"])

    @classmethod
    def yellow(cls, text):
        return cls.apply_color(text, cls._COLORS["YELLOW"])

    @classmethod
    def blue(cls, text):
        return cls.apply_color(text, cls._COLORS["BLUE"])

    @classmethod
    def magenta(cls, text):
        return cls.apply_color(text, cls._COLORS["MAGENTA"])

    @classmethod
    def cyan(cls, text):
        return cls.apply_color(text, cls._COLORS["CYAN"])

    @classmethod
    def white(cls, text):
        return cls.apply_color(text, cls._COLORS["WHITE"])

    @classmethod
    def bold(cls, text):
        return cls.apply_style(text, cls._STYLES["BOLD"])

    @classmethod
    def underline(cls, text):
        return cls.apply_style(text, cls._STYLES["UNDERLINE"])

    @classmethod
    def italic(cls, text):
        return cls.apply_style(text, cls._STYLES["ITALIC"])
