import cmd2


class AbstractShell(cmd2.Cmd):
    def do_quit(self, arg):
        exit(0)

    def do_exit(self, arg):
        self.do_quit(arg)
