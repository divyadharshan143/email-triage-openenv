from pydantic import BaseModel
from typing import List


# ----------- Email Object -----------

class Email(BaseModel):
    id: int
    sender: str
    subject: str
    type: str   # "spam", "important", "normal"


# ----------- Observation -----------

class Observation(BaseModel):
    emails: List[Email]


# ----------- Action -----------

class Action(BaseModel):
    email_id: int
    action_type: str   # "delete", "reply", "archive"


# ----------- Reward -----------

class Reward(BaseModel):
    value: float