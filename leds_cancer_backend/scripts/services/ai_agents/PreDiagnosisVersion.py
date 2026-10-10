from enum import StrEnum


class PreDiagnosisVersions(StrEnum):
    LEATEST = "v0"
    DEFAULT = "v0"
    BEST = "v0"
    V0 = "v0"

    @staticmethod
    def from_value(value: str | None) -> "PreDiagnosisVersions":
        match value:
            case PreDiagnosisVersions.LEATEST:
                return PreDiagnosisVersions.LEATEST
            case PreDiagnosisVersions.BEST:
                return PreDiagnosisVersions.BEST
            case PreDiagnosisVersions.V0:
                return PreDiagnosisVersions.V0
            case _:
                return PreDiagnosisVersions.DEFAULT
