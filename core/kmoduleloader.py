import core.exploit.kexploit as kexploit
import core.errors
from config import KojikoConfig

import os
import os.path
import sys
import inspect
import importlib

class KModuleLoader:
    def __init__(self):
        pass

    def load_exploit(self, path: str) -> kexploit.KExploit:
        exploit_file = os.path.basename(path)
        save_dir = os.getcwd()
        save_syspath = sys.path
        try:
            os.chdir(path)

            try:
                sys.path.append(os.getcwd())
                module = importlib.import_module(exploit_file)
                #module = __import__(exploit_file)
            except ImportError as err:
                raise core.errors.ModuleError(str(err) + '\nCannot load module \'{}\'.'
                                              ' Cannot import {}.py file.'.format(path, exploit_file))

            kexploit_classes = inspect.getmembers(module, predicate=self._is_subclass_of_kexploit)
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
