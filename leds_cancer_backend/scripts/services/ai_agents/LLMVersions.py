from enum import StrEnum


class LLMVersions(StrEnum):
    LEATEST = "V0"
    DEFAULT = "V0"
    BEST = "v0"
    V0 = "v0"

    @staticmethod
    def from_value(value: str | None) -> "LLMVersions":
        match value:
            case LLMVersions.LEATEST:
                return LLMVersions.LEATEST
            case LLMVersions.BEST:
                return LLMVersions.BEST
            case LLMVersions.V0:
                return LLMVersions.V0
            case _:
                return LLMVersions.DEFAULT
