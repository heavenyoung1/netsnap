import wmi
from typing import NamedTuple

from logger import logger


class AdapterInfo(NamedTuple):
    name: str
    dhcp_enabled: bool
    ip: str
    subnet: str
    gateway: str | None
    dns_enabled: bool
    dns_servers: list[str] | None


class AdapterManager:
    def __init__(self):
        self._wmi = wmi.WMI()

    def get_adapters(self) -> dict[str, AdapterInfo]:
        '''Returns all active network adapters with their current settings.'''
        net_adapters = self._wmi.Win32_NetworkAdapterConfiguration

        output = {
            adapter.Description: AdapterInfo(
                name=adapter.Description,
                dhcp_enabled=adapter.DHCPEnabled,
                ip=adapter.IPAddress[0],
                subnet=adapter.IPSubnet[0],
                gateway=(
                    adapter.DefaultIPGateway[0] if adapter.DefaultIPGateway else None
                ),
                dns_enabled=adapter.DNSServerSearchOrder is not None,
                dns_servers=adapter.DNSServerSearchOrder,
            )
            for adapter in net_adapters(IPEnabled=True)
        }
        return output

    def get_adapter_config(self, adapter_name: str) -> AdapterInfo | None:
        output = self.get_adapters().get(adapter_name)
        logger.info(output)
        return output
