import subprocess
import re

class AdapterManager:
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

        return result
    
    def get_adapters(self):
        output = self._run('netsh interface ip show config')
        adapters = {}
        current = None

        
    

    
