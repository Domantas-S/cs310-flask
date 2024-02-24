from typing import Optional, List
from enum import Enum
from pydantic import BaseModel

class Common(BaseModel):
    text: List[List[str]]
    start: List[List[int]]
    entity_id: List[List[str]]

class ValuedCommonBool(Common):
    value: bool

class ValuedCommonStr(Common):
    value: str
    
class EventInfo(BaseModel):
    event_type: str
    event_id: str
    

class Subject(Common):
    Age: Optional[Common]
    Disorder: Optional[Common]
    Gender: Optional[Common]
    Population: Optional[Common]
    Race: Optional[Common]


class Combination(EventInfo):
    Drug: Optional[Common]
    Trigger: Optional[Common]


class Treatment(Common):
    Drug: Optional[Common]
    Disorder: Optional[Common]
    Dosage: Optional[Common]
    Duration: Optional[Common]
    Trigger: Optional[Common]
    Route: Optional[Common]
    Time_elapsed: Optional[Common]
    Freq: Optional[Common]
    Combination: Optional[List[Combination]]
    
class Event(EventInfo):
    Effect: Optional[Common]
    Trigger: Optional[Common]
    Negated: Optional[ValuedCommonBool]
    Speculated: Optional[ValuedCommonBool]
    Severity: Optional[ValuedCommonStr]
    Subject: Optional[Subject]
    Treatment: Optional[Treatment]

class Events(BaseModel):
    events: List[Event]

class Record(BaseModel):
    id: str
    context: str
    is_mult_event: bool
    annotations: List[Events]
