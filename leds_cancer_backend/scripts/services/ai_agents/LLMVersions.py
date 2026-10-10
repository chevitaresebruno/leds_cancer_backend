from enum import StrEnum


class LLMVersions(StrEnum):
    LEATEST = "v1"
    DEFAULT = "v1"
    BEST = "v1"
    V1 = "v1"

    @staticmethod
    def from_value(value: str | None) -> "LLMVersions":
        match value:
            case LLMVersions.LEATEST:
                return LLMVersions.LEATEST
            case LLMVersions.BEST:
                return LLMVersions.BEST
            case LLMVersions.V1:
                return LLMVersions.V1
            case _:
                return LLMVersions.DEFAULT
