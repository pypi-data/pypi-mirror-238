from dotenv import load_dotenv
import json
import os
from circles_local_database_python.connector import Connector
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from circles_local_database_python.connector import Connector
from circles_local_database_python.generic_crud import GenericCRUD
from src.api_call import APICall
from url_local.url_circlez import UrlCirclez
from url_local import action_name_enum, entity_name_enum, component_name_enum
from user_context_remote.user_context import UserContext
from src.api_limit import (DEVELOPER_EMAIL,
                               API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
                               API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME,APILimit)
import requests

BRAND_NAME = os.getenv('BRAND_NAME')
ENVIORNMENT_NAME = os.getenv('ENVIRONMENT_NAME')
AUTHENTICATION_API_VERSION = 1

url_circlez = UrlCirclez()
authentication_login_validate_jwt_url = url_circlez.endpoint_url(
            brand_name=BRAND_NAME,
            environment_name=ENVIORNMENT_NAME,
            component_name=component_name_enum.ComponentName.AUTHENTICATION.value,
            entity_name=entity_name_enum.EntityName.AUTH_LOGIN.value,
            version=AUTHENTICATION_API_VERSION,
            action_name=action_name_enum.ActionName.VALIDATE_JWT.value
        )
object1 = {
    'component_id': API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
load_dotenv()

logger=Logger.create_logger(object=object1)
class APIManagementLocal( GenericCRUD):
    def __init__(self) -> None:
        pass
        
    def get_actual_by_api_type_id_succ( api_type_id:int, hours: int) -> int:
        logger.start(object={'api_type_id':str(api_type_id),'hours':str(hours)})
        connection = Connector.connect("api_call")
        cursor = connection.cursor()
        try:
            cursor.execute("""
                  SELECT COUNT(*)
                  FROM api_call_view
                  WHERE api_type_id = %s
                  AND TIMESTAMPDIFF(HOUR, created_timestamp, NOW()) <= %s
                  AND http_status_code = 200 """.format(api_type_id, hours))
            count_result = cursor.fetchone()[0]
            logger.end(object={'count_result':count_result})
            return count_result
        except Exception as exception:
            logger.exception(object=exception)
            logger.end()
            raise
    
    @staticmethod
    def  _get_json_with_only_sagnificant_fields_by_api_type_id( json1:json, api_type_id:int)-> json:
        logger.start(object={'json1':str(json1),'api_type_id':str(api_type_id)})
        connection = Connector.connect("api_type")
        try:
            cursor = connection.cursor()
            query = f"SELECT field_name FROM api_type.api_type_field_view WHERE api_type_id = %s"
            cursor.execute(query, (api_type_id,))
            significant_fields = [row[0] for row in cursor.fetchall()]
            data = json.loads(json1)
            filtered_data = {key: data[key] for key in significant_fields if key in data}
            filtered_json = json.dumps(filtered_data)
            logger.end(object={'filtered_json':str(filtered_json)})
            return filtered_json
        except Exception as exception:
            logger.exception(object=exception)
            logger.end()
            raise
        
    @staticmethod
    def try_to_call_api(api_type_id:int, endpoint:str,outgoing_body:str,outgoing_header:str,hour:int)->str:
        logger.start(object={'api_type_id':str(api_type_id),'endpoint':str(endpoint),'outgoing_body':str(outgoing_body),'outgoing_header':str(outgoing_header)})
        api_succ=APIManagementLocal.get_actual_by_api_type_id_succ(api_type_id,hour)
        connection = Connector.connect("api_call")
        cursor = connection.cursor()
        try:
                query=f"SELECT http_status_code, response_body FROM api_call.api_call_table WHERE api_type_id= %s"
                cursor.execute(query, (api_type_id,))
                arr =cursor.fetchone()
                if arr[0]==200:
                    return arr[1]
                api_limit=APILimit()
                api_type_id1=str(api_type_id)
                limits=api_limit.get_limits_by_api_type_id(api_type_id=api_type_id1)
                if api_succ <limits[0][0]:
                      user=UserContext.login()
                      data = {"jwtToken":f"Bearer ${user.get_user_JWT()} "}
                      outgoing_body_significant_fields_hash = APIManagementLocal._get_json_with_only_sagnificant_fields_by_api_type_id(json1=json.dumps(data), api_type_id=api_type_id1)
                      output = requests.post(url=endpoint, data=json.dumps(outgoing_body, separators=(",", ":")), headers=outgoing_header)
                      status=output.status_code
                      incoming_message = output.content.decode('utf-8')
                      responsebody=output.json()
                      res=json.dumps(responsebody)
                      outgoing_body_significant_fields_hash1 = json.dumps(outgoing_body_significant_fields_hash)
                      data1 = (api_type_id,endpoint, outgoing_header, outgoing_body,outgoing_body_significant_fields_hash1,incoming_message,status,res )
                      APICall1=APICall()
                      APICall1._insert_data_into_table(data1)
                      logger.end()
                      return responsebody                         
                elif limits[0]<=api_succ and limits[1]>api_succ:
                      user=UserContext.login()
                      output = requests.post(url=authentication_login_validate_jwt_url, data=json.dumps(data, separators=(",", ":")), headers=outgoing_header)
                      logger.warn("you passed the soft limit")
                      logger.end()
                else:
                    logger.error("you passed the hard limit")
                    logger.end()

                  
        except Exception as exception:
            logger.exception(object=exception)
            logger.end()
            raise
