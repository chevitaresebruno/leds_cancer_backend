from dataclasses import dataclass, field
from typing import Any

from .LaudoFormats import LaudoFormats
from .LLMVersions import LLMVersions
from .PreDiagnosisVersion import PreDiagnosisVersions


@dataclass
class LaudoPayloadModel:
    llm_version: LLMVersions = LLMVersions.DEFAULT
    pre_diagnosis_version: PreDiagnosisVersions = PreDiagnosisVersions.DEFAULT

    @staticmethod
    def best() -> "LaudoPayloadModel":
        return LaudoPayloadModel(LLMVersions.BEST, PreDiagnosisVersions.BEST)

    def to_dict(self) -> dict[str, Any]:
        return {
            "llm_version": self.llm_version,
            "pre_diagnosis_version": self.pre_diagnosis_version,
        }


@dataclass
class LaudoPayload:
    image_id: int
    model: LaudoPayloadModel = field(default_factory=LaudoPayloadModel)
    format: LaudoFormats = LaudoFormats.DEFAULT

    @staticmethod
    def from_request(
        image_id: int,
        llm_model: str | None,
        pdai_model: str | None,
        format: LaudoFormats = LaudoFormats.DEFAULT,
    ) -> "LaudoPayload":
        true_llm_model = LLMVersions.from_value(llm_model)
        true_pdai_model = PreDiagnosisVersions.from_value(pdai_model)

        return LaudoPayload(
            image_id, LaudoPayloadModel(true_llm_model, true_pdai_model), format
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "image_id": self.image_id,
            "model": self.model.to_dict(),
            "format": self.format,
        }
