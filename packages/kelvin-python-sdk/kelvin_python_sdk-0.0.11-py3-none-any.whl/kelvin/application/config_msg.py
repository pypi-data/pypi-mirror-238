from __future__ import annotations

from typing import Dict, List, Optional, Union

from pydantic import BaseModel, StrictBool, StrictFloat, StrictInt, StrictStr

from kelvin.message import KMessageType, Message


class KMessageTypeConfig(KMessageType):
    _TYPE = "configuration"

    @classmethod
    def from_krn(cls, _: str, __: Optional[Dict[str, str]]) -> KMessageTypeConfig:
        return cls(cls._TYPE)


class Resource(BaseModel):
    type: str
    name: Optional[str] = None
    properties: Dict[str, Union[StrictBool, StrictInt, StrictFloat, StrictStr]] = {}
    parameters: Dict[str, Union[StrictBool, StrictInt, StrictFloat, StrictStr]] = {}


class ConfigMessagePayload(BaseModel):
    resources: List[Resource] = []


class ConfigMessage(Message):
    _TYPE = KMessageTypeConfig()

    payload: ConfigMessagePayload
