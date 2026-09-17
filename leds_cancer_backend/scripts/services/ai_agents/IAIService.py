from typing import Protocol

from .LaudoGetResponse import LaudoGetResponse
from .LaudoPayload import LaudoPayload
from .LaudoResponse import LaudoResponse
from .LaudoStatusResponse import LaudoStatusReponse


class IAIService(Protocol):
    def get_status(self, laudo_id: int) -> LaudoStatusReponse: ...

    def new_report(self, payload: LaudoPayload) -> LaudoResponse: ...

    def get_report(self, laudo_id: int) -> LaudoGetResponse: ...
