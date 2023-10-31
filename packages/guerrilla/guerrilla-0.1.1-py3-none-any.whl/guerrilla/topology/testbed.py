from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Union

from guerrilla.utils.type import DefaultBox as Box

if TYPE_CHECKING:
    from guerrilla.topology import Device, Link


@dataclass
class Testbed:
    name: str
    devices: Union[Dict[str, Device], List[Device]] = field(default_factory=Box)
    tacacs: Dict[str, Union[str, int]] = field(default_factory=dict)
    passwords: Dict[str, str] = field(default_factory=dict)
    credentials: Dict[str, str] = field(default_factory=Box)
    servers: Dict[str, Dict] = field(default_factory=dict)
    clean: Dict[str, Union[str, int, float]] = field(default_factory=dict)
    custom: Dict[str, Union[str, int, float]] = field(default_factory=dict)
    testbed_file: Optional[str] = None
    alias: Optional[str] = None

    def __post_init__(self):
        if not self.alias:
            self.alias = self.name
        # Convert list of devices to dictionary if necessary
        if isinstance(self.devices, list):
            self.devices = Box({device.name: device for device in self.devices})

    @property
    def links(self) -> Set[Link]:
        links = set()
        for device in self.devices.values():
            links.update(device.links)
        return links

    def add_device(self, device: Device) -> Dict[str, Device]:
        self.devices[device.name] = device
        return self.devices

    def remove_device(self, device: Device) -> Dict[str, Device]:
        if device in self.devices.values():
            del self.devices[device.name]
        return self.devices

    def squeeze(self, *device_names: str) -> Dict[str, Device]:
        # Implementation depends on criteria for 'unwanted' devices, interfaces, and links.
        self.devices = {
            name: device
            for name, device in self.devices.items()
            if name in device_names
        }
        return self.devices

    # TODO - Implement methods for ConnectionManager
    # def connect(self, devices: Optional[Union[str, List[str]]] = None):
    #     """Connects to all or multiple devices in the testbed in parallel together."""
    #     for device in devices or self.devices.values():
    #         device.connection_manager.connect()

    # def disconnect(self, devices: Optional[Union[str, List[str]]] = None):
    #     """Disconnects all or multiple devices in the testbed in parallel together."""
    #     for device in devices or self.devices.values():
    #         device.connection_manager.disconnect()

    # def destroy(self, devices: Optional[Union[str, List[str]]] = None):
    #     """Destroys all or multiple device connections in the testbed in parallel together."""
    #     for device in devices or self.devices.values():
    #         device.connection_manager.destroy()

    # def execute(self, command: str, devices: Optional[Union[str, List[str]]] = None):
    #     """Executes commands against all or multiple devices in the testbed in parallel together."""
    #     results = {}
    #     for device in devices or self.devices.values():
    #         results[device.name] = device.connection_manager.execute(command)  # Assuming the Device class has an execute method
    #     return results

    # def configure(self, config: str, devices: Optional[Union[str, List[str]]] = None):
    #     # Implementation depends on your configure method(s).
    #     pass

    # def parse(self, command: str, devices: Optional[Union[str, List[str]]] = None):
    #     # Implementation depends on your parse method(s).
    #     pass

    def __iter__(self):
        yield from (device for device in self.devices.values())
