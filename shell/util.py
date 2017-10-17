from colorama import Fore


def color_str(string, color):
    return color + string + Fore.RESET


def color_print(string, color):
    print(color_str(string, color))


def print_err(err):
    color_print(err, Fore.RED)