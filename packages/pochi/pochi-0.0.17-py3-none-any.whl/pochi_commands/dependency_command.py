class DependencyCommand(object):
    def __init__(self, parser):
        # print('dependency command')
        parser.add_parser("dependency", help="Handle dependencies")
    def execute(self, options):
        print("Dependency Command is not implemented.")