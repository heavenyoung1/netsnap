import wmi
from typing import NamedTuple

from logger import logger

class AdapterInfo(NamedTuple):
    name: str
    dhcp_enabled: bool
    ip_address_v4: str
    ip_subnet: str
    ip_gateway: str | None
    dns_enabled: bool
    dns_servers: list[str] | None

class AdapterManager:
    def __init__(self):
        self._wmi = wmi.WMI()
        #self._cache : dict[str, AdapterInfo] | None = None

    def get_adapters(self) -> list[dict]:
        '''Возвращает список активных сетевых адаптеров с их конфигурацией.'''
        # Win32_NetworkAdapterConfiguration — это таблица всех сетевых адаптеров
        # IPEnabled=True — только те у которых включён IP (отсекаем виртуальные/bluetooth)
        net_adapters = self._wmi.Win32_NetworkAdapterConfiguration

        output = {
            adapter.Description: AdapterInfo(
                name=adapter.Description,
                dhcp_enabled=adapter.DHCPEnabled,
                ip_address_v4=adapter.IPAddress[0],
                ip_subnet=adapter.IPSubnet[0],
                ip_gateway=adapter.DefaultIPGateway[0] or None,
                dns_enabled=adapter.DNSServerSearchOrder is not None,
                dns_servers=adapter.DNSServerSearchOrder,
            )
            for adapter in net_adapters(IPEnabled=True)
        }
        #logger.info(output)
        return output

    def get_adapter_config(self, adapter_name: str) -> AdapterInfo | None:
        output = self.get_adapters().get(adapter_name)
        logger.info(output)
        return output
    
# ------------------------------------------------------------------
# Низкоуровневые netsh-команды (приватные методы)
# ------------------------------------------------------------------








cli = AdapterManager()
cli.get_adapter_config('Intel(R) Wi-Fi 6 AX201 160MHz')

