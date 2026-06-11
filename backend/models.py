from pydantic import BaseModel
from datetime import datetime

class inputMessage(BaseModel):
    text: str

class outputMessage(BaseModel):
    id: int
    text: str
    sentiment: str
    timestamp: datetime
    