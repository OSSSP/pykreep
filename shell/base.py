try:
    import gnureadline
    import sys
    sys.modules['readline'] = gnureadline
except ImportError:
    pass

import cmd
import glob
import os
import logging

import shell.errors

from config import KojikoConfig
from shell.exploit import ExploitShell


class BaseShell(cmd.Cmd):
    prompt = 'K>'
    show_subcommands = ['exploits']

    def do_exploit(self, exploit_name):
        try:
            exploit_shell = ExploitShell(exploit_name)
            exploit_shell.cmdloop()
        except shell.errors.InvalidCommandArgument as err:
            print(str(err))

    def help_exploit(self):
        print('exploit <exploit path>')
        print('    switches to exploit configuration mode')

    def do_show_exploits(self, exploit_path):
        pass

    def complete_show_exploits(self, text, line, begidx, endidx):
        before_arg = line.rfind(' ', 0, begidx)
        if before_arg == -1:
            return  # arg not found

        fixed = line[before_arg + 1:begidx]  # fixed portion of the arg
        arg = line[before_arg + 1:endidx]
        pattern = arg + '*'
        completions = []
        # iter all exploits withing exploits_path
        for path in [match for match in glob.glob(pattern) if match.startswith(KojikoConfig.exploits_path)]:
            if os.path.isdir(path):
                path = path + '/'
                completions.append(path.replace(fixed, '', 1))

        return completions

    def emptyline(self):
        pass

    def do_EOF(self, line):
        return True

    def postloop(self):
        print()
