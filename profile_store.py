import os
import json

# Folder where profile_store.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class ProfileStore:
    '''
    A simple profile storage backed by a JSON file.

    A profile is a dict with network settings.
    Example DHCP profile (home):
    {
        'adapter': 'Wi-Fi',
        'dhcp': true
    }

    Example static IP profile (work):
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

    def __init__(self, filepath: str = None):
        # Path to the profiles file (defaults to the same folder as this script)
        self.filepath = filepath or os.path.join(BASE_DIR, 'profiles.json')
        # Load profiles from disk on startup.
        # If the file doesn't exist yet, start with an empty dict.
        self._data: dict = self._load()

    def _load(self):
        '''Read the JSON file from disk. If the file doesn't exist, return an empty dict.'''
        if os.path.exists(self.filepath):
            with open (self.filepath, encoding='utf-8') as file:
                return json.load(file)

        return {}

    def _save(self):
        '''Write the current profiles dict back to the JSON file.'''
        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump(self._data, file, ensure_ascii=False, indent=2)

    def list_profiles(self):
        '''Return all profiles. Used by the "list" command.'''
        return self._data

    def get_profile(self, name):
        '''
        Get a profile by name.
        Returns None if the profile is not found.
        '''
        return self._data.get(name)

    def save_profile(self, name: str, profile: dict):
        '''Save a profile under the given name and write it to disk.'''
        self._data[name] = profile
        self._save()

    def delete_profile(self, name: str):
        '''
        Delete a profile by name.
        Returns True if deleted, False if not found.
        '''
        if name in self._data:
            del self._data[name]
            self._save()
            return True
        return False
