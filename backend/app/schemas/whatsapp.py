from pydantic import BaseModel, Field


class WhatsAppWebhookRequest(BaseModel):
    entry: list[dict] = Field(default_factory=list)
