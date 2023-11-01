import sys
from logs.manager import LoggingManager
from pochi_commands.pochi_util import PochiUtil
import shutil
import os


class CleanCommand(object):
    def __init__(self, parser):
        # print('clean command')
        parser.add_parser("clean", help="Clean")
        self.pochi_util = PochiUtil()

    def get_help_text(self):
        help_text = """pochi clean
    Drop deployed Application Package and remove generated files.
"""
        return help_text

    def __get_footer(self, has_errors):
        LoggingManager.display_message("closing_section")
        LoggingManager.display_message(
            "pochi_sucess", ["CLEAN", "FAILED" if has_errors else "SUCCESS"]
        )

    def execute(self, options):
        has_errors = False
        current_directory = os.getcwd()
        # print("Cleaning")
        LoggingManager.display_message("pochi_header", "CLEAN")
        # (1) run DROP APPLICATION PACKAGE options.project_config.application_package_name
        has_errors = self.pochi_util.get_connection(options)

        if has_errors:
            self.__get_footer(has_errors=has_errors)
            sys.exit()
        LoggingManager.display_message(
            "dropping_app_pkg", options.project_config.application_package_name
        )

        has_errors = self.pochi_util.execute_sql(
            "DROP APPLICATION PACKAGE IF EXISTS {application_package_name}".format(
                application_package_name=options.project_config.application_package_name
            )
        )

        LoggingManager.display_message(
            "removing_generated_out", os.path.join(current_directory, "generated")
        )

        # (2) delete generated directory
        if os.path.exists("generated"):
            shutil.rmtree("generated")

        self.__get_footer(has_errors=has_errors)
