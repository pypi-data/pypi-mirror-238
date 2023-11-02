from enum import Enum
from typing import List, Optional, Any

from pydantic import BaseModel


class HubSpotCRMCardActionType(Enum):
    IFRAME = "IFRAME"
    ACTION_HOOK = "ACTION_HOOK"
    CONFIRMATION_ACTION_HOOK = "CONFIRMATION_ACTION_HOOK"


class HubSpotCRMCardActionModel(BaseModel):
    type: HubSpotCRMCardActionType
    width: Optional[int]
    height: Optional[int]
    uri: str
    label: str
    associatedObject_properties: Optional[List[str]]
    confirmationMessage: Optional[str]
    confirmButtonText: Optional[str]
    cancelButtonText: Optional[str]


class HubSpotCRMCardModel(BaseModel):
    results: Optional[List]
    primaryAction: HubSpotCRMCardActionModel


class TopLevelAction(BaseModel):
    type: HubSpotCRMCardActionType
    width: Optional[int]
    height: Optional[int]
    url: str
    label: str
    propertyNamesIncluded: Optional[List[str]]


class TopLevelActions(BaseModel):
    settings: Optional[TopLevelAction]
    primary: Optional[TopLevelAction]
    secondary: Optional[List[TopLevelAction]]


class Token(BaseModel):
    name: str
    label: str
    dataType: str
    value: Any


class Action(BaseModel):
    type: str = "ACTION_HOOK"
    confirmation: Optional[str]
    httpMethod: str
    url: str
    label: str
    propertyNamesIncluded: Optional[List[str]]


class Section(BaseModel):
    id: str
    title: str
    linkUrl: Optional[str]
    tokens: Optional[List[Token]]
    actions: Optional[List[Action]]


class CRMCard(BaseModel):
    responseVersion: str = "v3"
    allItemsLinkUrl: str
    cardLabel: str
    topLevelActions: Optional[TopLevelActions]
    sections: Optional[List[Section]]
