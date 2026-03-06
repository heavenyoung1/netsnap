import wmi

c = wmi.WMI()
net_adapters = c.Win32_NetworkAdapterConfiguration


# Win32_NetworkAdapterConfiguration — это таблица всех сетевых адаптеров
# IPEnabled=True — только те у которых включён IP (отсекаем виртуальные/bluetooth)
for adapter in net_adapters(IPEnabled=True):
    desc = adapter.Description                      # Адаптер
    dhcp_enabled = adapter.DHCPEnabled              # DHCP
    ip_address_v4 = adapter.IPAddress[0]            # IP
    ip_subnet = adapter.IPSubnet[0]                 # Маска
    ip_gateway = adapter.DefaultIPGateway or None   # Шлюз
    dns_server = adapter.DNSServerSearchOrder       # DNS
    print('Адаптер  :', desc)
    print('DHCP     :', dhcp_enabled)
    print('IP       :', ip_address_v4)
    print('Маска    :', ip_subnet)
    print('Шлюз     :', ip_gateway)
    print('DNS      :', dns_server)
    print('---')