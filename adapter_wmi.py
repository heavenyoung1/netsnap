import wmi
from typing import NamedTuple


class AdapterInfo(NamedTuple):
    name: str
    adapter: str
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
        _adapter_configurations = self._wmi.Win32_NetworkAdapterConfiguration
        adapter_configurations = _adapter_configurations(IPEnabled=True)
        adapters = self._wmi.Win32_NetworkAdapter()

        name_map = {
            adapter.Name: adapter.NetConnectionID 
            for adapter in adapters 
            if adapter.NetConnectionID
        }

        output = {} 
        for adapter_config in adapter_configurations:
            display_name = name_map.get(adapter_config.Description)
            output[display_name] = AdapterInfo(
                name=display_name,
                adapter=adapter_config.Description,
                dhcp_enabled=adapter_config.DHCPEnabled,
                ip=adapter_config.IPAddress[0],
                subnet=adapter_config.IPSubnet[0],
                gateway=(
                    adapter_config.DefaultIPGateway[0] if adapter_config.DefaultIPGateway else None
                ),
                dns_enabled=adapter_config.DNSServerSearchOrder is not None,
                dns_servers=adapter_config.DNSServerSearchOrder,
            )

        return output
       

    def get_adapter_config(self, adapter_name: str) -> AdapterInfo | None:
        output = self.get_adapters().get(adapter_name)
        return output
