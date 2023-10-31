from typing import Protocol


class SessionProtocol(Protocol):
    protocol: str
    name: str
    type: str

    @property
    def status(self) -> str:
        ...

    def _is_alive(self) -> bool:
        ...

    def connect(self) -> None:
        ...

    def disconnect(self) -> None:
        ...

    def run(self, command: str) -> str:
        ...

    def find_prompt(self) -> str:
        ...
