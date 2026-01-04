from pydantic import BaseModel, ConfigDict


class RemoveNone(BaseModel):
    model_config = ConfigDict(
        extra="allow"
    )
