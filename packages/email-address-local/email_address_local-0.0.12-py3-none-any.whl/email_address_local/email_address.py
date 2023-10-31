from circles_local_database_python.generic_crud import GenericCRUD
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from language_local import lang_code
from dotenv import load_dotenv
load_dotenv()
EMAIL_ADDRESS_LOCAL_PYTHON_COMPONENT_ID = 174
EMAIL_ADDRESS_LOCAL_PYTHON_COMPONENT_NAME = 'email address local'
DEVELOPER_EMAIL = "idan.a@circ.zone"
EMAIL_ADDRESS_SCHEMA_NAME = "email_address"
EMAIL_ADRESS_ML_TABLE_NAME = "email_ml_table"
EMAIL_ADDRESS_TABLE_NAME = "email_address_table"
EMAIL_ADDRESS_VIEW = "email_address_view"
EMAIL_ADDRESS_ID_COLLUMN_NAME = "email_address_id"
EMAIL_COLLUMN_NAME = "email"
object1 = {
    'component_id': EMAIL_ADDRESS_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': EMAIL_ADDRESS_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': "idan.a@circ.zone"
}
logger = Logger.create_logger(object=object1)


class EmailAddress(GenericCRUD):

    def __init__(self) -> None:
        super().__init__(schema_name=EMAIL_ADDRESS_SCHEMA_NAME,
                         default_table_name=EMAIL_ADDRESS_TABLE_NAME, default_id_column_name=EMAIL_ADDRESS_ID_COLLUMN_NAME)

    def insert_email_adress(self, email_address: str, lang_code: lang_code.LangCode, name: str) -> int or None:
        logger.start(object={"email_address": email_address,
                     "lang_code": lang_code.value, "name": name})
        data = {
            EMAIL_COLLUMN_NAME: f'{email_address}',
        }
        email_address_id = self.insert(json_data=data)
        email_json_data = {
            "email_id": email_address_id,
            # TODO Make sure we have those two in lang_code https://www.digitalocean.com/community/tutorials/python-str-repr-functions
            "lang_code": f'{lang_code.value}',
            "name": f'{name}'
        }
        self.insert(
            table_name=EMAIL_ADRESS_ML_TABLE_NAME, json_data=email_json_data)
        logger.end(object={'email_address_id': email_address_id})
        return email_address_id

    def update_email_adress(self, email_address_id: int, new_email: str) -> None:
        logger.start(
            object={"email_address_id": email_address_id, "new_email": new_email})
        email_json_data = {"email": new_email}
        self.update_by_id(
            json_data=email_json_data, id_column_name="email_address_id", id_column_value=email_address_id)
        logger.end(object={})

    def delete(self, email_address_id: int) -> None:
        logger.start(object={"email_id": email_address_id})
        self.delete_by_id(
            id_column_name=EMAIL_ADDRESS_ID_COLLUMN_NAME, id_column_value=email_address_id)
        logger.end(object={})

    def get_email_address_by_email_address_id(self, email_address_id: int) -> str or None:
        logger.start(object={"email_address_id":  email_address_id})
        email_address = None
        result = self.select_multi_tuple_by_id(view_table_name=EMAIL_ADDRESS_VIEW, select_clause_value=EMAIL_COLLUMN_NAME,
                                               id_column_value=email_address_id)
        if result:
            email_address = result[0][0]
        logger.end(object={'email_address': email_address})
        return email_address

    def get_email_address_id_by_email_address(self, email: str) -> int or None:
        email_address_id = None
        logger.start(object={"email": email})
        result = self.select_multi_tuple_by_where(
            view_table_name=EMAIL_ADDRESS_VIEW, where=f"{EMAIL_COLLUMN_NAME}='{email}'")
        if result:
            email_address_id = result[0][0]
        logger.end(object={'email_address_id': email_address_id})
        return email_address_id
