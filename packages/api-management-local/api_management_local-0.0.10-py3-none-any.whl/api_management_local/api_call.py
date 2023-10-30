from dotenv import load_dotenv
import json
from typing import Dict
import ast
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from circles_local_database_python.generic_crud import GenericCRUD
from src.api_limit import (
    DEVELOPER_EMAIL,
    API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
    API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME,
    APILimit,
)

object1 = {
    "component_id": API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
    "component_name": API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME,
    "component_category": LoggerComponentEnum.ComponentCategory.Code.value,
    "developer_email": DEVELOPER_EMAIL,
}
load_dotenv()

logger = Logger.create_logger(object=object1)


class APICall(GenericCRUD):
    def __init__(self) -> None:
        super().__init__("api_call")

    def _insert_data_into_table(self, data: tuple) -> None:
        data_dict = {
            'api_type_id': data[0],
            'endpoint': data[1],
            'outgoing_header': data[2],
            'outgoing_body': data[3],
             'outgoing_body_significant_fields_hash': data[4],
            'incoming_message': data[5],
            'http_status_code': data[6],
            'response_body': data[7],
        }
        logger.start(object={"data_dict": data_dict})
        try:
            json_data_str = json.dumps(data_dict)
            myJson = json.loads(json_data_str)
            APICall1 = GenericCRUD(schema_name="api_call")
            APICall1.insert(table_name="api_call_table", json_data=myJson)
            logger.end()
        except Exception as exception:
            logger.exception(object=exception)
            logger.end()
            raise
