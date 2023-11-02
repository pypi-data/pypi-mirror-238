pochi_header = "--- POCHI {} ----------------------------------------------"
create_project_template = "Creating the project template in {}"
error_ocurred = "Error: An error occurred: {}"
project_exists = "Error: A Project {} already exists, use --force option to overwrite the project files"
project_config_created = "Project config file created at {}"
w_already_exists = "Warning: {} already exists, skipping..."
source_provider_created = "Source files for application package created in {}"
source_consumer_created = "Source files for application logic created in {}"
default_test_created = "Default tests created in {}"
default_readme_created = "Default README.md created in {}"
closing_section = "-------------------------------------------------------------"
pochi_sucess = "POCHI {}: {}\n"
building_application_parameters = """Building application package using the following parameters: 
{}"""
display_application_parameters = """Project configuration parameters: 
{}"""
output_generated_at = "Output directory created at {}"
application_setup_resources_created = (
    "Application Setup script and resources created in {}"
)
deployment_created = "Deployment Scripts created in {}"
deployment_info = "Deploying {} to Snowflake Account {} with connection {}"
deployment_version_code = "Deploying application logic"
deployment_postinstall_scripts = "Deploying postinstall scripts"
deployment_preinstall_scripts = "Deploying preinstall scripts"
deployment_app_package_def = "Deploying application package definition"
app_package_info = "Application Package {} Version {} Patch {} created."
connection_issues = "Error: Failed to connect to {} using connection {}"
script_issues = "Error: {} failed: {}"
connection_file_missing = "Error: Connection config file not found."
connection_name_issue = (
    "Error: Connection default_connection is not a valid connection name."
)
running_test = "Running Test {}"
dropping_app_pkg = "Dropping Application Package {}"
removing_generated_out = "Removing generated output directory {}"
parameter_config_issue = "Invalid parameters for pochi config. See help for details"
set_config_parameter = "Setting paramter {} to {} in config/project.toml"
missing_parameters_connection_issue = "Error: Connection config file does not contain either username, password or accountname parameters"
missing_private_key_passphrase_connection_issue = "Error: private key passphrase is not defined in environment variable SNOWSQL_PRIVATE_KEY_PASSPHRASE"
invalid_connection_name_issue = 'Error: Invalid config parameter. default_connection = "{}" is not a valid connection name.'
not_load_project_config_issue = (
    "Error: Not able to load project config. Run the build command inside root folder"
)
test_suite_status = "Test {}: {}"
not_existent_test_file_issue = "Error: Specified Test file ({}) does not exists"
not_existent_test_suite_issue = "Error: Specified Test suite ({}) does not exists"
wrong_testing_parameter_syntax = "Error: Syntax error for testing parameter."
