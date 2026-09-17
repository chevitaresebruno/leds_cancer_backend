from dataclasses import dataclass


@dataclass
class LaudoResponseModel:
    llm_version: str
    pre_diagnosis_version: str


@dataclass
class LaudoResponse:
    laudo_id: int
    model: LaudoResponseModel
    format: str
