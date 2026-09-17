from dataclasses import dataclass

from .LaudoStatus import LaudoStatus


@dataclass
class LaudoGetResponse:
    status: LaudoStatus
    err: str | None
    report: str | None

    @property
    def is_ok(self) -> bool:
        return (
            self.status is not LaudoStatus.ERROR
            and self.err is None
            and self.report is not None
        )
