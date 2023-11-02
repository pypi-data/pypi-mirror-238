from typing import Optional

from pydantic import BaseModel


class FileOptions(BaseModel):
    access: str
    ttl: Optional[str]
    overwrite: Optional[bool]
    duplicate_validation_strategy: Optional[str]
    duplicate_validation_scope: Optional[str]
