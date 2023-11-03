from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()


def print_nested_dict(input_dict: dict, level=0, spaces=4):
    """
    Print a nested dictionary with indentation.

    Args:
        input_dict (dict): The dictionary to print.
        spaces (int, optional): The number of spaces to indent. Defaults to 4.
    """
    for key, value in input_dict.items():
        if isinstance(value, dict):
            print(f"{' ' * spaces * level} {Fore.CYAN}{key}{Style.RESET_ALL}:")
            print_nested_dict(value, spaces=spaces, level=level + 1)
        else:
            print(f"{' ' * spaces * level} {Fore.YELLOW}{key}{Style.RESET_ALL}: {Fore.GREEN}{value}{Style.RESET_ALL}")
