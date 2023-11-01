from collections.abc import Iterable
import json
import os
from enum import Enum

import mysql.connector

from circles_local_database_python.connector import Connector
from circles_local_database_python.generic_crud import GenericCRUD
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from .our_queue import OurQueue

QUEUE_LOCAL_PYTHON_COMPONENT_ID = 155
QUEUE_LOCAL_PYTHON_COMPONENT_NAME = "queue_local/src/database_queue.py"
DEVELOPER_EMAIL = 'akiva.s@circ.zone'


class StatusEnum(Enum):
    NEW = 0
    RETRIEVED = 1


class DatabaseQueue(OurQueue, GenericCRUD):
    def __init__(self, schema_name: str = None, table_name: str = "queue_item_table", view_name: str = None,
                 id_column_name: str = "queue_item_id", connection: Connector = None) -> None:
        """Initialize the queue.
        Default schema_name = the first part of the table_name, before the first underscore.
        Default view_name = table_name with "_view" instead of "_table"
        You can pass a Connector object to use an existing connection, or None to create a new connection.
        """
        self.logger = Logger(
            object={
                'component_id': QUEUE_LOCAL_PYTHON_COMPONENT_ID,
                'component_name': QUEUE_LOCAL_PYTHON_COMPONENT_NAME,
                'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
                'developer_email': DEVELOPER_EMAIL
            }
        )
        if not view_name:
            view_name = table_name.replace("_table", "_view")
        if not schema_name:
            schema_name = table_name.split("_")[0]
        self.table_name = table_name
        self.view_name = view_name
        self.id_column_name = id_column_name

        GenericCRUD.__init__(self, schema_name=schema_name, connection=connection)
        self.logger.info("DatabaseQueue initialized successfully", object={
            "schema_name": schema_name, "table_name": table_name, "view_name": view_name, "id_column_name": id_column_name})

    def push(self, json_data: dict) -> None:
        """Pushes a new entry to the queue.
        json_data consists of columns and values to insert into the queue table."""
        created_user_id = 0  # TODO
        self.logger.start("Pushing entry to the queue database", object={"json_data": json_data})

        try:
            self._fix_parameters_json(json_data)

            json_data["status_id"] = StatusEnum.NEW.value
            json_data["created_user_id"] = created_user_id

            self.insert(table_name=self.table_name, json_data=json_data)
            self.logger.end("Entry pushed to the queue database successfully")
        except Exception as e:
            self.logger.exception("Error while pushing entry to the queue database", object=e)
            raise

    def get(self, action_ids: tuple = ()) -> dict:
        """
        Returns the first item from the queue (possibly considering specific actions) and marks it as taken.

        :param action_ids: Tuple of action IDs to consider (optional).
        :return: Dictionary representing the retrieved queue item.
        """
        updated_user_id = 0  # TODO
        self.logger.start("Getting and updating queue item from the queue database", object={"action_ids": action_ids})
        action_ids = self._fix_action_ids(action_ids)

        try:
            json_data = {"process_id": os.getpid()}
            update_where = f"process_id IS NULL AND status_id = {StatusEnum.NEW.value}" + \
                           (f" AND action_id IN {action_ids}" if action_ids else "")
            self.update_by_where(table_name=self.table_name, where=update_where, order_by="created_timestamp",
                                 limit=1, json_data=json_data)

            select_where = f"process_id = {os.getpid()} AND status_id = {StatusEnum.NEW.value}"
            queue_item = self.select_one_dict_by_where(self.view_name, where=select_where)
            if queue_item:
                # Update the selected queue item
                json_data = {"status_id": StatusEnum.RETRIEVED.value, "updated_user_id": updated_user_id}
                self.update_by_id(table_name=self.table_name, id_column_name=self.id_column_name,
                                  id_column_value=queue_item[self.id_column_name], json_data=json_data)
                self.logger.end("Entry retrieved and updated from the queue database successfully",
                                object={k: str(v) for k, v in queue_item.items()})  # contains a datetime object
            else:
                self.logger.end("The queue is empty")
        except mysql.connector.Error as e:
            self.connection.rollback()
            self.logger.exception("Error while getting and updating queue item from the queue database", object=e)
            raise
        return queue_item

    def peek(self) -> dict:
        """Get the first item in the queue without changing it"""
        try:
            self.logger.start("Peeking queue item from the queue database")
            queue_item = self.select_one_dict_by_id(self.view_name, id_column_name="status_id",
                                                    id_column_value=StatusEnum.NEW.value, order_by="created_timestamp")
            self.logger.end("Entry peeked from the queue database successfully" if queue_item else "The queue is empty")
        except Exception as e:
            self.logger.exception("Error while peeking queue item from the queue database", object=e)
            raise
        return queue_item

    def _fix_action_ids(self, action_ids):
        """Fixes the action_ids argument to fit the SQL syntax (action_id IN action_ids)"""
        if isinstance(action_ids, int):
            action_ids = (action_ids,)
        elif isinstance(action_ids, Iterable):
            action_ids = tuple(action_ids)
        else:
            self.logger.error("get_by_action_ids (queue database) invalid argument", object=action_ids)
            raise ValueError("`action_ids` must be a tuple")
        return action_ids if len(action_ids) != 1 else f"({action_ids[0]})"

    @staticmethod
    def _fix_parameters_json(json_data: dict):
        """Fixes the parameters_json argument to fit the SQL syntax (parameters_json must be a string)"""
        for key, value in json_data.items():
            if "parameters_json" in key:
                if isinstance(value, str):
                    json_data[key] = value.replace("'", '"')
                else:
                    json_data[key] = json.dumps(value)
