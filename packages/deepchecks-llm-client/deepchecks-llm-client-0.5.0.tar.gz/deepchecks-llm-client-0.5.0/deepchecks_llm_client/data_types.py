import enum
import uuid
from dataclasses import dataclass

__all__ = ["Tag", "EnvType", "AnnotationType", "GoldenSetInteraction", "Step", "StepType"]

from datetime import datetime
from typing import Dict, Any, Union


class Tag(str, enum.Enum):
    """
    Namespace for useful tags that deepchecks case use
    You can use `dc_client.set_tag()` to pass user tags to deepchecks

    USER_INPUT
        Relevant only for auto_collect=True, should contain the input as the user supply it

    INFORMATION_RETRIEVAL
        Relevant only for auto_collect=True, should contain the "information retrieval" if exist

    USER_ID
        The external user that used the AI model

    EXT_INTERACTION_ID
        An external unique id the user can set, this id can be used later on to annotate the interaction
        if EXT_INTERACTION_ID was not supplied by the user, deepchecks will try to capture openai response id
        (i.e. - {"id": <openai unique id>, ...} and will set it as the "ext_interaction_id" of the logged interaction
    """
    USER_INPUT = "user_input"
    INFORMATION_RETRIEVAL = "information_retrieval"
    USER_ID = "user_id"
    EXT_INTERACTION_ID = "ext_interaction_id"


class EnvType(str, enum.Enum):
    PROD = "PROD"
    EVAL = "EVAL"


class AnnotationType(str, enum.Enum):
    GOOD = "good"
    BAD = "bad"
    UNKNOWN = "unknown"


@dataclass
class GoldenSetInteraction:
    id: uuid.UUID
    ext_interaction_id: str
    user_input: str
    information_retrieval: str
    full_prompt: str
    response: str
    created_at: datetime


class StepType(str, enum.Enum):
    LLM = 'LLM'
    INFORMATION_RETRIVAL = 'INFORMATION_RETRIVAL'
    TRANSFORMATION = 'TRANSFORMATION'
    FILTER = 'FILTER'
    FINE_TUNING = 'FINE_TUNING'
    PII_REMOVAL = 'PII_REMOVAL'
    UDF = 'UDF'


@dataclass
class Step:
    name: str
    type: StepType
    attributes: Dict[str, Any]
    started_at: datetime = datetime.now()
    annotation: Union[AnnotationType, None] = None
    finished_at: Union[datetime, None] = None
    input: Union[str, None] = None
    output: Union[str, None] = None
    error: Union[str, None] = None

    def to_json(self):
        return {
            'name': self.name,
            'annotation': self.annotation.value if self.annotation is not None else None,
            'type': self.type.value,
            'attributes': self.attributes,
            'started_at': self.started_at.astimezone().isoformat() if self.started_at else None,
            'finished_at': self.finished_at.astimezone().isoformat() if self.finished_at else None,
            'input': self.input,
            'output': self.output,
            'error': self.error
        }

    @classmethod
    def as_jsonl(cls, steps):
        if steps is None:
            return None
        return [step.to_json() for step in steps]
