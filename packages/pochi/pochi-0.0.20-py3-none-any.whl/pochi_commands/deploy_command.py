import os
from logs.manager import LoggingManager
from pochi_commands.pochi_util import PochiUtil
import sys


class DeployCommand(object):
    def __init__(self, parser):
        # print('deploy command')
        deploy_parser = parser.add_parser(
            "deploy", help="Deploy application_package or application_logic"
        )
        deploy_parser.add_argument(
            "--application-package",
            action="store_true",
            help="Deploy application_package",
        )
        deploy_parser.add_argument(
            "--application-logic", action="store_true", help="Deploy application_logic"
        )

        self.pochi_util = PochiUtil()

    def get_help_text(self):
        help_text = """pochi deploy [--application-logic|--application-package]
    Create an application package and generate a new version/patch in the target Snowflake account specified in config/project.toml.
    This command automatically runs the build command, and then executes the deployment SQL scripts to create an Application Package,
    set up shared content, push application code into a stage, and add a version/patch.
        
    Options:
        --application-logic                         Deploy only the native app application logic and create a new patch.
        --application-package                       Deploy only the native app package or other objects in the provider account.
"""
        return help_text

    def execute(self, options):
        has_errors = False
        LoggingManager.display_message("pochi_header", "DEPLOY")
        if options.project_config.default_connection is None:
            LoggingManager.display_message("connection_file_missing")
            has_errors = True
        else:
            has_errors = self.pochi_util.get_connection(options)

        if options.default_connection is None:
            LoggingManager.display_message(
                "invalid_connection_name_issue",
                options.project_config.default_connection,
            )
            has_errors = True

        if not has_errors:
            if options.deploy.application_logic:
                has_errors = self.__deployment_sequence(
                    "application version code",
                    options,
                    False,
                    False,
                    True,
                    True,
                    True,
                    has_errors,
                )
            elif options.deploy.application_package:
                has_errors = self.__deployment_sequence(
                    "application package side code",
                    options,
                    True,
                    True,
                    False,
                    False,
                    False,
                    has_errors,
                )
            else:
                has_errors = self.__deployment_sequence(
                    "full application package",
                    options,
                    True,
                    True,
                    True,
                    True,
                    True,
                    has_errors,
                )

        LoggingManager.display_message("closing_section")
        LoggingManager.display_message(
            "pochi_sucess", ["DEPLOY", "FAILED" if has_errors else "SUCCESS"]
        )
        if has_errors:
            sys.exit(-1)

    def __deployment_sequence(
        self,
        deployment,
        options,
        deployment_preinstall_scripts,
        deployment_app_package_def,
        deployment_version_code,
        deployment_postinstall_scripts,
        app_package_info,
        has_errors=False,
    ):
        if has_errors:
            return has_errors

        LoggingManager.display_message(
            "deployment_info",
            [
                deployment,
                options.default_connection.account,
                options.project_config.default_connection,
            ],
        )
        if deployment_preinstall_scripts:
            file_path = os.path.join(
                    "generated", "deployment", "deploy_preinstall_objects.sql"
                )
            if os.path.isfile(file_path):
                LoggingManager.display_message("deployment_preinstall_scripts")
                has_errors = self.pochi_util.execute_sql_from_file(
                file_path,
                has_errors,
                False
                )
                if has_errors:
                    return has_errors
        
        if deployment_app_package_def:
            file_path = os.path.join(
                    "generated", "deployment", "deploy_application_package.sql"
                )
            if os.path.isfile(file_path):
                LoggingManager.display_message("deployment_app_package_def")
                has_errors = self.pochi_util.execute_sql_from_file(
                    file_path,
                    has_errors,
                    False
                )
                if has_errors:
                    return has_errors

        patch_number = None
        if deployment_version_code:
            file_path = os.path.join("generated", "deployment", "deploy_application_logic.sql")
            if os.path.isfile(file_path):
                LoggingManager.display_message("deployment_version_code")
                has_errors = self.pochi_util.execute_sql_from_file(
                    file_path,
                    has_errors,
                    False
                )
                if has_errors:
                    return has_errors
                else:
                    self.pochi_util.execute_sql(
                        "show versions in application package {};".format(
                        options.project_config.application_package_name
                        ),
                    )

                    _, output = self.pochi_util.execute_sql(
                        'select max("patch") from table(result_scan(last_query_id())) where "version"=upper(\'{}\');'.format(
                            options.project_config.application_version_name
                        ),
                        with_output=True,
                    )

                    patch_first_row_tuple = output[0] if len(output) > 0 else (0,)
                    patch_number = patch_first_row_tuple[0] if len(patch_first_row_tuple) > 0 else 0

        if deployment_postinstall_scripts:
            file_path = os.path.join(
                    "generated", "deployment", "deploy_postinstall_objects.sql"
                )
            if os.path.isfile(file_path):
                LoggingManager.display_message("deployment_postinstall_scripts")
                has_errors = self.pochi_util.execute_sql_from_file(
                    file_path,
                    has_errors,
                    False
                )
                if has_errors:
                    return has_errors
                
        if app_package_info and patch_number is not None:
            LoggingManager.display_message(
                "app_package_info",
                [
                    options.project_config.application_package_name,
                    options.project_config.application_version_name,
                    patch_number,
                ],
            )

        return has_errors
