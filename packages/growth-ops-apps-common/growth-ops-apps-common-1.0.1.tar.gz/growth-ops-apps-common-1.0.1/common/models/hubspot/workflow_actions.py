from enum import Enum
from typing import List, Optional, Any

from pydantic import BaseModel, Field


class HubSpotExecutionState(Enum):
    SUCCESS = "SUCCESS"
    FAIL_CONTINUE = "FAIL_CONTINUE"
    BLOCK = "BLOCK"
    ASYNC = "ASYNC"


class WorkflowOptionsOrigin(BaseModel):
    portal_id: int = Field(alias="portalId")
    action_definition_id: int = Field(alias="actionDefinitionId")
    action_definition_version: int = Field(alias="actionDefinitionVersion")
    action_execution_index_identifier: Optional[Any] = Field(alias="actionExecutionIndexIdentifier")
    extension_definition_id: Optional[int] = Field(alias="extensionDefinitionId")
    extension_definition_version_id: Optional[int] = Field(alias="extensionDefinitionVersionId")

    class Config:
        populate_by_name = True


class WorkflowFetchOptions(BaseModel):
    q: Optional[str]
    after: Optional[str]


class WorkflowOptionsRequest(BaseModel):
    origin: WorkflowOptionsOrigin
    input_field_name: str = Field(alias="inputFieldName")
    input_fields: dict = Field(alias="inputFields")
    fetch_options: Optional[WorkflowFetchOptions] = Field(alias="fetchOptions")
    object_type_id: Optional[str] = Field(alias="objectTypeId")
    portal_id: Optional[int] = Field(alias="portalId")
    extension_definition_id: Optional[int] = Field(alias="extensionDefinitionId")
    extension_definition_version: Optional[int] = Field(alias="extensionDefinitionVersion")

    class Config:
        populate_by_name = True


class WorkflowFieldOption(BaseModel):
    label: str
    description: str
    value: str


class WorkflowOptionsResponse(BaseModel):
    options: List[WorkflowFieldOption]
    after: Optional[str]
    searchable: Optional[bool]


class HubSpotWorkflowActionOriginModel(BaseModel):
    portal_id: Optional[int] = Field(alias="portalId")
    action_definition_id: Optional[int] = Field(alias="actionDefinitionId")
    action_definition_version: Optional[int] = Field(alias="actionDefinitionVersion")

    class Config:
        populate_by_name = True


class HubSpotWorkflowActionContextModel(BaseModel):
    source: Optional[str]
    workflow_id: Optional[int] = Field(alias="workflowId")

    class Config:
        populate_by_name = True


class HubSpotWorkflowActionObjectModel(BaseModel):
    object_id: Optional[int] = Field(alias="objectId")
    object_type: Optional[str] = Field(alias="objectType")

    class Config:
        populate_by_name = True


class MarketingEventType(Enum):
    SUCCESS = "WEBINAR"
    FAIL_CONTINUE = "CONFERENCE"
    BLOCK = "WORKSHOP"


class HubSpotWorkflowActionInputFieldsModel(BaseModel):
    # hubspot_recruiting set default job form
    form_id: Optional[str]

    # hubspot_recruiting set default application data
    pipeline_id: Optional[str]
    stage_id: Optional[str]

    # hubspot_file_parser parse file
    source_property: Optional[str]
    destination_property: Optional[str]

    # hubspot_marketing_events subscriber state change
    external_event_id: Optional[str]
    subscriber_state: Optional[str]
    action_date_time_type: Optional[str]
    action_date_time_property: Optional[str]
    action_date_time: Optional[str]

    # hubspot_file_attachment_manager attach file
    file_property: Optional[str]
    destination_object_type: Optional[str]
    association_type: Optional[str]
    association_label: Optional[str]
    file_name_customization_type: Optional[str]
    text_to_append: Optional[str]
    new_file_name: Optional[str]
    access: Optional[str]

    # hubspot_file_attachment_manager delete attached files
    deletion_type: Optional[str]

    # hubspot_task_assistant
    from_owner_type: Optional[str]
    from_owner_property: Optional[str]
    from_owner: Optional[str]
    from_team: Optional[str]
    owner_type: Optional[str]
    owner_property: Optional[str]
    owner: Optional[str]
    team: Optional[str]
    task_status: Optional[str]
    task_type: Optional[List[str]]

    # fix my typo
    duplicate_behavior: Optional[str]

    # line item assistant
    product_id: Optional[int]
    quantity: Optional[float]
    price_type: Optional[str]
    price: Optional[float]
    price_property_value: Optional[str]
    products: Optional[List[str]]
    deletion_type: Optional[str]
    update_deal_amount: Optional[bool]
    create_if_none_match: Optional[bool]


class HubSpotWorkflowActionInputModel(BaseModel):
    callback_id: Optional[str] = Field(alias="callbackId")
    origin: Optional[HubSpotWorkflowActionOriginModel]
    context: Optional[HubSpotWorkflowActionContextModel]
    object: Optional[HubSpotWorkflowActionObjectModel]
    input_fields: Optional[HubSpotWorkflowActionInputFieldsModel] = Field(alias="inputFields")

    class Config:
        populate_by_name = True


class ErrorCode(Enum):
    INVALID_SUBSCRIPTION = "INVALID_SUBSCRIPTION"
    INVALID_PROPERTY_VALUE = "INVALID_PROPERTY_VALUE"
    INVALID_EVENT = "INVALID_EVENT",
    INVALID_FILE_ACCESS = "INVALID_FILE_ACCESS"
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    LINE_ITEMS_NOT_FOUND = "LINE_ITEMS_NOT_FOUND"


class HubSpotWorkflowActionOutputFieldsModel(BaseModel):
    error_code: Optional[ErrorCode]
    hs_execution_state: HubSpotExecutionState
    hs_expiration_duration: Optional[str]
    attempted_correction: Optional[str]
    result: Optional[str]

    def to_hubspot(self):
        output = {
            "hs_execution_state": self.hs_execution_state.value
        }
        if self.error_code:
            output["errorCode"] = self.error_code.value
        if self.hs_expiration_duration:
            output["hs_expiration_duration"] = self.hs_expiration_duration
        if self.attempted_correction:
            output["attempted_correction"] = self.attempted_correction
        if self.result:
            output["result"] = self.result

        return output


class HubSpotWorkflowActionOutputModel(BaseModel):
    output_fields: HubSpotWorkflowActionOutputFieldsModel

    def to_hubspot(self):
        return {
            "outputFields": self.output_fields.to_hubspot()
        }


class HubSpotWorkflowException(Exception):
    def __init__(self, error_code: ErrorCode, message: str):
        self.error_code = error_code
        self.message = message

    def __str__(self):
        return self.message
