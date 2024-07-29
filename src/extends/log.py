import builtins
from colorama import Fore

original_print = builtins.print

def print(*args, **kwargs):
    prefix = Fore.CYAN + ""
    original_print(prefix, *args, **kwargs)
