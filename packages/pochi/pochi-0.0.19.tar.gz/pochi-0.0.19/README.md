# Pochi - a Snowflake Native App Build Automation Tool

## Important
This application is not part of the Snowflake Service and is governed by the terms in LICENSE, unless expressly agreed to in writing.  You use this application at your own risk, and Snowflake has no obligation to support your use of this application.

## Overview
Pochi is a Command-Line Interface (CLI) tool that allows a user to create, build, deploy, and test [Snowflake native applications](https://docs.snowflake.com/en/developer-guide/native-apps/native-apps-about) with simple commands. Pochi is built using the [Snowflake Connector for Python](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector).

What Pochi is / does:
* streamlines the end-to-end Snowflake native application development experience using industry-standard CLI commands
* uses a simple project structure that closely matches with native application concepts while giving developers control on source file management
* generates and automates SQL commands to deploy and test native applications
* supports Snowflake implementation in the following languages: SQL, Javascript, and Python
* supports parameter substitution to simplify code customizations

What Pochi is not / does not do:
* Pochi does not integrate with [SnowCLI](https://github.com/Snowflake-Labs/snowcli) and is not a replacement
* Pochi does not support compiling Java / generating JAR files at this time; you can build your JAR files using your established processes, and use Pochi to deploy them along with the other application resource files
* Pochi does not support testing using multiple Snowflake accounts
* Pochi does not include commands to create or manage marketplace listings
* Pochi does not include commands to manage CI/CD or release management

## Install Pochi
To use Pochi, you need the following:
1. Python (>= 3.10)
2. [SnowCLI](https://github.com/Snowflake-Labs/snowcli) or [SnowSQL](https://docs.snowflake.com/en/user-guide/snowsql)

To install Pochi, run this command in a terminal:
```
% pip install pochi
```

## Pochi Command Cheat Sheet

| Command           | Description              |
|-------------------|--------------------------|
|[`pochi init`](#initialize-a-pochi-native-app-project-directory) | Initialize a Pochi Native App Project Directory |
|[`pochi config`](#add-or-update-project-configuration) | Add or Update Project Configuration |
|[`pochi build`](#build-the-application-artifacts-and-generate-deployment-scripts) | Build the Application Artifacts and Generate Deployment Scripts |
|[`pochi deploy`](#deploy-the-application-package-to-snowflake) | Deploy the Application Package to Snowflake |
|[`pochi test`](#run-test-suites-on-snowflake) | Run Test Suites on Snowflake |
|[`pochi clean`](#clean-the-project) | Clean the Project |



# Building Native App with Pochi

## Before You Start

Native Application development can be broken down into roughly the following parts:

### Application Logic
[Application logic](https://docs.snowflake.com/en/developer-guide/native-apps/adding-application-logic) includes functions, procedures, tables / views, stages, or any other objects that are created in a consumer account during the application installation or upgrade process. The SQL code that defines these objects is referred to as the ["Setup Script"](https://docs.snowflake.com/en/developer-guide/native-apps/creating-setup-script)

The source code for application logic is located in the `src/application_logic` directory.

Note: Native Application Framework does not allow an installed application to use functions/procedures/stages in the provider account.

### Shared Data Content
[Shared Data Content](https://docs.snowflake.com/en/developer-guide/native-apps/preparing-data-content) refers to data (schemas, tables, views) that are *shared* with the installed applications. You must create the Shared Data Content objects in the application package in the provider account. Views in share data content can select from databases outside of the application package (but still in the same provider account).

The source code for shared data content is located in the `src/application_package` directory.

## Project Directory Structure

The default project directory is as follows:
![Project Directory](https://drive.google.com/uc?id=1CxBVGJR3JMF-VNgSF0azNsiZT6E31K07)

1. **Project configuration file**<br>
This config file contains the default Snowflake connection name and application package name, among other parameters. You can edit the config file directly, or use the `pochi config` command to update or add parameters. You can directly reference any parameter in your SQL files using this format: `{{parameter_name}}`.  By default, the config file has the following required parameters:<br>
   |Parameter                 |Description                                                 |
   |--------------------------|------------------------------------------------------------|
   |`application_package_name`|the name of the Application Package|
   |`application_version_name`|the name of the version being worked on (default: MyFirstVersion)|
   |`application_package_distribution`|application package distribution mode (default: INTERNAL)|
   |`default_connection`|the Snowflake connection name to deploy the Application Package|

2. **Application Package and Shared Data Content**<br>
This directory defines all of the SQL commands that need to be executed on the provider account to create the application package.

3. **SQL files for Shared Data Content**<br>
A default file `app_pkg_definition_01.sql` is included for you to create shared data content (and other objects) inside the application package. You can create multiple SQL files with any naming of your choice. When you run `pochi build`, the SQL files in this directory are ordered by the file names in alphanumeric order, and then consolidated into the output directory, in `generated/deployment/deploy_application_package.sql`.

4. **SQL files to be run on the provider account *before* the application package object is created**<br>
A default file `preinstall_definition_01.sql` is included for you to incorporate SQL commands that should be run before the application package is created. You can create multiple SQL files with any naming of your choice. When you run `pochi build`, the SQL files in this directory are ordered by the file names in alphanumeric order, and then consolidated into the output directory, in `generated/deployment/deploy_preinstall_objects.sql`.

5. **SQL files to be run on the provider account, *after* a new application version or patch has been added**<br>.
A default file `postinstall_definition_01.sql` is included for you to incorporate SQL commands that should be run after the application package is created and a new version or patch has been added. You can create multiple SQL files with any naming of your choice. When you run `pochi build`, the SQL files in this directory are ordered by the file names in alphanumeric order, and then consolidated into the output directory, in `generated/deployment/deploy_postinstall_objects.sql`.

6. **Application logic**<br>
This directory defines all of the SQL commands that make up the application setup script and any additional resource files that will be created in the consumer's account during the application installation or upgrade process.

7. **SQL files for the Application Setup Script**<br>
The SQL files in this directory define the application logic and are later consolidated into the application setup script. A default file `app_setup_definition_01.sql` is included for you to define the application logic. You can create multiple SQL files with any naming of your choice. When you run `pochi build`, the SQL files in this directory are ordered by the file names in alphanumeric order, and then consolidated into the application setup script in the output directory, in `generated/app/`, with the exact file name / path defined based on the manifest definition in the `src/application_logic/resources/manifest.yml`. In addition, a SQL deployment script to upload the application files is generated in the output directory, in `generated/deployment/deploy_versioned_code.sql`.

8. **Application Resource files**<br>
This directory defines all of the required resource files, libraries, zip files, and any other files that should be included as part of the application such as `manifest.yml` and `README.md`. When you run `pochi build`, all files and subdirectories in the directory are automatically consolidated into the output directory, `generated/app`.


9. **Python Modules / Libraries**<br>
This directory defines all of the python modules that should be included as part of the application. When you run pochi build, all files and subdirectories in the directory are automatically consolidated into the output directory, `generated/app`.


10. **Test Directory**<br>
This directory contains subdirectories of test suites.


11. **Test Suite**<br>
Each test suite contains default test SQL files: `setup.sql`, then `test*.sql`, and then `teardown.sql`. When you run `pochi test`, the files are consolidated into the output directory, `generated/test/<testsuite_name>.sql`, and the test suite SQL is run on Snowflake.

## Create a Hello-World App
To create a hello-world app (i.e. an application that has a function that returns "Hello World"), you need to:
* Create a consumer-side schema and the Hello World function using [Versioned Schema](https://docs.snowflake.com/sql-reference/sql/create-versioned-schema)
* Grant access on the schema and the function to an [Application Role](https://docs.snowflake.com/en/sql-reference/sql/create-application-role)

You first create the HelloWorld project directory by running the following commands on command-line:
```
% pochi init --name=HelloWorld --connection=<Your_Connection_Name>
% cd HelloWorld
```

Then, using a text editor or IDE, you insert the following application logic code into `src/application_logic/sql/app_setup_definition_01.sql`:
```sql
-- Define a versioned schema to maintain logic objects such as UDFs/Procedures
CREATE OR ALTER VERSIONED SCHEMA api;

-- A humble hello-world function
CREATE OR REPLACE FUNCTION api.hello()
RETURNS VARCHAR
LANGUAGE JAVASCRIPT
AS $$
   return 'Hello World';
$$;

-- Create an application role; this is how you grant privileges on application
-- objects to a customer.
CREATE APPLICATION ROLE IF NOT EXISTS APPOWNER;
GRANT USAGE ON SCHEMA api TO APPLICATION ROLE APPOWNER;
GRANT USAGE ON FUNCTION api.hello() TO APPLICATION ROLE APPOWNER;
```

Then, to incorporate test code, you use a Text Editor or your IDE to add the following SQL to `test/testsuite1/test01.sql`
```sql
-- Call the helloworld function, using parameter-substitution from project.toml
SELECT {{application_package_name}}_Client.api.hello();
```

Now, you deploy and test your HelloWorld App by running the following command in a command-line console:
```
% pochi deploy test
```
You should see that the application package was deployed and that `testsuite1` was run successfully. You can check Query History in Snowsight to validate that:
* The HelloWorld application package was deployed successfully, 
* An application called `HelloWorld_Client` was created,
* `HelloWorld_Client.api.hello()` was invoked and returned "Hello World", and
* The `HelloWorld_Client` application was dropped.


## Add Shared Data Content to the Hello-World App
To add [Shared Data Content](https://docs.snowflake.com/en/developer-guide/native-apps/preparing-data-content) into a native app, you need to:
* Create a provider-side schema and a data object (eg table)
* Grant access on the schema and the table to a special SHARE in the application package
* Use the shared data content object in the application code normally

Building on the example above, using a text editor or IDE, you insert the following share data content SQL code into `src/application_package/sql/app_pkg_definition_01.sql`. This code defines the shared schema/data in the application package.
```sql
-- Create a schema for the shared data content
CREATE OR REPLACE SCHEMA shared_schema;

-- Create a table in the shared data content schema
CREATE OR REPLACE TABLE shared_schema.shared_data (DESCRIPTION VARCHAR);
INSERT INTO shared_schema.shared_data (DESCRIPTION) values ('Hello World From Shared Content');

-- Grant these objects to SHARE IN APPLICATION PACKAGE <pkg_name> to allow
-- the application code access to the shared data content objects.
GRANT USAGE ON SCHEMA shared_schema TO SHARE IN APPLICATION PACKAGE {{application_package_name}};
GRANT SELECT ON TABLE shared_schema.shared_data TO SHARE IN APPLICATION PACKAGE {{application_package_name}};
```

Using a test editor or an IDE, insert the following application logic code into `src/application_logic/sql/app_setup_definition_01.sql`
```sql
-- Define a UDF that uses the shared data content
CREATE OR REPLACE FUNCTION api.hello_from_shared_content()
RETURNS VARCHAR
AS 'SELECT description FROM shared_schema.shared_data LIMIT 1';

-- Grant the UDF to the application role
GRANT USAGE ON FUNCTION api.hello_from_shared_content() TO APPLICATION ROLE APPOWNER;
```

Finally, insert the following test SQL code into the test file `test/testsuite1/test01.sql`
```sql
-- Call the helloworld function that uses the shared data content
SELECT {{application_package_name}}_Client.api.hello_from_shared_content();
```


Now, you deploy and test your updated HelloWorld App by running the following command:
```
% pochi deploy test
```

You should see that the application package was deployed and that testsuite1 was run successfully. You can check Query History in Snowsight to validate that:
* `HelloWorld_Client.api.hello_from_shared_content()` was invoked and returned "Hello World From Shared Content"


## Add Reference Database as Shared Data Content to the Hello-World App
To add a reference database as shared data content into a native app, in addition to the work for a standard shared data content, you also need to:
* Grant [REFERENCE_USAGE](https://docs.snowflake.com/en/developer-guide/native-apps/preparing-data-content#referencing-objects-that-exist-outside-the-application-package) on the source database to the application package

Building on the example above, using a text editor or IDE, you insert the following SQL code into `src/application_package/sql/preinstall/preinstall_definition_01.sql`. This code defines the reference database in the provider account.
```sql
-- Create a Reference Database in the Provider Account
CREATE OR REPLACE DATABASE ReferenceDatabase;
CREATE OR REPLACE SCHEMA ReferenceDatabase.reference_schema;
CREATE OR REPLACE TABLE ReferenceDatabase.reference_schema.reference_data (DESCRIPTION VARCHAR);

-- Inserting a stub reference data that will be surfaced via the app
INSERT INTO ReferenceDatabase.reference_schema.reference_data (DESCRIPTION) values ('Hello World From Reference Database');
```


Then, you insert the following shared data content code into `src/application_package/sql/app_pkg_definition_01.sql`. This code defines the shared schema/data in the application package.
```sql
-- Create a View in the shared data content schema using the reference database
CREATE OR REPLACE VIEW shared_schema.reference_data AS
   SELECT DESCRIPTION FROM ReferenceDatabase.reference_schema.reference_data;

-- You need to grant REFERENCE_USAGE on the reference database to the app pkg
-- BEFORE you can grant the VIEW
GRANT REFERENCE_USAGE ON DATABASE ReferenceDatabase TO SHARE IN APPLICATION PACKAGE {{application_package_name}};

-- Grant these objects to SHARE IN APPLICATION PACKAGE <pkg_name> to allow
-- the application code access to the shared data content objects.
GRANT SELECT ON VIEW shared_schema.reference_data TO SHARE IN APPLICATION PACKAGE {{application_package_name}};
```

Using a test editor or an IDE, insert the following application logic code into `src/application_logic/sql/app_setup_definition_01.sql`
```sql
-- Define a UDF that uses the reference data in shared data content
CREATE OR REPLACE FUNCTION api.hello_from_reference_data()
RETURNS VARCHAR
AS 'SELECT description FROM shared_schema.reference_data LIMIT 1';

-- Grant the UDF to the application role
GRANT USAGE ON FUNCTION api.hello_from_reference_data() TO APPLICATION ROLE APPOWNER;
```

Finally, insert the following code into the test code in `test/testsuite1/test01.sql`
```sql
-- Call the helloworld function that uses the shared data content
SELECT {{application_package_name}}_Client.api.hello_from_reference_data();
```

Now, you deploy and test your updated HelloWorld App by running the following command:
```
% pochi deploy test
```


You should see that the application package was deployed and that `testsuite1` was run successfully. You can check Query History in Snowsight to validate that:
* `HelloWorld_Client.api.hello_from_reference()` was invoked and returned "Hello World from Reference Data"

## Add a Python Module and Python UDF into the Hello-World App
To add a python UDF that imports a python module, you need to
* Add the python module to `src/application_logic/python` directory
* Add the UDF to the `src/application_logic/sql/app_setup_definition_01.sql` with a [relative import](https://docs.snowflake.com/en/developer-guide/native-apps/adding-application-logic#using-external-python-files).

Building on the example above, using a text editor or IDE, create a new python module named `calculator.py` in `src/application_logic/python/` and paste the following code:
```python
def add(num1, num2):
  return num1+num2
```

Using a test editor or an IDE, insert the following application logic code into `src/application_logic/sql/app_setup_definition_01.sql`:
```sql
-- Define a UDF that imports the calculator.py module with relative imports
CREATE or replace FUNCTION api.add(num1 float, num2 float)
  RETURNS float
  LANGUAGE PYTHON
  RUNTIME_VERSION=3.8
  IMPORTS = ('/python/calculator.py')
  HANDLER='calculator.add';

-- Grant the UDF to the application role
GRANT USAGE ON FUNCTION api.add(FLOAT, FLOAT) TO APPLICATION ROLE APPOWNER;
```

Finally, insert the following test SQL code into the test file `test/testsuite1/test01.sql`:
```sql
SELECT {{application_package_name}}_Client.api.add(10, 5);
```

Now, you deploy and test your updated HelloWorld App by running the following command:
```
% pochi deploy test
```

You should see that the application package was deployed and that testsuite1 was run successfully. You can check Query History in Snowsight to validate that, in addition to the expected output from the Hello World App, you also see that:
* `HelloWorld_Client.api.add(10, 5)` was invoked and returned 15

<blockquote>
<br>
<p><b>Note</b></p>

In this example, you added the `calculator.py` python module into the `src/application_logic/python` directory, and your function referenced the file as `/python/calculator.py`. Technicall, you have the option of adding the python module in the `src/application_logic/python` directory or `src/application_logic/resources` directory. When you run `pochi build`, the files and subdirectories in both of those directories will all automatically be packaged into the application artifacts.

For example, you can add `calculator.py` to:
* `src/application_logic/python`, and use `/python/calculator.py` as the relative import path in your function
* `src/application_logic/python/lib`, and use `/python/lib/calculator.py` as the relative import path
* `src/application_logic/resources/lib`, and use `/lib/calculator.py` as the relative import path
* `src/application_logic/resources/python`, and use `/python/calculator.py` as the relative import path

You also can include zip files of python modules, and they are packaged the same way.
<br><br>
</blockquote>

## Add a Streamlit into the Hello-World App
To add a [streamlit](https://docs.snowflake.com/en/developer-guide/native-apps/adding-streamlit) to a native app, you need to:
* Add the streamlit python module
* Add the Streamlit DDL to the `src/application_logic/sql/app_setup_definition_01.sql` with relative import.

Building on the example above, using a text editor or IDE, create a new python module named `helloworld_streamlit.py` in `src/application_logic/python/` and paste the following code:
```python
# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title("Hello World in Streamlit")
st.write(
   """Display reference data.
   """
)

# Get the current credentials
session = get_active_session()

#  Create an example data frame
data_frame = session.sql("SELECT * FROM shared_schema.reference_data;")

# Execute the query and convert it into a Pandas data frame
queried_data = data_frame.to_pandas()

# Display the Pandas data frame as a Streamlit data frame.
st.dataframe(queried_data, use_container_width=True)
```

Using a test editor or an IDE, insert the following application logic code into `src/application_logic/sql/app_setup_definition_01.sql`
```sql
-- Define the Streamlit with relative imports
CREATE STREAMLIT api.helloworld_streamlit
  FROM '/python'
  MAIN_FILE = '/helloworld_streamlit.py';

-- Grant the Streamlit to the application role
GRANT USAGE ON STREAMLIT api.helloworld_streamlit TO APPLICATION ROLE APPOWNER;
```

Because we cannot test streamlits programmatically via SQL, we will need to verify the Streamlit in Snowsight. One way to do that is to update the test code and comment out the `DROP APPLICATION` statement. Using a text editor or an IDE, open `test/testsuite1/teardown.sql`, and comment out the `DROP APPLICATION` statement so that the application remains in the account.
```sql
-- DROP APPLICATION IF EXISTS {{application_package_name}}_Client;
```

Now, you deploy and test your updated HelloWorld App by running the following command:
```
% pochi deploy test
```

You should see that the application package was deployed and that testsuite1 was run successfully.

To validate your Streamlit is correct, log in to Snowflake, and using Snowsight, click to **Apps** on the left nav (and not Streamlit), click into the application ``HELLOWORLD_CLIENT``, and then click on the "HELLO_SNOWFLAKE_STREAMLIT" link on the top of the page to display the Streamlit. Your Streamlit should look like this:
![HelloWorld_Streamlit](https://drive.google.com/uc?id=1VPA9qYcDvlzRkVvbx3QHRAms_y_TFU62)


# CLI Command References

## Initialize a Pochi Native App Project Directory
```
pochi init [--name=<application_package_name>][--version=<application_version_name>] 
           [--connection=<default_connection>][--distribution={INTERNAL|EXTERNAL}]
           [--force]
```
|<div style="width:350px">Options</div>|Description|
|-------|-----------|
|`--name=<application_package_name>`|Create a new directory with the specified name in the current directory, and create the project in it|
|`--version=<application_version_name>`|Set the application_version_name in config/project.toml|
|`--connection=<default_connection>`|Set the default_connection name in config/project.toml; the name should exist in a connection file for SnowCLI or SnowSQL|
|`--distribution=INTERNAL\|EXTERNAL`|Set the application package distribution property; default is INTERNAL|
|`--force`|Replace an existing project directory with default templates|

This command creates a template native app project with default directory structure in the current directory.

## Add or Update Project Configuration
```
pochi config [--name=<parameter_name> --value=<parameter_value>] 
```

Project configuration parameters are defined in config/project.toml. You can edit the file directly to add or update project configuration parameters, or you can use this command on the command-line to view, add, or modify parameter values.
* If `<parameter_name>` exists in `config/project.toml`, the value is updated directly
* If `<parameter_name>` does not exist in `config/project.toml`, the parameter is added.
* Parameter name and value are case-sensitive.
* If `--name` and `--value` are not specified, all config parameter values are displayed.

The project configuration parameters can be referenced directly in your SQL files for parameter substitution.
To use parameter substitution in your SQL files, use `{{parameter_name}}` in your SQL commands.

## Build the Application Artifacts and Generate Deployment Scripts
```
pochi build
```

This command performs the following actions:
* creates the `generated` output directory in the current directory
* creates Snowflake artifacts with the application code/resource files in the `generated/app` directory
* creates SQL deployment scripts in the `generated/deployment` directory to run preinstall SQLs, create an application package and its objects, upload the application code/resource files, create a version or patch, and run postinstall SQLs

Note: This target is automatically run when you run `pochi deploy`. You can use `pochi build` to examine the generated output files without automatically deploying them to the target Snowflake account.

You can use this target along with `clean`, `deploy`, and `test`. When multiple targets are specified, Pochi always runs the targets in the following order: `clean`, `build`, `deploy`, and `test`.

## Deploy the Application Package to Snowflake
```
pochi deploy [--application-logic|--application-package]
```
|<div style="width:350px">Options</div>                   |Description                                     |
|-------------------------- |----------------------------------------------- |
| `--application-logic`     |If specified, deploy only uploads the application code/resource files to create a version or patch, and executes the postinstall SQL file (if applicable).|
| `--application-package`   |If specified, deploy only executes the preinstall SQL file (if applicable) and creates an application package and its objects.|

This command automatically runs the build target to generate the application artifacts and the SQL deployment scripts, and then it connects to the target Snowflake account to perform the following actions:
* Executes `generated/deployment/deploy_preinstall_objects.sql`,
* Executes `generated/deployment/deploy_application_package.sql`,
* Executes `generated/deployment/deploy_versioned_code.sql`,
* Executes `generated/deployment/deploy_postinstall_objects.sql`

You can use this target along with `clean`, `build`, and `test`. When multiple targets are specified, Pochi always runs the targets in the following order: `clean`, `build`, `deploy`, and `test`.


## Run Test Suites on Snowflake
```
pochi test [--tests=<testsuite>[.<testname>][,...]]
```
| <div style="width:350px">Options</div>|Description|
|----------------- |-----------|
| `--tests=<testsuite>[.<testname>][,...]`     |If specified, only the test suites and/or test names in a test suite are run. By default, all test suites are run.|


This command creates and runs the test suites defined in the `test` directory against the target Snowflake account. By default, a sample test suite `testsuite1` is included in the project. It is a basic test suite with a `setup.sql`, `test01.sql`, and `teardown.sql`. When the test suite is run, the order of SQL execution is:
1. the `setup.sql`,
2. all of the test scripts in alphanumeric order, and
3. then the `teardown.sql`.

The default test verifies that an `APPLICATION` object can be created from an `APPLICATION PACKAGE` successfully. It does not validate functionality or correctness.

* setup.sql and teardown.sql are optional
* You can add add more tests in a test suite by creating SQL files with a prefix of "`test`"
* You can create more test suites by adding directories in the `test` directory

You can use this target along with `clean`, `build`, and `deploy`. When multiple targets are specified, Pochi always runs the targets in the following order: `clean`, `build`, `deploy`, and `test`.

## Clean the Project
```
pochi clean
```

This command drops the application package in the target Snowflake account and deletes the `generated` output directory in the current directory.

You can use this target along with `build`, `deploy`, and `test`. When multiple targets are specified, Pochi always runs the targets in the following order: `clean`, `build`, `deploy`, and `test`.

