from pydantic import BaseModel, constr
from typing import Optional, List

# subclass for ReadingUnitGets
class ReadingTextBase(BaseModel):
    id: int
    title: str

# subclass for ReadingTextGet
class ReadingQuestBase(BaseModel):
    id: int
    quest: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    justification : str


# POST readings/units: ReadingUnitCreate -> Returns string
# PUT readings/units/{id}: ReadingUnitCreate -> Returns string
class ReadingUnitCreate(BaseModel):
    title: constr(min_length=1, max_length=35)

# GET readings/units
class ReadingUnitGets(BaseModel):
    id: int
    name: str
    titles: List[ReadingTextBase]

# DELETE admin/readings/units/{id} (NoBody!) id -> string





# POST admin/readings/texts: ReadingTextCreate -> ReadingTextGet
class ReadingTextCreate(BaseModel):
    unit_id: int
    subject: str
    context: str

# GET readings/texts -> ReadingTextGet
class ReadingTextGet(BaseModel):
    id: int
    unit: str
    subject: str
    context: str
    quests: List[ReadingQuestBase]