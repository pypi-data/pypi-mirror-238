from pydantic import BaseModel


class BkYouSupportPackage(BaseModel):
    sessionId: str
    url: str
