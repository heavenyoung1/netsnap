import argparse
import sys

from adapter_wmi import AdapterManager
from profile_store import ProfileStore
from adapter_applier import AdapterApplier


def cmd_list(store: ProfileStore):
    profiles = store.list_profiles()
    if not profiles:
        print('No saved profiles')
        return

    # Head Table
    print(f'{"NAME":<20} {"ADAPTER":<25} {"TYPE":<8} {"IP"}')
    print('-' * 65)

    for name, data in profiles.items():
        adapter = data.get('adapter', '-')
        if data.get('dhcp'):
            type_ = 'DHCP'
            ip = '-'
        else:
            type_ = 'static'
            ip = data.get('ip', '-')
        print(f'{name: <20} {adapter: <25} {type_: <8} {ip}')


def cmd_save(
    profile_name: str,
    adapter_name: str,
    store: ProfileStore,
    manager: AdapterManager,
):
    exist_profile = store.get_profile(profile_name)
    if exist_profile:
        print(f'Profile {profile_name} already exists')
        sys.exit(1)
    exist_adapter = manager.get_adapter_config(adapter_name)
    if not exist_adapter:
        print(f'Adapter {adapter_name} not exists')
        sys.exit(1)

    # Converting AdapterInfo to dict
    profile = {
        'name': exist_adapter.name,
        'adapter': exist_adapter.adapter,
        'dhcp': exist_adapter.dhcp_enabled,
        'ip': exist_adapter.ip,
        'subnet': exist_adapter.subnet,
        'gateway': exist_adapter.gateway,
        'dns1': exist_adapter.dns_servers[0] if exist_adapter.dns_servers else None,
        'dns2': (
            exist_adapter.dns_servers[1]
            if exist_adapter.dns_servers and len(exist_adapter.dns_servers) > 1
            else None
        ),
    }

    store.save_profile(profile_name, profile)
    print(f'Profile {profile_name} saved. Configs - {profile}')

def cmd_show(
        manager: AdapterManager,
        adapter_name: str, 
        ):
    adapter_config = manager.get_adapter_config(adapter_name)
    if not adapter_config:
        print('Not existed adapter name')
    for key, value in adapter_config._asdict().items():
        print(f'{key.capitalize:<15} - {value}')
    

def cmd_apply(
    profile_name: str, 
    store: ProfileStore, 
    applier: AdapterApplier,
):
    profile = store.get_profile(profile_name)
    if profile is None:
        print(f'Profile {profile_name} was not found')
        sys.exit(1)

    adapter = profile.get('name')
    if not adapter:
        print('Adapter not specify')
        sys.exit(1)

    applier.apply_profile(adapter, profile)
    print(f'Profile "{profile_name}" to "{adapter}" successfully set')


def cmd_delete(profile_name: str, store: ProfileStore):
    '''Delete a profile by name.'''
    if store.delete_profile(profile_name):
        print(f'Profie successfully {profile_name} deleted')
    else:
        print(f'Profile {profile_name} was not found')
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='netsnap - switching network profiles'
        )
    sub = parser.add_subparsers(dest='command')

    # netsnap list
    sub.add_parser('list', help='List profiles')

    # netsnap show --adapter 'Wi-Fi'
    p_show = sub.add_parser('show', help='Show current adapter')
    p_show.add_argument('--adapter', required=True, help='Adapter name')

    # netsnap apply work --adapter 'Wi-Fi'
    p_apply = sub.add_parser('apply', help='Apply profile')
    p_apply.add_argument('name', help='Name profile')
    p_apply.add_argument('--adapter', default=None, help='Adapter name')

    # netsnap save work --adapter 'Wi-Fi'
    p_save = sub.add_parser('save', help='Save current configured adapter')
    p_save.add_argument('name', help='Name profile')
    p_save.add_argument('--adapter', required=True, help='Adapter name')

    # netsnap delete work
    p_delete = sub.add_parser('delete', help='Delete profile')
    p_delete.add_argument('name', help='Profile name for remove')

    args = parser.parse_args()
    applier = AdapterApplier()
    manager = AdapterManager()
    store = ProfileStore()

    if args.command == 'list':
        cmd_list(store)

    elif args.command == 'apply':
        cmd_apply(args.adapter, args.name, store, applier)

    elif args.command == 'show':
        cmd_show(manager, args.adapter)

    elif args.command == 'delete':
        cmd_delete(args.name, store)

    elif args.command == 'save':
        cmd_save(args.name, args.adapter, store, manager)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
