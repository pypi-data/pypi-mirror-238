from __future__ import annotations

import uuid
import weakref
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from guerrilla.topology import Device, Interface


@dataclass
class Link:
    name: str
    id: uuid.UUID = field(default_factory=lambda: str(uuid.uuid4()))
    alias: Optional[str] = field(default_factory=str)
    interfaces: list[weakref.ReferenceType[Interface]] = field(default_factory=list)

    # Initialize default values
    def __post_init__(self):
        if not self.alias:
            self.alias = self.name
        self.interfaces = [
            weakref.ref(interface)
            if not isinstance(interface, weakref.ReferenceType)
            else interface
            for interface in self.interfaces
        ]

    @property
    def connected_devices(self) -> set[Device]:
        devices = (
            interface.device
            for interface in self.connected_interfaces
            if interface.device
        )
        return set(devices)

    @property
    def connected_interfaces(self) -> set[Interface]:
        # Dereference the weakref to get the actual interfaces
        interfaces = (interface() for interface in self.interfaces if interface())
        return set(interfaces)

    def connect_interface(self, interface: Interface):
        # Store weak reference to the interface to avoid circular references
        self.interfaces.append(weakref.ref(interface))
        interface.link = weakref.ref(self)

    def disconnect_interface(self, interface: Interface):
        # Remove the weak reference of the interface
        self.interfaces = [i for i in self.interfaces if i() != interface]
        interface.link = None

    def __iter__(self):
        yield from (intf_ref() for intf_ref in self.interfaces if intf_ref())

    def __hash__(self):
        return hash((self.id))
