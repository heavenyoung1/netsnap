import argparse
import sys

from profile_store import ProfileStore
from adapter_applier import AdapterApplier

def cmd_list(store: ProfileStore):
    profiles = store.list_profiles()
    if not profiles:
        print('No saved profiles')
        return
    for name, data in profiles.items():
        print(f'{name} - {data}')


def cmd_apply(adapter_name: str, profile_name: str, store: ProfileStore, applier: AdapterApplier):
    profile = store.get_profile(profile_name)
    if profile is None:
        print(f'Profile {profile_name} was not found')
        sys.exit(1)

    adapter = adapter_name or profile.get('adapter')
    if not adapter:
        print('Adapter not specify')
        sys.exit(1)

    applier.apply_profile(adapter, profile)
    print(f'Adapter {profile_name} successfully set')


def cmd_delete(profile_name: str, store: ProfileStore):
    '''Delete a profile by name.'''
    if store.delete_profile(profile_name):
        print(f'Profie successfully {profile_name} deleted')
    else:
        print(f'Profile {profile_name} was not found')
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='netsnap - switching network profiles')
    sub = parser.add_subparsers(dest='command')

    # command: python main.py list
    sub.add_parser('list', help='List profiles')

    # command: python main.py apply work --adapter "Wi-Fi"
    p_apply = sub.add_parser('apply', help='Apply profile')
    p_apply.add_argument('name', help='Name profile')
    p_apply.add_argument('--adapter', default=None, help='Adapter name')

    # command: python main.py delete work
    p_delete = sub.add_parser('delete', help='Delete profile')
    p_delete.add_argument('name', help='Profile name for remove')

    args = parser.parse_args()
    store = ProfileStore()
    applier = AdapterApplier()

    if args.command == 'list':
        cmd_list(store)
    elif args.command == 'apply':
        cmd_apply(args.adapter, args.name, store, applier)
    elif args.command == 'delete':
        cmd_delete(args.name, store)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()