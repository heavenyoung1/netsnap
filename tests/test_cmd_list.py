import io
import sys
import types
import unittest
from contextlib import redirect_stdout


adapter_wmi_stub = types.ModuleType('adapter_wmi')
adapter_wmi_stub.AdapterManager = object
sys.modules.setdefault('adapter_wmi', adapter_wmi_stub)

adapter_applier_stub = types.ModuleType('adapter_applier')
adapter_applier_stub.AdapterApplier = object
sys.modules.setdefault('adapter_applier', adapter_applier_stub)

import main


class DummyStore:
    def __init__(self, profiles):
        self._profiles = profiles

    def list_profiles(self):
        return self._profiles


class CmdListFormattingTests(unittest.TestCase):
    def test_list_keeps_columns_aligned_for_empty_and_long_adapter_names(self):
        profiles = {
            'missing-adapter': {
                'dhcp': True,
            },
            'long-adapter': {
                'adapter': 'Intel(R) Ethernet Connection (16) I219-V Extra Long Name',
                'dhcp': False,
                'ip': '192.168.0.10',
            },
        }

        buf = io.StringIO()
        with redirect_stdout(buf):
            main.cmd_list(DummyStore(profiles))

        lines = buf.getvalue().splitlines()
        self.assertEqual(lines[0], 'NAME                 ADAPTER                   TYPE     IP')
        self.assertEqual(lines[1], '-' * 65)

        missing_adapter_type_index = lines[2].index('DHCP')
        long_adapter_type_index = lines[3].index('static')

        self.assertEqual(missing_adapter_type_index, 47)
        self.assertEqual(long_adapter_type_index, 47)
        self.assertIn('Intel(R) Ethernet Conn...', lines[3])


if __name__ == '__main__':
    unittest.main()
