import cmd2
import glob
import os
from shell.util import print_err

import core.errors
from config import KreepConfig
from shell.exploit import ExploitShell
from core.kmoduleloader import KModuleLoader

class BaseShell(cmd2.Cmd):
    prompt = 'K:>'
    show_subcommands = ['exploits']

    @cmd2.options([
        cmd2.make_option('-l', '--list', action='store_true', help='Lists all known exploits'),
        cmd2.make_option('-i', '--info', action='store_true', help='Shows specific exploit info')
    ], arg_desc='\nRun/List/Describe exploit')
    def do_exploit(self, use_path, opts=None):
        loader = KModuleLoader()
        if opts.list:
            return loader.list_exploits()
        elif opts.info:
            if not use_path:
                return print_err('No exploit identifier provided for info')
            else:
                return loader.info_exploit(use_path[0])

        if not use_path:
            return print_err('Specify exploit identifier')

        try:
            exploit_shell = ExploitShell(use_path[0])
            exploit_shell.cmdloop()
        except core.errors.InvalidCommandArgumentError as err:
            print(str(err))
        except core.errors.ModuleError as err:
            print(str(err))


    def complete_exploit(self, text, line, begidx, endidx):
        before_arg = line.rfind(' ', 0, begidx)
        if before_arg == -1:
            return  # arg not found

        fixed = line[before_arg + 1:begidx]  # fixed portion of the arg
        arg = line[before_arg + 1:endidx]
        pattern = arg + '*'
        completions = []
        # iter all exploits withing exploits_path
        for path in [match for match in glob.glob(pattern) if match.startswith(KreepConfig.exploits_path)]:
            if os.path.isdir(path):
                path = path + '/'
                completions.append(path.replace(fixed, '', 1))

        return completions

    def emptyline(self):
        pass

    #def do_EOF(self, line):
    #    return True

    def preloop(self):
        print('Ctrl-D or quit to exit environment\n')
