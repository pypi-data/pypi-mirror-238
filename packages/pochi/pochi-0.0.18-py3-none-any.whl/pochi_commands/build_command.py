import os
import shutil
import logging
import glob
from pathlib import Path
import sys

import yaml

from templates.manager import TemplateManager
from logs.manager import LoggingManager
from utils.helpers import Helpers


class BuildCommand(object):
    def __init__(self, parser):
        # print('build command')
        parser.add_parser("build", help="Build")

    def get_help_text(self):
        help_text = """pochi build
    Build and generate Snowflake artifacts that can be deployed to a Snowflake account. Files are staged in generated/ folder.
"""
        return help_text

    def __refresh_output_folder(self):
        current_directory = os.getcwd()

        if os.path.exists("generated"):
            shutil.rmtree("generated")

        # Create necessary directories
        os.makedirs(os.path.join("generated", "app"), exist_ok=True)
        os.makedirs(os.path.join("generated", "deployment"), exist_ok=True)
        LoggingManager.display_message(
            "output_generated_at", os.path.join(current_directory, "generated")
        )
        LoggingManager.display_message(
            "application_setup_resources_created",
            os.path.join(current_directory, "generated", "app"),
        )
    def __read_sql_files(self, src_dir):
        sql_files = sorted(glob.glob(os.path.join(src_dir, "*.sql")))
        consolidated_output = ""
        if sql_files:
            for sql_file in sql_files:
                with open(sql_file, "r") as sql_input:
                    consolidated_output = consolidated_output + sql_input.read() + "\n"
        return consolidated_output

    def __write_sql_file(self, sql_content, dest_sql_file):
        with open(dest_sql_file, "w") as sql_output:
            sql_output.write(sql_content)

    def __print_footer(self, has_errors):
        LoggingManager.display_message("closing_section")
        LoggingManager.display_message(
            "pochi_sucess", ["BUILD", "FAILED" if has_errors else "SUCCESS"]
        )

    def execute(self, options):
        has_errors = False
        LoggingManager.display_message("pochi_header", "BUILD")
        if options.project_config is None:
            LoggingManager.display_message("not_load_project_config_issue")
            self.__print_footer(True)
            sys.exit()
        dict_project_config = vars(options.project_config)
        parameters = Helpers.toml_dict_to_string(dict_project_config)
        LoggingManager.display_message("building_application_parameters", parameters)
        self.__refresh_output_folder()
        template_manager = TemplateManager(dict_project_config)
        current_directory = os.getcwd()
        LoggingManager.display_message(
            "deployment_created",
            os.path.join(current_directory, "generated", "deployment"),
        )

        # for preinstall files, consolidate all of the SQL files (ordered by file name) in the
        # src/application_package/sql/preinstall directory into generated/deployment/deploy_preinstall_objects.sql
        preinstall_sql_commands = self.__read_sql_files(
            src_dir=os.path.join("src", "application_package", "sql", "preinstall")
        )

        # Verifies that the actual preinstall read files existed or had content
        if preinstall_sql_commands != "":
            self.__write_sql_file(
                template_manager.render_template(preinstall_sql_commands),
                dest_sql_file=os.path.join(
                    "generated", "deployment", "deploy_preinstall_objects.sql"
                ),
            )

            LoggingManager.display_single_message(
                "\tdeploy_preinstall_objects.sql",
            )

        # for app package definition files, consolidate all of the SQL files (ordered by file name) in the
        # src/application_package/sql directory into generated/deployment/deploy_application_package.sql
        # PLUS: Add the CREATE APPLICATION PACKAGE line
        app_pkg_sql_commands = f"""
create application package if not exists {options.project_config.application_package_name} DISTRIBUTION = { options.project_config.application_package_distribution };
use application package {options.project_config.application_package_name};
"""
        app_pkg_sql_commands += self.__read_sql_files(
            src_dir=os.path.join("src", "application_package", "sql")
        )
        self.__write_sql_file(
            template_manager.render_template(app_pkg_sql_commands),
            dest_sql_file=os.path.join(
                "generated", "deployment", "deploy_application_package.sql"
            ),
        )

        LoggingManager.display_single_message(
            "\tdeploy_application_package.sql",
        )

        # Compose the application code directory inside "generated/app" folder.
        # 1. Copy all the resource files (recursively) into generated/app directory
        # This should include the README.md, the manifest.yml, or any other additional resources
        # such as ML models, test data, zip files, images, etc.
        shutil.copytree(
            os.path.join("src", "application_logic", "resources"),
            os.path.join("generated", "app"),
            dirs_exist_ok=True,
        )

        # 2. Copy all the files in the src/application_logic/python directory (recursively) into generated/app/python directory
        src_directory = os.path.join("src", "application_logic", "python")
        if os.path.isdir(src_directory) and len(os.listdir(src_directory))>0:
            shutil.copytree(src_directory,
                        os.path.join("generated", "app", "python"), dirs_exist_ok=True)


        # 3. Copy all the subdirectories in the src/application_logic/sql directory (recursively) into generated/app directory
        # The purpose is to support the scenario where the project has subfolders inside the src/application_logic/sql directory,
        # eg to include streamlit folders, additional SQL files that should be loaded dynamically, etc.
        src_directory = os.path.join("src", "application_logic", "sql")
        target_directory = os.path.join("generated", "app")
        for obj in os.listdir(src_directory):
            obj_path = os.path.join(src_directory, obj)
            if os.path.isdir(obj_path):
                shutil.copytree(obj_path, os.path.join(target_directory, obj), dirs_exist_ok=True)
            elif not obj.endswith(".sql"):
                shutil.copy(obj_path, target_directory)

        # 4. for app code definition (i.e. setup script), consolidate all of the SQL files (ordered by file name) in the
        # src/application_logic/sql directory into generated/app/sql/setup.sql
        app_setup_sql_commands = self.__read_sql_files(
            src_dir=os.path.join("src", "application_logic", "sql")
        )

        path_setup_file = "setup.sql"
        with open(
            os.path.join("src", "application_logic", "resources", "manifest.yml"), "r"
        ) as file:
            yaml_data = yaml.safe_load(file)
            if "artifacts" in yaml_data:
                artifacts = yaml_data["artifacts"]
                if "setup_script" in artifacts:
                    path_setup_file = artifacts["setup_script"]

        setup_file_final_path = os.path.join("generated", "app", path_setup_file)
        os.makedirs(os.path.dirname(setup_file_final_path), exist_ok=True)
        
        self.__write_sql_file(
            template_manager.render_template(app_setup_sql_commands),
            dest_sql_file=os.path.join("generated", "app", path_setup_file),
        )

        # 5. Generate a deployment SQL to perform the following:
        # (a) CREATE STAGE to store the application version files
        # (b) PUT statements to upload all of the files in generated/app directory into the stage
        # (c) ALTER APPLICATION PACKAGE statement to create a new version or add a patch to an existing version using
        #     the stage in (a)

        deploy_app_code_commands = f"""

create schema if not exists {options.project_config.application_package_name}.sourcecode;
create stage if not exists {options.project_config.application_package_name}.sourcecode.{options.project_config.application_version_name};

"""

        upload_sql = ""
        for root, _, files in os.walk(os.path.join("generated", "app")):
            for file in files:
                file_path = os.path.join(root, file)
                full_path = os.path.abspath(file_path)
                relative_path = os.path.relpath(
                    file_path, os.path.join("generated", "app")
                )

                # To support windows clients, we need to convert relative path to posix version for stage/path
                relative_path = Path(relative_path).as_posix()
                # Since relative_path contains the file name, which we don't need for the PUT command, remove the file name
                relative_path = relative_path.rstrip(file)
                # print(relative_path)
                upload_sql += f"PUT 'file://{full_path}' @{options.project_config.application_package_name}.sourcecode.{options.project_config.application_version_name}/{relative_path} auto_compress=false overwrite=true;\n"

        deploy_app_code_commands += upload_sql
        deploy_app_code_commands += f"""
----------------------------------------------------------------------------------------------------------------
-- Create a new version or a new patch for an existing version using the files uploaded in the named stage.
-- To change the application package name or the version name, edit config/project.config, and your changes will
-- automatically propagate throughout the generated SQL files.
--
-- See Docs:
-- https://docs.snowflake.com/en/developer-guide/native-apps/versioning
-- https://docs.snowflake.com/en/sql-reference/sql/alter-application-package-version
----------------------------------------------------------------------------------------------------------------
execute immediate $$
declare
  QUERY_RESULT_NUMBER integer;
begin
    show versions in application package {options.project_config.application_package_name};
    select count(*) into :QUERY_RESULT_NUMBER from table(result_scan(last_query_id())) where "version"=UPPER('{options.project_config.application_version_name}');
    
    if (QUERY_RESULT_NUMBER = 0) then
        alter application package {options.project_config.application_package_name}
            add version {options.project_config.application_version_name} using '@{options.project_config.application_package_name}.sourcecode.{options.project_config.application_version_name}';
        return '{options.project_config.application_package_name} added';
    else
        alter application package {options.project_config.application_package_name}
            add patch for version {options.project_config.application_version_name} using '@{options.project_config.application_package_name}.sourcecode.{options.project_config.application_version_name}';
        
        select "patch" into :QUERY_RESULT_NUMBER from table(result_scan(last_query_id()));
        return 'Version {options.project_config.application_version_name} Patch ' || QUERY_RESULT_NUMBER || ' added';
    end if;
end;
$$;
"""

        self.__write_sql_file(
            template_manager.render_template(deploy_app_code_commands),
            dest_sql_file=os.path.join(
                "generated", "deployment", "deploy_application_logic.sql"
            ),
        )

        LoggingManager.display_single_message(
            "\tdeploy_application_logic.sql",
        )

        # for postinstall files, consolidate all of the SQL files (ordered by file name) in the
        # src/application_package/sql/postinstall directory into generated/deployment/deploy_postinstall_objects.sql
        postinstall_sql_commands = self.__read_sql_files(
            src_dir=os.path.join("src", "application_package", "sql", "postinstall")
        )

        if postinstall_sql_commands != "":
            self.__write_sql_file(
                template_manager.render_template(postinstall_sql_commands),
                dest_sql_file=os.path.join(
                    "generated", "deployment", "deploy_postinstall_objects.sql"
                ),
            )

            LoggingManager.display_single_message(
                "\tdeploy_postinstall_objects.sql",
            )

        self.__print_footer(has_errors)
