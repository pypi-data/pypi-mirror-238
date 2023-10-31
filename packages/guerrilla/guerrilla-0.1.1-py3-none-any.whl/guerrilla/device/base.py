from dataclasses import dataclass, field
from guerrilla.connection import Session
from guerrilla.tpying import SessionProtocol


@dataclass
class BaseDevice:
    name: str
    type: str
    connections: dict
    session: SessionProtocol = field(init=False)

    def __post_init__(self):
        self.session = Session(config=self.connections, name=self.name)

    def connect(self) -> None:
        self.session.connect()

    def disconnect(self) -> None:
        self.session.disconnect()

    def run(self, command: str, expect_return: str = None) -> str:
        return self.session.run(command, expect_return=expect_return)

    def find_prompt(self) -> str:
        return self.session.find_prompt()

    @property
    def status(self) -> str:
        return self.session.status


@dataclass
class Device:
    config: dict

    def __new__(cls, config: dict):
        device_type = config.get("type", None)
        match device_type:
            case "router":
                from .router import Router

                return Router(**config)
            case "linux":
                from .linux import Linux

                return Linux(**config)
            case _:
                raise NotImplementedError(f"Device type {device_type} not implemented")
