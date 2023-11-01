import sys
from pochi_commands.pochi_commands import PochiCommandManager
import logging

# Configure logger to also write to stdout
root = logging.getLogger()
root.setLevel(logging.ERROR)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

def main():
    pochi_command_manager = PochiCommandManager()
    argument_list = [word if word not in ['--help', '-h', '-help'] else 'help' for word in sys.argv[1:]]
    pochi_command_manager.execute_commands(argument_list or ["help"])