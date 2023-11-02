from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field


class HubSpotSettingsIframeModel(BaseModel):
    iframeUrl: str


class HubSpotSettingsIframeResponseModel(BaseModel):
    response: HubSpotSettingsIframeModel


class HubSpotAppSettingsActionTypeModel(Enum):
    ACCOUNTS_FETCH = "ACCOUNTS_FETCH"
    BUTTON_UPDATE = "BUTTON_UPDATE"
    IFRAME_FETCH = "IFRAME_FETCH"
    TOGGLE_FETCH = "TOGGLE_FETCH"
    TOGGLE_UPDATE = "TOGGLE_UPDATE"
    DROPDOWN_FETCH = "DROPDOWN_FETCH"
    DROPDOWN_UPDATE = "DROPDOWN_UPDATE"


class HubSpotAppSettingsModel(BaseModel):
    action_type: HubSpotAppSettingsActionTypeModel = Field(alias="actionType")
    app_id: int = Field(alias="appId")
    portal_id: int = Field(alias="portalId")
    user_id: int = Field(alias="userId")
    user_email: str = Field(alias="userEmail")
    account_id: Optional[str] = Field(alias="accountId")
    enabled: Optional[bool]


class HubSpotAccountSettingsModel(BaseModel):
    accountId: str
    accountName: Optional[str]
    accountLogoUrl: Optional[str]


class HubSpotSettingsAccountListModel(BaseModel):
    accounts: List[HubSpotAccountSettingsModel]


class HubSpotAccountsFetchResponseModel(BaseModel):
    response: HubSpotSettingsAccountListModel


class HubSpotAccountDetails(BaseModel):
    portal_id: int = Field(alias="portalId")
    time_zone: str = Field(alias="timeZone")
    company_currency: str = Field(alias="companyCurrency")
    additional_currencies: List[str] = Field(alias="additionalCurrencies")
    utc_offset: str = Field(alias="utcOffset")
    utc_offset_milliseconds: int = Field(alias="utcOffsetMilliseconds")
    ui_domain: str = Field(alias="uiDomain")
    data_hosting_location: str = Field(alias="dataHostingLocation")
