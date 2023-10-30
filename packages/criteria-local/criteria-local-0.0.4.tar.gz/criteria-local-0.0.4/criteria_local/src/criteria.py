from circles_local_database_python.generic_crud import GenericCRUD
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.Logger import Logger

CRITERIA_LOCAL_PYTHON_COMPONENT_ID = 210
CRITERIA_LOCAL_PYTHON_COMPONENT_NAME = 'criteria-local-python'
DEVELOPER_EMAIL = 'jenya.b@circ.zone'

object_init = {
    'component_id': CRITERIA_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': CRITERIA_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    "developer_email": DEVELOPER_EMAIL
}
logger = Logger.create_logger(object=object_init)

class Criterion:
    def __init__(self, entity_type_id: int = None, group_list_id: int = None, gender_list_id: int = None, location_id: int = None) -> None:
        self.entity_type_id = entity_type_id
        self.group_list_id = group_list_id
        self.gender_list_id = gender_list_id
        self.location_id = location_id

class CriteriaLocal(GenericCRUD):
    #TODO: add in another branch methods i.e. match( profile_id ) -> bool
    #TODO: add in another branch distance( position ) -> float
    #TODO: add another methods

    def __init__(self) -> None:
        super().__init__(schema_name = "criteria")

    def insert(self, criterion: Criterion) -> None:
        logger.start("Insert criteria", object={
            "entity_type_id": criterion.entity_type_id,
            "group_list_id": criterion.group_list_id,
            "gender_list_id": criterion.gender_list_id,
            "location_id": criterion.location_id
        })
        criteria_json = {
            "entity_type_id": criterion.entity_type_id,
            "group_list_id": criterion.group_list_id,
            "gender_list_id": criterion.gender_list_id,
            "location_id": criterion.location_id
        }
        self.insert(table_name="criteria_table",json_data=criteria_json)
        logger.end()

    def update_min_age(self,criteria_id: int, min_age: float, kids: bool) -> None:
        logger.start("Update minimun ages", object={"criteria_id": criteria_id, "min_age": min_age})
        if kids == True:
            kids_age_json = {
                "min_kids_age": min_age,
            }
            self.update_by_id(table_name="criteria_table", id_column_name="criteria_id", id_column_value=criteria_id, json_data=kids_age_json)
            logger.end("Minimum kids ages update")
        else:
            age_json = {
                "min_age": min_age,
            }
            self.update_by_id(table_name="criteria_table", id_column_name="criteria_id", id_column_value=criteria_id, json_data=age_json)
            logger.end("Minimum ages update")

    def update_max_age(self, criteria_id: int, max_age: float, kids: bool) -> None:
        logger.start("Update maximum ages", object={"criteria_id": criteria_id, "max_age": max_age})
        if kids == True:
            kids_age_json = {
                "max_kids_age": max_age
            }
            self.update_by_id(table_name="criteria_table", id_column_name="criteria_id", id_column_value=criteria_id, json_data=kids_age_json)
            logger.end("Maximum kids ages update")
        else:
            age_json = {
                "max_age": max_age
            }
            self.update_by_id(table_name="criteria_table", id_column_name="criteria_id", id_column_value=criteria_id, json_data=age_json)
            logger.end("Maximum ages update")

    def update_min_number_of_kids(self, criteria_id: int, min_number_of_kids: int) -> None:
        logger.start("Update minimum number of kids", object={"criteria_id": criteria_id, "min_number_of_kids":min_number_of_kids})
        number_of_kids_json = {
            "min_number_of_kids": min_number_of_kids,
            }
        self.update_by_id(table_name="criteria_table", id_column_name="criteria_id", id_column_value=criteria_id, json_data=number_of_kids_json)
        logger.end()

    def update_max_age_number_of_kids(self, criteria_id: int, max_number_of_kids: int) -> None:
        logger.start("Update minimum number of kids", object={"criteria_id": criteria_id, "max_number_of_kids": max_number_of_kids})
        number_of_kids_json = {
            "max_number_of_kids": max_number_of_kids,
            }
        self.update_by_id(table_name="criteria_table", id_column_name="criteria_id", id_column_value=criteria_id, json_data=number_of_kids_json)
        logger.end()
    
    def update_min_max_height(self, criteria_id: int, min_height: int, max_height: int) -> None:
        logger.start("Update minimum and maximum height", object={"criteria_id": criteria_id, "min_height": min_height, "max_height": max_height})
        number_of_kids_json = {
            "min_height": min_height,
            "max_height": max_height
            }
        self.update_by_id(table_name="criteria_table", id_column_name="criteria_id", id_column_value=criteria_id, json_data=number_of_kids_json)
        logger.end()
        
    def update_partner_experience_level(self, criteria_id: int, partner_experience_level: int) -> None:
        logger.start("Update partner experience level", object={"criteria_id": criteria_id, "partner_experience_level": partner_experience_level})
        experience_level_json = {
            "partner_experience_level": partner_experience_level
            }
        self.update_by_id(table_name="criteria_table", id_column_name="criteria_id", id_column_value=criteria_id, json_data=experience_level_json)
        logger.end()

    def update_number_of_partners(self, criteria_id: int, number_of_partners: int) -> None:
        logger.start("Update number of partners", object={"criteria_id": criteria_id, "number_of_partners": number_of_partners})
        number_of_partners_json = {
            "number_of_partners": number_of_partners
            }
        self.update_by_id(table_name="criteria_table", id_column_name="criteria_id", id_column_value=criteria_id, json_data=number_of_partners_json)
        logger.end()

    def delete(self, criteria_id: int) -> None:
        logger.start("Delete criteria", object={"criteria_id": criteria_id})
        self.delete_by_id(table_name="criteria_table",id_column_name="criteria_id",id_column_value=criteria_id)
        logger.end(f"Criteria deleted criteria_id= {criteria_id}", object={'criteria_id': criteria_id})
