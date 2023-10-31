from enum import Enum


# noqa: E731
class Commands(Enum):
    def FLUSH_IP(dev):
        return f"ip addr flush dev {dev}"
