from pathlib import Path

import yaml
from box import Box

from guerrilla.topology import Device, Interface, Link, Testbed


def load(file_path: str):
    fp = Path(file_path)
    assert fp.is_file(), f"File not found: {fp}"
    assert fp.suffix in [".yaml", ".yml"], f"File must be a YAML file: {fp}"

    with open(fp, "r", encoding="utf-8") as file:
        data = Box(yaml.safe_load(file))

    # Create Testbed
    testbed = Testbed(**data["testbed"], testbed_file=fp.resolve())

    # Load topology (interfaces and links)
    link_objects = {}  # Dictionary to store Link objects by their names

    # Load devices
    for device_name, device_data in data["devices"].items():
        device = Device(**device_data)
        testbed.add_device(device)

    # Load topology (interfaces and links)
    for device_name, topology_data in data["topology"].items():
        device = testbed.devices[device_name]
        # print(topology_data.interfaces.items())
        for interface_name, interface_data in topology_data["interfaces"].items():
            # print(interface_name, interface_data)
            interface = Interface(name=interface_name, **interface_data)
            device.add_interface(interface)

            # Create or get the link and connect the interface
            link_name = interface_data["link"]
            if link_name not in link_objects:
                link_objects[link_name] = Link(name=link_name)
            link = link_objects[link_name]
            link.connect_interface(interface)
            interface.link = link

    return data, testbed
