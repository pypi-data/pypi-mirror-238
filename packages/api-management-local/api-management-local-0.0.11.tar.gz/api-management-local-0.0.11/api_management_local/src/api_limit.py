from dotenv import load_dotenv
import json
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from circles_local_database_python.generic_crud import GenericCRUD

API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID = 212  
API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME = "api-management-local-python-package"
DEVELOPER_EMAIL = "heba.a@circ.zone"

object1 = {
    'component_id': API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
load_dotenv()

logger=Logger.create_logger(object=object1)
class APILimit( GenericCRUD):
    def __init__(self) -> None:
         super().__init__("api_limit")
    
    
    def get_limits_by_api_type_id(self,api_type_id:str)->list:
        logger.start(object={'api_type_id':api_type_id})
        try:
           select_clause="soft_limit,hard_limit"
           api_str="api_type_id="+api_type_id
           list=self.select_multi_by_where(view_table_name="api_limit_view",select_clause_value=select_clause,where=api_str)
           logger.end(object={'list':str(list)})
           return list 
        except Exception as exception:
            logger.exception(object=exception)
            logger.end()
            raise
            
