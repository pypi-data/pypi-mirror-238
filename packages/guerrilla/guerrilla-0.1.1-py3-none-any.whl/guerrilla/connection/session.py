from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


@dataclass
class BaseSession(ABC):
    """
    Base class for all session types.

    Attributes:
    -----------
    protocol : str
        The protocol used to connect to the device.
    """

    protocol: str
    name: str

    @property
    def status(self):
        """
        Returns the status of the session.

        Returns:
        --------
        str
            'connected' if the session is alive, 'disconnected' otherwise.
        """
        return "connected" if self._is_alive() else "disconnected"

    @abstractmethod
    def _is_alive(self) -> bool:
        """
        Abstract method to check if the session is alive.

        Returns:
        --------
        bool
            True if the session is alive, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def connect(self):
        """
        Abstract method to connect to the device.
        """
        raise NotImplementedError

    @abstractmethod
    def disconnect(self):
        """
        Abstract method to disconnect from the device.
        """
        raise NotImplementedError

    @abstractmethod
    def run(self):
        """
        Abstract method to run a command on the device.

        Returns:
        --------
        str
            The output of the command.
        """
        raise NotImplementedError

    @abstractmethod
    def find_prompt(self):
        """
        Abstract method to find the prompt of the device.

        Returns:
        --------
        str
            The prompt of the device.
        """
        raise NotImplementedError


class PROTOCOL(Enum):
    SSH = "ssh"
    TELNET = "telnet"
    SERIAL = "serial"

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)


@dataclass
class Session:
    """
    Session class for managing sessions.
    """

    name: str
    config: dict

    def __new__(cls, config: dict, name: str):
        """
        Create a new session based on the protocol.
        """
        protocol = config.get("protocol", None)
        match protocol:
            case PROTOCOL.SSH:
                from guerrilla.connection.ssh import SSHSession

                return SSHSession(**config, name=name)
            case _:
                raise ValueError(f"Invalid protocol: {protocol}")
