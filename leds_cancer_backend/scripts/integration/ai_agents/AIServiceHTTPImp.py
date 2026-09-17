from typing import Any

import requests
from scripts.services.ai_agents.IAIService import IAIService
from scripts.services.ai_agents.LaudoStatus import LaudoStatus

from leds_cancer_backend.scripts.services.ai_agents.LaudoGetResponse import (
    LaudoGetResponse,
)
from leds_cancer_backend.scripts.services.ai_agents.LaudoPayload import LaudoPayload
from leds_cancer_backend.scripts.services.ai_agents.LaudoResponse import (
    LaudoResponse,
    LaudoResponseModel,
)
from leds_cancer_backend.scripts.services.ai_agents.LaudoStatusResponse import (
    LaudoStatusReponse,
)


def _api_laudo_staus_parser(status: str) -> tuple[LaudoStatus, str | None]:
    match status:
        case "proc":
            return LaudoStatus.IN_PROCESSING, None
        case "finish":
            return LaudoStatus.FINISHED, None
        case _:
            return LaudoStatus.ERROR, status


class AIServiceHTTPImp(IAIService):
    def __init__(
        self, status_url: str, new_report_url: str, get_report_url: str
    ) -> None:
        super().__init__()
        self.__status_url = status_url
        self.__newrep_url = new_report_url
        self.__getrep_url = get_report_url

    def get_status(self, laudo_id: int) -> LaudoStatusReponse:
        response = requests.get(self.__status_url.format(laudo_id))
        if response.status_code == 200 or response.status_code == 202:
            data: dict[str, Any] = response.json()
            status: LaudoStatus
            data_status = data.get("status")
            if data_status is None:
                raise Exception()

            status, err = _api_laudo_staus_parser(data_status)
            return LaudoStatusReponse(status, err)
        raise Exception()

    def get_report(self, laudo_id: int) -> LaudoGetResponse:
        response = requests.get(self.__getrep_url.format(laudo_id))
        if response.status_code == 200 or response.status_code == 202:
            data: dict[str, Any] = response.json()
            status: LaudoStatus
            data_status = data.get("status")
            if data_status is None:
                raise Exception()

            status, err = _api_laudo_staus_parser(data_status)

            return LaudoGetResponse(status, err, data.get("report"))
        raise Exception()

    def new_report(self, payload: LaudoPayload) -> LaudoResponse:
        response = requests.post(self.__newrep_url, json=payload.to_dict())

        response.raise_for_status()

        data: dict[str, Any] = response.json()

        _id = data.get("id")
        if _id is None:
            raise Exception()

        if type(_id) is not int:
            if type(_id) is str and _id.isnumeric():
                _id = int(_id)
            else:
                raise Exception()

        model = data.get("model")
        if type(model) is not dict[str, str]:
            raise Exception()
        llm_version = model.get("llm_version")
        pre_diagnosis_version = model.get("pre_diagnosis_version")

        if not llm_version or not pre_diagnosis_version:
            raise Exception()

        _format = data.get("format")
        if type(_format) is not str:
            raise Exception()

        return LaudoResponse(
            _id, LaudoResponseModel(llm_version, pre_diagnosis_version), _format
        )
