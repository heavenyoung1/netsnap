import subprocess

class AdapterApplier:

    def _run(self, cmd: str):
        '''
        Выполнить команду в cmd и вернуть её вывод как строку.

        encoding="cp866" — кодировка Windows-консоли в России (она же OEM 866).
        Без неё кириллица в выводе netsh превращается в кракозябры.
        errors="replace" — если символ не распознан, подставить '?' вместо краша.
        '''
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True, # перехватываем stdout и stderr
            text=True,
            encoding='cp866',
            errors='replace',
        )
        return result.stdout

    def apply_profile(self, adapter_name: str, profile: dict):
        '''
        Применить профиль к адаптеру.
        Определяет тип профиля (DHCP или статика) и вызывает нужные netsh-команды.
        '''
        if profile.get('dhcp'):
            self._set_dhcp_ip(adapter_name)
            self._set_dhcp_dns(adapter_name)
        else:
            self._set_static_ip(
                adapter_name,
                ip_address_v4=profile['ip'],
                ip_subnet=profile.get('subnet', '255.255.255.0'),
                ip_gateway=profile.get('gateway', ''),
            )
            dns1 = profile.get('dns1')
            dns2 = profile.get('dns2')
            if dns1:
                self._set_static_dns(adapter_name, dns1, dns2)

    def _set_static_ip(self, adapter: str, ip_address_v4: str, ip_subnet: str, ip_gateway: str):
        # netsh interface ip set address name="adapter" static ip mask gateway
        self._run(
            cmd=f'netsh interface ip set address name="{adapter}" static {ip_address_v4} {ip_subnet} {ip_gateway}'
        )

    def _set_dhcp_ip(self, adapter_name: str):
        self._run(f'netsh interface ip set address name="{adapter_name}" dhcp')

    def _set_static_dns(self, adapter: str, dns1: str, dns2: str | None = None):
        '''
        Задать статические DNS-серверы.
        Сначала устанавливаем основной (index=1), потом добавляем альтернативный (index=2).
        '''
        # set dns — заменяет весь список DNS (сбрасывает старые записи)
        self._run(
            f'netsh interface ip set dns name="{adapter}" static {dns1}'
        )
        if dns2:
            # add dns — добавляет второй DNS не трогая первый
            self._run(
                f'netsh interface ip add dns name="{adapter}" {dns2} index=2'
            )

    def _set_dhcp_dns(self, adapter: str):
        self._run(
            cmd=f'netsh interface ip set dns name="{adapter}" dhcp'
        )
