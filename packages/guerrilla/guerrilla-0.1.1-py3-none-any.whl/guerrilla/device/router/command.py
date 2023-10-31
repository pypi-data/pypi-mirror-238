from enum import Enum


class Commands:
    class SHOW(Enum):
        VERSION = "show version"
        CLOCK = "show clock"
        INTERFACES_WAN = "show interfaces wan"
        INTERFACES_LAN = "show interfaces lan"

    class SYSTEM(Enum):
        EXIT = "exit"
        CONFIGURE = "configure"
        FACTORY_DEFAULT = "reload factory-default"

    class CONFIG(Enum):
        def VLAN(vlan_id):
            return f"vlan create {vlan_id}"

        def HOSTNAME(hostname):
            return f"hostname {hostname}"
