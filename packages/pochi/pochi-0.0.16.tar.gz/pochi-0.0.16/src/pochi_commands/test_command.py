import os
import re
import sys
from logs.manager import LoggingManager
from pochi_commands.pochi_util import PochiUtil
from templates.manager import TemplateManager


class TestCommand(object):
    def __init__(self, parser):
        test_parser = parser.add_parser("test", help="Run tests")
        self.pochi_util = PochiUtil()

        test_parser.add_argument(
            "--tests",
            nargs="?",
            help="Specify test suites/test files to be run.",
        )

    def get_help_text(self):
        help_text = """pochi test [--tests=<testsuite>[.<testname>][,...]]
    Run the all of the test suites defined in the test directory or specified in the --tests option.
    
    Options:
        --tests=<testsuite>[.<testname>][,...]      Specify one or more test suites or test files, separated by commas.
                                                    To run test/testsuite1/test01.sql:  --tests=testsuite1.test01
                                                    To run multiple test suites:        --tests=testsuite1,testsuite2
                                                    To mix-and-match tests:             --tests=testsuite1,testsuite2.test03

"""
        return help_text

    def __get_footer(self, has_errors):
        LoggingManager.display_message("closing_section")
        LoggingManager.display_message(
            "pochi_sucess", ["TEST", "FAILED" if has_errors else "SUCCESS"]
        )

    def execute(self, options):
        has_errors = False
        regex = r"^[\"\']?(.*?)[\"\']?(?:\.[\"\']?(test.*?)[\"\']?)?$"
        LoggingManager.display_message("pochi_header", "TEST")
        if "test" in options:
            test_namespace = options.test
            dict_test_suite_files = {}
            if "tests" in test_namespace:
                if test_namespace.tests is not None:
                    test_string = test_namespace.tests
                    tests_to_run = test_string.split(",")

                    for test_to_run in tests_to_run:
                        match_test = re.search(regex, test_to_run)
                        if match_test:
                            if match_test.group(2) is None:
                                dict_test_suite_files[match_test.group(1)] = None

                            else:
                                if match_test.group(1) in dict_test_suite_files:
                                    dict_test_suite_files[match_test.group(1)].append(
                                        match_test.group(2)
                                    )
                                else:
                                    dict_test_suite_files[match_test.group(1)] = [
                                        match_test.group(2)
                                    ]

                        else:
                            LoggingManager.display_message(
                                "wrong_testing_parameter_syntax"
                            )
                            has_errors = True

            self.__test(options, dict_test_suite_files, has_errors=has_errors)
        else:
            print("there is no test info")

    def __test(self, options, dict_test_suite_files, has_errors=False):
        
        has_errors = self.pochi_util.get_connection(options)

        if has_errors:
            self.__get_footer(has_errors=has_errors)
            sys.exit()

        dict_project_config = vars(options.project_config)
        template_manager = TemplateManager(dict_project_config)

        os.makedirs(os.path.join("generated", "test"), exist_ok=True)

        if not dict_test_suite_files:
            sorted_test_directories = sorted(os.listdir("test"))
            for test_suite_directory in sorted_test_directories:
                dict_test_suite_files[test_suite_directory] = None

        dict_test_suite_files_keys = dict_test_suite_files.keys()
        last_list_test_suites = len(dict_test_suite_files_keys) - 1
        test_suite_has_errors = False
        for index, testsuite in enumerate(dict_test_suite_files_keys):
            test_suite_has_errors = False
            if os.path.isdir(os.path.join("test", testsuite)):
                # this is the test suite.
                test_setup_sql = ""
                test_teardown_sql = ""
                test_code_sql = ""

                if dict_test_suite_files[testsuite] is None:
                    dict_test_suite_files[testsuite] = sorted(
                        os.listdir(os.path.join("test", testsuite))
                    )
                else:

                    dict_test_suite_files[testsuite].append("setup")
                    dict_test_suite_files[testsuite].append("teardown")

                    dict_test_suite_files[testsuite] = list(
                                map(
                                    lambda x: f"{x}.sql",
                                    dict_test_suite_files[testsuite],
                                )
                            )

                LoggingManager.display_message("running_test", testsuite)

                for file in dict_test_suite_files[testsuite]:
                    path_to_test_file = os.path.join("test", testsuite, file)

                    if file.startswith("test"):
                        if os.path.isfile(path_to_test_file):
                            with open(path_to_test_file, "r") as sql_input:
                                test_code_sql += sql_input.read() + "\n"
                        else:
                            test_suite_has_errors = True
                            LoggingManager.display_message(
                                "not_existent_test_file_issue", path_to_test_file
                            )
                            break

                    if file == "setup.sql" and os.path.isfile(path_to_test_file):
                        with open(path_to_test_file, "r") as sql_input:
                            test_setup_sql = sql_input.read() + "\n"
                    
                    if file == "teardown.sql" and os.path.isfile(path_to_test_file):
                        with open(path_to_test_file, "r") as sql_input:
                            test_teardown_sql = sql_input.read() + "\n"

                if not test_suite_has_errors:
                    test_suite_file = os.path.join(
                        "generated", "test", testsuite + ".sql"
                    )
                    with open(test_suite_file, "w") as sql_output:
                        sql_output.write(
                            template_manager.render_template(
                                test_setup_sql + test_code_sql + test_teardown_sql
                            )
                        )

                    test_suite_has_errors = self.pochi_util.execute_sql_from_file(
                        test_suite_file, query_logging=True
                    )
            else:
                test_suite_has_errors = True
                LoggingManager.display_message(
                                "not_existent_test_suite_issue", testsuite
                )

            has_errors = test_suite_has_errors or has_errors

            LoggingManager.display_message(
                    "test_suite_status",
                    [testsuite, "FAILED" if test_suite_has_errors else "SUCCESS"],
                )
            if index != last_list_test_suites:
                LoggingManager.display_single_message("")



        self.__get_footer(has_errors=has_errors)
