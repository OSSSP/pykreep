import core.exploit.kexploit as kexploit
import core.errors
from config import KreepConfig

import os
import os.path
import sys
import inspect
import importlib


class KModuleLoader:
    def __init__(self):
        pass

    def list_exploits(self):
        print('Listing all exploits')

    def info_exploit(self, path):
        print('Showing exploit info')

    # path must point to parent folder of exploit file
    # e.g. unix/vsftpd_234_backdoor
    # also, exploit main file must be of name same as its parent folder
    # e.g. unix/vsftpd_234_backdoor/vsftpd_234_backdoor.py
    def load_exploit(self, path: str) -> kexploit.KExploit:
        if path.endswith('/'):
            path = path[:-1]
        path = os.path.join(KreepConfig.exploits_path, path)

        exploit_file = os.path.basename(path)
        save_dir = os.getcwd()
        save_syspath = sys.path
        try:
            try:
                os.chdir(path)
            except FileNotFoundError:
                raise core.errors.ModuleError('Cannot load module \'{}\'. '
                                              'Invalid exploit identifier'.format(path))

            try:
                sys.path.append(os.getcwd())
                mod = importlib.import_module(exploit_file)
            except ImportError as err:
                raise core.errors.ModuleError(str(err) + '\nCannot load module \'{}\'.'
                                              ' Cannot import {}.py file.'.format(path, exploit_file))

            kexploit_classes = inspect.getmembers(mod, predicate=self._is_subclass_of_kexploit)
            if not kexploit_classes:
                raise core.errors.ModuleError('Module \'{}\' does not contain class which '
                                              'inherits core.exploit.kexploit.KExploit class'.format(path))

            if len(kexploit_classes) > 1:
                raise core.errors.ModuleError('Module \'{}\' contains multiple classes deriving '
                                              'core.exploit.kexploit.KExploit class, expecting exactly one'.format(path))

            kexploit_class = kexploit_classes[0][1]  # [(name, class), ...]
            kexploit_instance = kexploit_class()
            kexploit_instance.init()
            return kexploit_instance

        finally:
            os.chdir(save_dir)

    def _is_subclass_of_kexploit(self, member) -> bool:
        return inspect.isclass(member) and issubclass(member, kexploit.KExploit)
