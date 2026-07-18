import logging

import mysql.connector
import os
from dotenv import load_dotenv
from service.template_queries import SQL_TEMPLATES

load_dotenv()


class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

        try:
            db_port = int(str(os.getenv("DB_PORT", "3306")).strip())
            db_host = str(os.getenv("DB_HOST")).strip()
            db_user = str(os.getenv("DB_USER")).strip()
            db_pass = str(os.getenv("DB_PASSWORD")).strip()
            db_name = str(os.getenv("DB_NAME")).strip()

            self.connection = mysql.connector.connect(
                host=db_host,
                user=db_user,  # Must be the readonly_user
                password=db_pass,
                database=db_name,
                port=db_port
            )
            self.cursor = self.connection.cursor(dictionary=True)

        except mysql.connector.Error as err:
            logging.error(f"Error connecting to the database: {err}")
            self.connection = None

    def execute_template(self, template_name, limit, params):
        if not self.cursor:
            logging.error("❌ Cannot execute query: Database connection is missing.")
            return None

        query = SQL_TEMPLATES.get(template_name).get("query")

        # Add LIMIT
        if limit != 0:
            query += f" LIMIT {limit}"

        query += ";"
        logging.info(query)
        if query:
            logging.info(f"Executing Query: {query} with params: {params}")
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        return None

    def execute_dynamic_template(self, template_name, date_params, **kwargs ):

        if not self.cursor:
            logging.error("❌ Cannot execute query: Database connection is missing.")
            return None

        extra_filters = kwargs.get("extra_filters", {})
        extra_tables = kwargs.get("extra_tables", {})
        limit = kwargs.get("limit", 0)

        # Get the base query
        base_query = SQL_TEMPLATES[template_name]["query"]

        # split the query into 3 parts
        part_1, rest = base_query.split(" WHERE ")
        part_2, part_3 = rest.split(" GROUP BY ")

        dynamic_query = part_1
        final_params = date_params  # e.g., ['2026-05-10', '2026-05-14']

        # Dynamically append extra conditions
        if extra_filters:
            for column, value in extra_filters.items():
                # Append to the SQL string safely
                part_2 += f" AND {column} = %s"
                # Add the actual value to our parameters list
                final_params.append(value)


        if extra_tables:
            for t_column, t_value in extra_tables.items():
                    # Append to the SQL string
                    dynamic_query += f" {t_value}"

        # Form complete query
        dynamic_query += f" WHERE {part_2}"

        # Add GROUP BY or ORDER BY
        if "GROUP BY" in base_query:
            dynamic_query += f" GROUP BY {part_3}"

        # Add LIMIT
        if limit != 0:
            dynamic_query += f" LIMIT {limit}"

        dynamic_query += ";"
        logging.info(dynamic_query)
        logging.info(final_params)

        # Execute safely
        self.cursor.execute(dynamic_query, tuple(final_params))
        return self.cursor.fetchall()

    def execute_raw_sql(self, sql_query):
        # Strict security: Check for forbidden words before running
        if not self.cursor:
            logging.error("❌ Cannot execute query: Database connection is missing.")
            return None

        forbidden_words = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER"]
        if any(word in sql_query.upper() for word in forbidden_words):
            raise PermissionError("Write operations are strictly prohibited.")

        self.cursor.execute(sql_query)
        return self.cursor.fetchall()