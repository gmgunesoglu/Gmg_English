from pydantic import BaseModel, constr
from typing import List
from enum import Enum

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

class OptionType(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"



# POST readings/units: ReadingUnitCreate -> string
# PUT readings/units/{id}: ReadingUnitCreate + id -> string
class ReadingUnitCreate(BaseModel):
    title: constr(min_length=1, max_length=35)

# GET readings/units: -> List[ReadingUnitGets]
class ReadingUnitGets(BaseModel):
    id: int
    name: str
    titles: List[ReadingTextBase]

# DELETE readings/units/{id}: id -> string


# GET readings/texts: -> List[ReadingTextGets]
class ReadingTextGets(BaseModel):
    id: int
    unit_name: str
    title: str

# GET readings/texts/{id}: id -> ReadingTextGet
class ReadingTextGet(ReadingTextGets):
    context: str
    quests: List[ReadingQuestBase]

# POST readings/texts: ReadingTextCreate -> ReadingTextGets
# PUT readings/texts/{id}: ReadingTextCreate + id -> string
class ReadingTextCreate(BaseModel):
    unit_id: int
    title: constr(min_length=1, max_length=70)
    context: str

# DELETE readings/texts/{id}: id -> string




# POST readings/quests: ReadingQuestPost -> string
# PUT readings/quests/{id}: ReadingQuestPost + id -> string
class ReadingQuestPost(BaseModel):
    text_id: int
    quest: constr(min_length=5, max_length=400)
    option_a: constr(min_length=1, max_length=100)
    option_b: constr(min_length=1, max_length=100)
    option_c: constr(min_length=1, max_length=100)
    option_d: constr(min_length=1, max_length=100)
    correct_option: OptionType
    justification : constr(min_length=10, max_length=500)

# DELETE readings/quests/{id}: id -> string