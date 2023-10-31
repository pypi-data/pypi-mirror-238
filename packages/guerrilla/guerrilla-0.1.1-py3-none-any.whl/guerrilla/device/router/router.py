from guerrilla.device.base import BaseDevice
from guerrilla.device.router import Commands
from dataclasses import dataclass
from guerrilla.device.router.mode import MODE
import re
from guerrilla.logging import logger
from guerrilla.utils.decorator import mode
from typing import override


class RouterShowMixin:
    @mode(MODE.MAIN)
    def show_version(self) -> str:
        return self.run(Commands.SHOW.VERSION.value)

    @mode(MODE.MAIN)
    def show_interfaces_wan(self) -> str:
        return self.run(Commands.SHOW.INTERFACES_WAN.value)


@dataclass
class Router(BaseDevice, RouterShowMixin):
    @override
    def run(self, command: str, expect_return: str = None) -> str:
        result = self.session.run(command, expect_return=expect_return)
        if "^Parse error" in result:
            logger.warning(f"Command '{command}' not accepted")
        return result

    def check_mode(self) -> str:
        """
        Checks the mode of the remote device.

        Returns:
        --------
        str
            The mode of the device.
        """
        PATTERNS = [
            (r"\(config-if\)#$", MODE.CONFIG_IF),
            (r"\(config\)#$", MODE.CONFIG),
            (r"#$", MODE.MAIN),
        ]

        prompt = self.find_prompt()
        for pattern, mode in PATTERNS:  # noqa: F402
            if re.search(pattern, prompt):
                return mode.value
        raise ValueError("Unknown device mode detected.")

    @mode(MODE.MAIN)
    def reload_factory_default(self) -> None:
        self.run(Commands.SYSTEM.FACTORY_DEFAULT.value)
        self.run("Y")

    @mode(MODE.CONFIG)
    def create_vlan(self, vlan_id: str) -> None:
        self.run(Commands.CONFIG.VLAN(vlan_id))
