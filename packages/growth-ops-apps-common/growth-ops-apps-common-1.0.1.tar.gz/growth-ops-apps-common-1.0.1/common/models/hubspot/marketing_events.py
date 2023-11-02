from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MarketingEvent(BaseModel):
    event_name: str
    event_description: Optional[str]
    event_url: Optional[str]
    event_type: Optional[str]
    start_date_time: Optional[str]
    end_date_time: Optional[str]
    event_organizer: str
    external_account_id: str
    external_event_id: str
    custom_properties: Optional[dict]

    def to_hubspot(self):
        now = int(datetime.now().timestamp() * 1000)
        return {
            "eventName": self.event_name,
            "eventType": self.event_type,
            "eventDescription": self.event_description,
            "startDateTime": self.start_date_time,
            "endDateTime": self.end_date_time,
            "eventOrganizer": self.event_organizer,
            "eventUrl": self.event_url,
            "externalAccountId": self.external_account_id,
            "externalEventId": self.external_event_id,
            "customProperties": [
                {
                    "name": k,
                    "value": v,
                    "timestamp": now,
                    "sourceId": "growth_operations_marketing_events",
                    "sourceLabel": "Growth Operations Marketing Events",
                    "source": "API"
                } for k, v in self.custom_properties.items()
            ] if self.custom_properties else None
        }


class Registration(BaseModel):
    portal_id: int
    external_event_id: str
    contact_id: int
    subscriber_state: str
    timestamp: int
