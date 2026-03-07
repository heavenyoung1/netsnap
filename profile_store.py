import os
import json



class ProfileStore:
    '''
    Простое хранилище профилей на основе JSON-файла.

    Профиль — это словарь с настройками сети.
    Пример DHCP-профиля (дом):
    {
        'adapter': 'Wi-Fi',
        'dhcp': true
    }

    Пример статического профиля (работа):
    {
        'adapter': 'Wi-Fi',
        'dhcp': false,
        'ip': '10.157.1.227',
        'subnet': '255.255.255.0',
        'gateway': '10.157.1.1',
        'dns1': '10.157.100.7',
        'dns2': '10.155.10.6'
    }
    '''

    def __init__(self, filepath: str = 'profiles.json'):
        # Путь к файлу с профилями (по умолчанию рядом со скриптом)
        self.filepath = filepath
        # Загружаем профили из файла при старте.
        # Если файла ещё нет — начинаем с пустого словаря.
        self._data: dict = self._load()

    
    def _load(self):
        '''Читаем JSON-файл с диска. Если файла нет — возвращаем пустой словарь.'''
        if os.path.exists(self.filepath):
            with open (self.filepath, encoding='utf-8') as file:
                return json.load(file)
            
        return {}
    
    def _save(self):
       '''Сохраняем текущий словарь профилей обратно в JSON-файл.''' 
       with open (self.filepath, 'w', encoding='utf-8') as file:
            # indent=2        — красивое форматирование с отступами
            # ensure_ascii=False — кириллица сохраняется как есть, не в \uXXXX
           json.dump(self._data, file, ensure_ascii=False, indent=2)

    def list_profiles(self):
        '''Вернуть все профили. Используется в команде 'list'.'''
        return self._data
    
    def get_profile(self, name):
        '''
        Получить профиль по имени.
        Возвращает None если профиль не найден.
        '''
        return self._data.get(name)
    
    def save_profile(self, name: str, profile: dict):
        '''Сохранить профиль под заданным именем и записать на диск.'''
        self._data[name] = profile
        self._save()

    def delete_profile(self, name: str):
        '''
        Удалить профиль по имени.
        Возвращает True если удалён, False если не найден.
        '''
        if name in self._data:
            del self._data[name]
            self._save()
            return True
        return False
    
        