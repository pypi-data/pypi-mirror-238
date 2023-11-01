import snowflake.connector
import os

from logs.manager import LoggingManager


class PochiUtil:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PochiUtil, cls).__new__(cls)
            cls._instance.init_data()
        return cls._instance

    def init_data(self):
        self.__connection = None

    def get_connection(self, options):
        has_errors = False
        try:
            if options.default_connection is None:
                LoggingManager.display_message(
                    "connection_name_issue",
                )
                has_errors = True
            else:
                if self.__connection is None:
                    if (
                        options.default_connection is not None
                        and "username" in options.default_connection
                        and "password" in options.default_connection
                        and "accountname" in options.default_connection
                    ):
                        self.__connection = snowflake.connector.connect(
                            user=options.default_connection.username,
                            password=options.default_connection.password,
                            account=options.default_connection.accountname,
                        )
                    else:
                        LoggingManager.display_message(
                            "missing_parameters_connection_issue",
                        )

                        has_errors = True
        except snowflake.connector.Error as e:
            LoggingManager.display_message(
                "connection_issues",
                [
                    options.default_connection.accountname,
                    options.project_config.default_connection,
                ],
            )
            has_errors = True
        finally:
            return has_errors

    def execute_sql(self, sql_statement, with_output=False):
        has_errors = False
        try:
            cur = self.__connection.cursor().execute(sql_statement)
            if self.__connection.get_query_status(cur.sfqid).name != "SUCCESS":
                has_errors = True
        except Exception as e:
            LoggingManager.display_message(
                "script_issues",
                [
                    sql_statement,
                    e,
                ],
            )
            has_errors = True
        finally:
            if with_output:
                return has_errors, cur.fetchall()
            return has_errors

    def execute_sql_from_file(self, file_path, has_errors=False, query_logging=False):
        try:
            if os.path.exists(file_path) and not has_errors:
                with open(file_path, "r") as sql_file:
                    for cur in self.__connection.execute_stream(
                        sql_file, remove_comments=True
                    ):
                        if query_logging:
                            col_width = 39 if len(cur.description)>1 else 121
                            LoggingManager.display_single_message(
                                    "[SQL] +-" + "+-".join('-'*col_width for col in cur.description) + "+"
                                )
                            LoggingManager.display_single_message(
                                    # "[SQL] | " + "| ".join(str(col.name)[:col_width].ljust(col_width) for col in cur.description) + "|"
                                    "[SQL] | " + "| ".join(str(col.name)[:col_width].ljust(col_width) for col in cur.description) + "|"
                                )
                            LoggingManager.display_single_message(
                                    "[SQL] +-" + "+-".join('-'*col_width for col in cur.description) + "+"
                                )
                            for ret in cur:
                                LoggingManager.display_single_message(
                                    # "[SQL] | " + "| ".join(str(col)[:col_width].ljust(col_width) for col in ret) + "|"
                                    "[SQL] | " + "| ".join(str(col).ljust(col_width) for col in ret) + "|"
                                )
                            LoggingManager.display_single_message(
                                    "[SQL] +-" + "+-".join('-'*col_width for col in cur.description) + "+"
                                )
                            LoggingManager.display_single_message(
                                    "[SQL] ")
                        if (
                            self.__connection.get_query_status(cur.sfqid).name
                            != "SUCCESS"
                        ):
                            has_errors = True
        except Exception as e:
            LoggingManager.display_message(
                "script_issues",
                [
                    file_path,
                    e,
                ],
            )
            has_errors = True
        finally:
            return has_errors
