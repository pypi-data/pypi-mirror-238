import os
import shutil
import pochi_commands.constants as constants
from logs.manager import LoggingManager


class InitCommand(object):
    def __init__(self, parser):
        # print('init command')
        init_parser = parser.add_parser(
            "init",
            usage="pochi init [--name=<application_package_name>] [--version=<application_version_name>] [--connection=<connection_name] [--distribution={INTERNAL | EXTERNAL}] [--force]",
            description="Create a blank native app project with default folder structure and prebuilt templates in the current folder or in the folder specified with the --name option.",
            help=f"Creates a blank native app project with default folder structure and prebuilt templates in the current folder.\nIf the --name option is specified, create the folder and generate the project in it.",
        )
        init_parser.add_argument(
            "--name",
            nargs="?",
            help="Specify a folder name to create the project inside that folder.",
        )
        init_parser.add_argument(
            "--version",
            nargs="?",
            default="MyFirstVersion",
            help="Specify a version name; default is MyFirstVersion.",
        )
        init_parser.add_argument(
            "--connection",
            nargs="?",
            default="UnknownConnection",
            help="Specify a Snowflake connection; default is UnknownConnection",
        )
        init_parser.add_argument(
            "--distribution",
            nargs="?",
            default="INTERNAL",
            help="Specify an application package distribution; default is INTERNAL",
        )
        init_parser.add_argument(
            "--force",
            action="store_true",
            help="Full init and overwrite any existing files",
        )

    def get_help_text(self):
        help_text = """pochi init [--name=<application_package_name>] [--version=<application_version_name>] [--connection=<connection_name] [--distribution={INTERNAL | EXTERNAL}] [--force]
    Creates a blank native app project with default directory structure and prebuilt templates in the current directory.
        
    Options:
        --name=<application_package_name>           Create the blank native app project in a directory named <application_package_name>
        --version=<application_version_name>        Override the default version name in config/project.toml
        --connection=<conn_name>                    Override the default connection name in config/project.toml
        --distribution={INTERNAL | EXTERNAL}        Override the default application package distribution in config/project.toml
        --force                                     Overwrite an existing project directory with default templates
"""
        return help_text

    def execute(self, options):
        has_errors = False
        LoggingManager.display_message("pochi_header", "INIT")
        if options.init.name is None:
            current_directory = os.path.join(os.getcwd())
        else:
            current_directory = os.path.join(os.getcwd(), options.init.name)
        # print(f"Initializing with name: {options.init.name}")
        if options.init.name:
            # the user specified a name for the project; create a new folder with that name
            # and use the folder as the working directory
            os.makedirs(options.init.name, exist_ok=True)
            os.chdir(options.init.name)
            LoggingManager.display_message(
                "create_project_template",
                current_directory,
            )
        else:
            options.init.name = os.path.split(os.getcwd())[1]
            LoggingManager.display_message("create_project_template", current_directory)

        if options.init.force == True:
            # delete all the files in the current directory
            try:
                # Remove all files and directories within the directory
                for root, dirs, files in os.walk(os.getcwd(), topdown=False):
                    for file in files:
                        file_path = os.path.join(root, file)
                        os.remove(file_path)
                    for dir in dirs:
                        dir_path = os.path.join(root, dir)
                        shutil.rmtree(dir_path)
            except Exception as e:
                has_errors = True
                LoggingManager.display_message("error_ocurred", e)
        elif os.path.exists(os.path.join("config", "project.toml")):
            has_errors = True
            LoggingManager.display_message("project_exists", options.init.name)
            # return

        # Set up config folder
        if os.path.isdir("config") == False:
            os.makedirs("config", exist_ok=True)
            with open(os.path.join("config", "project.toml"), "w") as sql_output:
                sql_output.write(
                    constants.config_project_toml.format(
                        application_package_name=options.init.name,
                        application_version_name=options.init.version,
                        default_connection=options.init.connection,
                        application_package_distribution=options.init.distribution
                    )
                )
            LoggingManager.display_message(
                "project_config_created",
                os.path.join(current_directory, "config", "project.toml"),
            )
        else:
            LoggingManager.display_message(
                "w_already_exists", os.path.join(current_directory, "config")
            )

        # Set up server-side code folder (for App Package)
        if os.path.isdir(os.path.join("src", "application_package")) == False:
            os.makedirs(
                os.path.join("src", "application_package", "sql"), exist_ok=True
            )
            os.makedirs(
                os.path.join("src", "application_package", "sql", "preinstall"),
                exist_ok=True,
            )
            os.makedirs(
                os.path.join("src", "application_package", "sql", "postinstall"),
                exist_ok=True,
            )

            with open(
                os.path.join(
                    "src", "application_package", "sql", "app_pkg_definition_01.sql"
                ),
                "w",
            ) as sql_output:
                sql_output.write(
                    # constants.provider_app_pkg_definition_sql.format(
                    #         application_package_name=options.init.name)
                    constants.provider_app_pkg_definition_sql
                )

            with open(
                os.path.join(
                    "src",
                    "application_package",
                    "sql",
                    "preinstall",
                    "preinstall_definition_01.sql",
                ),
                "w",
            ) as sql_output:
                sql_output.write(
                    # constants.provider_preinstall_definition_sql.format(
                    #         application_package_name=options.init.name)
                    constants.provider_preinstall_definition_sql
                )
            with open(
                os.path.join(
                    "src",
                    "application_package",
                    "sql",
                    "postinstall",
                    "postinstall_definition_01.sql",
                ),
                "w",
            ) as sql_output:
                sql_output.write(
                    # constants.provider_postinstall_definition_sql.format(
                    #         application_package_name=options.init.name)
                    constants.provider_postinstall_definition_sql
                )

            LoggingManager.display_message(
                "source_provider_created",
                os.path.join(current_directory, "src", "application_package"),
            )
        else:
            LoggingManager.display_message(
                "w_already_exists",
                os.path.join(current_directory, "src", "application_package"),
            )

        # Set up client-side code folder (for App Version / App Instance)
        if os.path.isdir(os.path.join("src", "application_logic")) == False:
            os.makedirs(
                os.path.join("src", "application_logic", "python"), exist_ok=True
            )
            os.makedirs(
                os.path.join("src", "application_logic", "resources"), exist_ok=True
            )
            os.makedirs(os.path.join("src", "application_logic", "sql"), exist_ok=True)

            with open(
                os.path.join(
                    "src", "application_logic", "sql", "app_setup_definition_01.sql"
                ),
                "w",
            ) as sql_output:
                sql_output.write(
                    constants.consumer_app_definition_sql.format(
                        application_package_name=options.init.name
                    )
                )

            with open(
                os.path.join("src", "application_logic", "resources", "manifest.yml"),
                "w",
            ) as sql_output:
                sql_output.write(
                    constants.consumer_manifest_yml.format(
                        application_package_name=options.init.name
                    )
                )

            with open(
                os.path.join("src", "application_logic", "resources", "README.md"), "w"
            ) as sql_output:
                sql_output.write(
                    constants.consumer_readme.format(
                        application_package_name=options.init.name
                    )
                )

            LoggingManager.display_message(
                "source_consumer_created",
                os.path.join(current_directory, "src", "application_logic"),
            )
        else:
            LoggingManager.display_message(
                "w_already_exists",
                os.path.join(current_directory, "src", "application_logic"),
            )

        if os.path.isdir("test") == False:
            os.makedirs(os.path.join("test", "testsuite1"), exist_ok=True)
            with open(
                os.path.join("test", "testsuite1", "setup.sql"), "w"
            ) as sql_output:
                sql_output.write(constants.test_setup_sql)

            with open(
                os.path.join("test", "testsuite1", "teardown.sql"), "w"
            ) as sql_output:
                sql_output.write(constants.test_teardown_sql)

            with open(
                os.path.join("test", "testsuite1", "test01.sql"), "w"
            ) as sql_output:
                sql_output.write(constants.test_code_sql)

            LoggingManager.display_message(
                "default_test_created",
                os.path.join(current_directory, "test", "testsuite1"),
            )
        else:
            LoggingManager.display_message(
                "w_already_exists", os.path.join(current_directory, "test")
            )

        if os.path.isfile("README.md") == False:
            with open("README.md", "w") as sql_output:
                sql_output.write(
                    constants.project_readme.format(
                        application_package_name=options.init.name
                    )
                )
            LoggingManager.display_message(
                "default_readme_created", os.path.join(current_directory, "README.md")
            )
        else:
            LoggingManager.display_message(
                "w_already_exists", os.path.join(current_directory, "README.md")
            )

        LoggingManager.display_message("closing_section")
        LoggingManager.display_message(
            "pochi_sucess", ["INIT", "FAILED" if has_errors else "SUCCESS"]
        )
