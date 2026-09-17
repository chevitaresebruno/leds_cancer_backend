from dataclasses import dataclass

from .LaudoStatus import LaudoStatus


@dataclass
class LaudoStatusReponse:
    status: LaudoStatus
    err: str | None = None
