from __future__ import annotations

import ipaddress
import uuid
import weakref
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Optional, Set, Union

if TYPE_CHECKING:
    from guerrilla.topology import Device, Interface, Link


@dataclass
class Interface:
    name: str
    type: str = None
    id: uuid.UUID = field(default_factory=lambda: str(uuid.uuid4()))
    alias: Optional[str] = field(default_factory=str)
    device: weakref.ReferenceType[Device] = None
    link: weakref.ReferenceType[Link] = None
    ipv4: ipaddress.IPv4Interface = None
    ipv6: Union[ipaddress.IPv6Interface, List[ipaddress.IPv6Interface]] = None

    def __post_init__(self):
        if not self.alias:
            self.alias = self.name

    @property
    def remote_devices(self) -> Set[Device]:
        # Assume that the Link object has a method or attribute to get all connected devices
        return set(
            device for device in self.link().connected_devices if device != self.device
        )

    @property
    def remote_interfaces(self) -> Set[Interface]:
        # Assume that the Link object has a method or attribute to get all the connected interfaces
        return set(
            interface
            for interface in self.link().connected_interfaces
            if interface != self
        )

    def __hash__(self):
        return hash((self.id))

    def __eq__(self, other):
        if isinstance(other, Interface):
            return self.id == other.id  # or combine other attributes if needed
        return NotImplemented
