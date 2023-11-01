from typing import Any

from dotenv import load_dotenv
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum

from .connector import Connector
from .utils import validate_none_select_table_name, validate_select_table_name

load_dotenv()

# Constants
DATABASE_WITHOUT_ORM_PYTHON_GENERIC_CRUD_COMPONENT_ID = 206
DATABASE_WITHOUT_ORM_PYTHON_GENERIC_CRUD_COMPONENT_NAME = 'circles_local_database_python\\generic_crud'
DEVELOPER_EMAIL = 'akiva.s@circ.zone'

# Logger setup
logger = Logger.create_logger(object={
    'component_id': DATABASE_WITHOUT_ORM_PYTHON_GENERIC_CRUD_COMPONENT_ID,
    'component_name': DATABASE_WITHOUT_ORM_PYTHON_GENERIC_CRUD_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
})


class GenericCRUD:
    """A class that provides generic CRUD functionality"""

    def __init__(self, schema_name: str, default_table_name: str = None, default_id_column_name: str = None,
                 connection: Connector = None) -> None:
        """Initializes the GenericCRUD class. If connection is not provided, a new connection will be created."""
        logger.start(object={"schema_name": schema_name, "default_table_name": default_table_name,
                             "id_column_name": default_id_column_name})
        self.schema_name = schema_name
        self.connection = connection or Connector.connect(schema_name=schema_name)
        self.cursor = self.connection.cursor()
        self.default_column = default_id_column_name
        self.default_table_name = default_table_name
        logger.end()

    def insert(self, table_name: str = None, json_data: dict = None) -> int:
        """Inserts a new row into the table and returns the id of the new row or -1 if an error occurred."""
        logger.start(object={"table_name": table_name, "json_data": str(json_data)})
        table_name = table_name or self.default_table_name
        self._validate_json_data(json_data)
        self._validate_table_name(table_name)

        try:
            validate_none_select_table_name(table_name)
            columns = ','.join(json_data.keys())
            values = ','.join(['%s' for _ in json_data])
            insert_query = f"INSERT INTO {self.schema_name}.{table_name} ({columns}) " \
                           f"VALUES ({values})"
            self.cursor.execute(insert_query, tuple(json_data.values()))
            self.connection.commit()
            logger.end("Data inserted successfully.")
            return self.cursor.lastrowid()
        except Exception as e:
            logger.exception("Error inserting json_data", object=e)
            logger.end()
            raise

    # Old name: update
    def update_by_id(self, table_name: str = None, id_column_name: str = None, id_column_value: Any = None,
                     json_data: dict = None, limit: int = 100, order_by: str = "") -> None:
        """Updates data in the table by ID."""
        logger.start(object={"table_name": table_name, "json_data": str(json_data), "id_column_name": id_column_name,
                             "id_column_value": id_column_value, "order_by": order_by})
        table_name = table_name or self.default_table_name
        id_column_name = id_column_name or self.default_column
        self._validate_json_data(json_data)
        self._validate_table_name(table_name)

        if id_column_name:  # id_column_value can be empty
            where = f"{id_column_name}=%s"
            extra_sql_params = (id_column_value, )
            self.update_by_where(table_name=table_name, where=where, json_data=json_data,
                                 extra_sql_params=extra_sql_params, limit=limit, order_by=order_by)
        else:
            message = "Update by id requires an id_column_name"
            logger.error(message)
            logger.end()
            raise Exception(message)

    # Old name: update
    def update_by_where(self, table_name: str = None, where: str = None, json_data: dict = None,
                        extra_sql_params: tuple = None, limit: int = 100, order_by: str = "") -> None:
        """Updates data in the table by WHERE."""
        logger.start(object={"table_name": table_name, "json_data": str(json_data), "where": where,
                             "params": str(extra_sql_params), "limit": limit})
        table_name = table_name or self.default_table_name
        self._validate_json_data(json_data)
        self._validate_table_name(table_name)
        try:
            validate_none_select_table_name(table_name)
            set_values = ', '.join(f"{k}=%s" for k in json_data.keys()) + ("," if json_data else "")
            if not where:
                message = "update_by_where requires a 'where'"
                logger.error(message)
                logger.end()
                raise Exception(message)

            update_query = f"UPDATE {self.schema_name}.{table_name} " \
                           f"SET {set_values} updated_timestamp=CURRENT_TIMESTAMP() " \
                           f"WHERE {where} " + \
                           (f"ORDER BY {order_by} " if order_by else "") + \
                           f"LIMIT {limit} "

            extra_sql_params = extra_sql_params or tuple()
            self.cursor.execute(update_query, tuple(json_data.values()) + extra_sql_params)
            self.connection.commit()
            logger.end("Data updated successfully.")
        except Exception as e:
            logger.exception("Error updating json_data", object=e)
            logger.end()
            raise

    def delete_by_id(self, table_name: str = None, id_column_name: str = None, id_column_value: Any = None) -> None:
        """Deletes data from the table by id"""
        # logger, checks etc. are done inside delete_by_where
        id_column_name = id_column_name or self.default_column
        if id_column_name:  # id_column_value can be empty
            where = f"{id_column_name}=%s"
            params = (id_column_value, )
            self.delete_by_where(table_name, where, params)
        else:
            message = "Delete by id requires an id_column_name and id_column_value."
            logger.error(message)
            logger.end()
            raise Exception(message)

    def delete_by_where(self, table_name: str = None, where: str = None, params: tuple = None) -> None:
        """Deletes data from the table by WHERE."""
        logger.start(object={"table_name": table_name, "where": where, "params": str(params)})
        table_name = table_name or self.default_table_name
        self._validate_table_name(table_name)
        if not where:
            message = "delete_by_where requires a 'where'"
            logger.error(message)
            logger.end()
            raise Exception(message)

        try:
            update_query = f"UPDATE {self.schema_name}.{table_name} " \
                           f"SET end_timestamp=CURRENT_TIMESTAMP() " \
                           f"WHERE {where}"
            self.cursor.execute(update_query, params)
            self.connection.commit()
            logger.end("Deleted successfully.")

        except Exception as e:
            logger.exception("Error while deleting", object=e)
            logger.end()
            raise

    # Old name: select_one_by_id
    def select_one_tuple_by_id(self, view_table_name: str, select_clause_value: str = "*",
                               id_column_name: str = None, id_column_value: Any = None, order_by: str = "") -> tuple:
        """Selects one row from the table by ID and returns it as a tuple."""
        result = self.select_multi_tuple_by_id(view_table_name, select_clause_value, id_column_name, id_column_value,
                                               limit=1, order_by=order_by)
        if result:
            return result[0]
        else:
            return tuple()

    def select_one_dict_by_id(self, view_table_name: str, select_clause_value: str = "*",
                              id_column_name: str = None, id_column_value: Any = None, order_by: str = "") -> dict:
        """Selects one row from the table by ID and returns it as a dictionary (column_name: value)"""
        result = self.select_one_tuple_by_id(view_table_name, select_clause_value, id_column_name, id_column_value,
                                             order_by=order_by)
        return self._get_headers(result, select_clause_value)

    # Old name: select_one_by_where
    def select_one_tuple_by_where(self, view_table_name: str, select_clause_value: str = "*",
                                  where: str = None, params: tuple = None, order_by: str = "") -> tuple:
        """Selects one row from the table based on a WHERE clause and returns it as a tuple."""
        result = self.select_multi_tuple_by_where(view_table_name, select_clause_value, where=where, params=params,
                                                  limit=1, order_by=order_by)
        if result:
            return result[0]
        else:
            return tuple()

    def select_one_dict_by_where(self, view_table_name: str, select_clause_value: str = "*",
                                 where: str = None, params: tuple = None, order_by: str = "") -> dict:
        """Selects one row from the table based on a WHERE clause and returns it as a dictionary."""
        result = self.select_one_tuple_by_where(view_table_name, select_clause_value, where=where, params=params,
                                                order_by=order_by)
        return self._get_headers(result, select_clause_value)

    # Old name: select_multi_by_id
    def select_multi_tuple_by_id(self, view_table_name: str, select_clause_value: str = "*",
                                 id_column_name: str = None, id_column_value: Any = None,
                                 limit: int = 100, order_by: str = "") -> list:
        """Selects multiple rows from the table by ID and returns them as a list of tuples.
        send `id_column_name=''` if you want to select all rows and ignore default column"""
        if id_column_name is None:
            id_column_name = self.default_column

        if not id_column_name or id_column_value is None:
            where = None
            params = None
        else:
            where = f"{id_column_name}=%s"
            params = (id_column_value, )
        return self.select_multi_tuple_by_where(view_table_name, select_clause_value, where=where, params=params,
                                                limit=limit, order_by=order_by)

    def select_multi_dict_by_id(
            self, view_table_name: str, select_clause_value: str = "*", id_column_name: str = None,
            id_column_value: Any = None, limit: int = 100, order_by: str = "") -> list:
        """Selects multiple rows from the table by ID and returns them as a list of dictionaries."""
        result = self.select_multi_tuple_by_id(view_table_name, select_clause_value, id_column_name, id_column_value,
                                               limit=limit, order_by=order_by)
        return [self._get_headers(row, select_clause_value) for row in result]

    # Old name: select_multi_by_where
    def select_multi_tuple_by_where(self, view_table_name: str, select_clause_value: str = "*",
                                    where: str = None, params: tuple = None, limit: int = 100, order_by: str = "") -> list:
        """Selects multiple rows from the table based on a WHERE clause and returns them as a list of tuples."""
        logger.start(object={"view_table_name": view_table_name, "select_clause_value": select_clause_value,
                             "where": where, "params": str(params), "limit": limit, "order_by": order_by})
        view_table_name = view_table_name or self.default_table_name
        self._validate_table_name(view_table_name)
        try:
            validate_select_table_name(view_table_name)
            select_query = f"SELECT {select_clause_value} " \
                           f"FROM {self.schema_name}.{view_table_name} " + \
                           (f"WHERE {where} " if where else "") + \
                           (f"ORDER BY {order_by} " if order_by else "") + \
                           f"LIMIT {limit}"
            self.cursor.execute(select_query, params)
            result = self.cursor.fetchall()
            logger.end("Data selected successfully.", object={"result": str(result)})
            return result
        except Exception as e:
            logger.exception("Error selecting json_data", object=e)
            logger.end()
            raise

    def select_multi_dict_by_where(
            self, view_table_name: str, select_clause_value: str = "*", where: str = None, params: tuple = None,
            limit: int = 100, order_by: str = "") -> list:
        """Selects multiple rows from the table based on a WHERE clause and returns them as a list of dictionaries."""
        result = self.select_multi_tuple_by_where(view_table_name, select_clause_value, where=where, params=params,
                                                  limit=limit, order_by=order_by)
        return [self._get_headers(row, select_clause_value) for row in result]

    # helper functions:

    def switch_db(self, new_database: str) -> None:
        """Switches the database to the given database name."""
        logger.start(object={"schema_name": new_database})
        self.connection.set_schema(new_database)
        self.schema_name = new_database
        logger.end("Schema set successfully.")

    def _get_headers(self, row: tuple, select_clause_value: str) -> dict:
        """Returns a dictionary of the column names and their values."""
        if select_clause_value == "*":
            column_names = [col[0] for col in self.cursor.description()]
        else:
            column_names = [x.strip() for x in select_clause_value.split(",")]
        return dict(zip(column_names, row or tuple()))

    @staticmethod
    def _validate_table_name(table_name: str) -> None:
        """Validates the table name."""
        if not table_name:
            message = "Table name is required."
            logger.error(message)
            logger.end()
            raise Exception(message)

    @staticmethod
    def _validate_json_data(json_data: dict) -> None:
        """Validates the json data."""
        if not json_data:
            message = "Json data is required."
            logger.error(message)
            logger.end()
            raise Exception(message)

    def set_schema(self, schema_name: str):
        """Sets the schema to the default schema."""
        logger.start()
        self.connection.set_schema(schema_name)
        self.schema_name = schema_name
        logger.end()

    def close(self) -> None:
        """Closes the connection to the database."""
        logger.start()
        self.connection.close()
        logger.end()
