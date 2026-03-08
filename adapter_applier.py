import subprocess

class AdapterApplier:

    def _run(self, cmd: str):
        '''
        Run a command in cmd and return its output as a string.

        encoding="cp866" — the Windows console encoding used in Russian locale (OEM 866).
        Without it, Cyrillic characters in netsh output turn into garbage.
        errors="replace" — if a character can't be decoded, put "?" instead of crashing.
        '''
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True, # capture both stdout and stderr
            text=True,
            encoding='cp866',
            errors='replace',
        )
        return result.stdout

    def apply_profile(self, adapter_name: str, profile: dict):
        '''
        Apply a profile to the adapter.
        Checks whether the profile is DHCP or static, then runs the right netsh commands.
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
        Set static DNS servers.
        First set the primary DNS (index=1), then add the secondary one (index=2).
        '''
        # "set dns" replaces the whole DNS list (clears old entries)
        self._run(
            f'netsh interface ip set dns name="{adapter}" static {dns1}'
        )
        if dns2:
            # "add dns" adds a second DNS without touching the first one
            self._run(
                f'netsh interface ip add dns name="{adapter}" {dns2} index=2'
            )

    def _set_dhcp_dns(self, adapter: str):
        self._run(
            cmd=f'netsh interface ip set dns name="{adapter}" dhcp'
        )
