from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class HubSpotAppWebhookEvent(BaseModel):
    event_id: Optional[int] = Field(alias='eventId')
    event_type: Optional[str] = Field(alias='eventType')
    subscription_id: Optional[int] = Field(alias='subscriptionId')
    portal_id: Optional[int] = Field(alias='portalId')
    app_id: Optional[int] = Field(alias='appId')
    occurred_at: Optional[int] = Field(alias='occurredAt')
    subscription_type: Optional[str] = Field(alias='subscriptionType')
    attempt_number: Optional[int] = Field(alias='attemptNumber')
    change_source: Optional[str] = Field(alias='changeSource')
    association_type: Optional[str] = Field(alias='associationType')
    from_object_id: Optional[int] = Field(alias='fromObjectId')
    to_object_id: Optional[int] = Field(alias='toObjectId')
    association_removed: Optional[bool] = Field(alias='associationRemoved')
    is_primary_association: Optional[bool] = Field(alias='isPrimaryAssociation')
    primary_object_id: Optional[int] = Field(alias='primaryObjectId')
    merged_object_ids: Optional[List[int]] = Field(alias='mergedObjectIds')
    new_object_id: Optional[int] = Field(alias='newObjectId')
    number_of_properties_moved: Optional[int] = Field(alias='numberOfPropertiesMoved')
    object_id: Optional[int] = Field(alias='objectId')
    property_name: Optional[str] = Field(alias='propertyName')
    property_value: Optional[str] = Field(alias='propertyValue')
    message_id: Optional[int] = Field(alias='messageId')
    message_type: Optional[str] = Field(alias='messageType')

    class Config:
        populate_by_name = True


class HubSpotWorkflowWebhookEvent(BaseModel):
    portal_id: Optional[int] = Field(alias='portalId')
    object_type_id: Optional[str] = Field(alias='objectTypeId')
    object_id: Optional[int] = Field(alias='objectId')
    properties: Optional[dict]

    class Config:
        populate_by_name = True
