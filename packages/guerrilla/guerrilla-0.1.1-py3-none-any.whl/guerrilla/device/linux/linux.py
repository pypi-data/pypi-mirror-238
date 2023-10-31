from guerrilla.device.base import BaseDevice
from dataclasses import dataclass
from guerrilla.device.linux import Commands
from typing import List


@dataclass
class Linux(BaseDevice):
    def flush_ip(self, dev: str) -> None:
        self.run(Commands.FLUSH_IP(dev))

    def set_networks(self, dev: str, ip: List[str], mask: List[str]) -> None:
        self.flush_ip(dev)
        self.run(
            'echo "source-directory /etc/network/interfaces.d" > /etc/network/interfaces'
        )
        config = (
            f"auto {dev}\niface {dev} inet static\naddress {ip[0]}\nnetmask {mask[0]}"
        )
        self.run(f'echo "{config}" > /etc/network/interfaces.d/{dev}')
        for i in range(1, len(ip)):
            self.run(
                f'echo "up ip addr add {ip[i]}/{mask[i]} dev {dev}" >> /etc/network/interfaces.d/{dev}'
            )
