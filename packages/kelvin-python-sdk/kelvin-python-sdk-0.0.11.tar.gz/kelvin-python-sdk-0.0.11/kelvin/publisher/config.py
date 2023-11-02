from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel


class MetricInfo(BaseModel):
    class Config:
        extra = "allow"

    asset_names: Optional[List[str]]


class Metric(BaseModel):
    class Config:
        extra = "allow"

    name: str
    data_type: str


class ParameterDefinition(BaseModel):
    class Config:
        extra = "allow"

    name: str
    data_type: str
    default: Optional[Dict]


class MetricInput(Metric):
    class Config:
        extra = "allow"

    sources: Optional[List[MetricInfo]] = []


class MetricOutput(Metric):
    class Config:
        extra = "allow"

    targets: Optional[List[MetricInfo]] = []


class AssetsEntry(BaseModel):
    class Config:
        extra = "allow"

    name: str
    parameters: Dict[str, Dict] = {}


class KelvinAppConfig(BaseModel):
    class Config:
        extra = "allow"

    assets: List[AssetsEntry] = []
    inputs: List[Metric] = []
    parameters: List[ParameterDefinition] = []
    configuration: Dict = {}


class KelvinAppType(BaseModel):
    class Config:
        extra = "allow"

    kelvin: KelvinAppConfig


class AppConfig(BaseModel):
    class Config:
        extra = "allow"

    app: KelvinAppType
