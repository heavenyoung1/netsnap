import argparse
import sys
from logger import logger

from profile_store import ProfileStore
from adapter_applier import AdapterApplier

def cmd_list(store: ProfileStore):
    profiles = store.list_profiles()
    if not profiles:
        logger.warning('Нет сохраненных профилей')
        return
    for name, data in profiles.items():
        print(f'{name} - {data}')


def cmd_apply(adapter_name: str, profile_name: str, store: ProfileStore, applier: AdapterApplier):
    profile = store.get_profile(profile_name)
    if profile is None:
        logger.error(f'Профиль "{profile_name}" не найден')
        sys.exit(1)

    adapter = adapter_name or profile.get('adapter')  # ← из аргумента или из профиля
    if not adapter:
        print('Адаптер не указан')
        sys.exit(1)

    applier.apply_profile(adapter, profile)


def cmd_delete(profile_name: str, store: ProfileStore):
    """Delete a profile by name."""
    if store.delete_profile(profile_name):
        logger.info(f'Профиль "{profile_name}" удалён')
    else:
        logger.error(f'Профиль "{profile_name}" не найден')
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='netsnap — смена сетевых профилей')
    sub = parser.add_subparsers(dest='command')

    # команда: python main.py list
    sub.add_parser('list', help='Список профилей')

    # команда: python main.py apply work --adapter "Беспроводная сеть"
    p_apply = sub.add_parser('apply', help='Применить профиль')
    p_apply.add_argument('name', help='Имя профиля')
    p_apply.add_argument('--adapter', default=None, help='Имя адаптера')

    # команда: python main.py delete work
    p_delete = sub.add_parser('delete', help='Удалить профиль')
    p_delete.add_argument('name', help='Имя профиля для удаления')

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