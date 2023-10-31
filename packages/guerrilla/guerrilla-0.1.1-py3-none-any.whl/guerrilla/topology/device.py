from __future__ import annotations

import uuid
import weakref
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, Optional, Set, Union

from guerrilla.utils.type import DefaultBox as Box

if TYPE_CHECKING:
    from guerrilla.topology import Device, Interface, Link, Testbed


@dataclass
class Device:
    name: str
    type: str = None
    id: uuid.UUID = field(default_factory=lambda: str(uuid.uuid4()))
    alias: Optional[str] = None
    os: Optional[str] = None
    testbed: Testbed = None  # TODO: testbed type
    interfaces: Dict[str, Interface] = field(default_factory=Box)
    tacacs: Dict[str, Any] = field(default_factory=dict)
    passwords: Dict[str, Any] = field(default_factory=dict)
    credentials: Dict[str, Any] = field(default_factory=Box)
    connections: Dict[str, Any] = field(default_factory=Box)
    connection_manager: Optional[Any] = None  # TODO: connection_manager type
    clean: Dict[str, str] = field(default_factory=Box)
    custom: Dict[str, Any] = field(default_factory=Box)

    @property
    def links(self) -> Set[Link]:
        return {
            interface.link for interface in self.interfaces.values() if interface.link
        }

    @property
    def remote_devices(self) -> Set[Device]:
        devices = set()
        for link in self.links:
            devices.update(link.connected_devices)
        devices.discard(self)  # Ensure this device is not in the set
        return devices

    @property
    def remote_interfaces(self) -> Set[Interface]:
        interfaces = set()
        for link in self.links:
            interfaces.update(link.connected_interfaces)
        interfaces.difference_update(
            self.interfaces.values()
        )  # Remove this device's interfaces
        return interfaces

    def add_interface(self, interface: Interface):
        self.interfaces[interface.name] = interface
        interface.device = weakref.ref(self)

    def remove_interface(self, interface: Interface):
        self.interfaces.pop(interface.name, None)
        interface.device = None

    def find_links(self, destination: Union[Device, Interface]) -> Set[Link]:
        from .interface import Interface

        connected_links = set()

        if isinstance(destination, Device):
            for interface in self.interfaces.values():
                for remote_interface in interface.link.connected_interfaces:
                    if remote_interface.device() == destination:
                        connected_links.add(interface.link)

        elif isinstance(destination, Interface):
            for interface in self.interfaces.values():
                if interface.link == destination.link():
                    connected_links.add(interface.link)

        return connected_links

    def __hash__(self):
        return hash((self.id))

    def __eq__(self, other):
        if isinstance(other, Device):
            return self.id == other.id  # or combine other attributes if needed
        return NotImplemented

    def __iter__(self):
        yield from (intf_ref for intf_ref in self.interfaces if intf_ref)
