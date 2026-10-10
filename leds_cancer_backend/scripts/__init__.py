from dataclasses import dataclass

from decouple import config

from scripts.integration.ai_agents.AIServiceHTTPImp import AIServiceHTTPImp
from scripts.services.ai_agents.IAIService import IAIService

from .services.ai_agents.LaudoPayload import LaudoPayload, LaudoPayloadModel
from .services.ai_agents.LaudoStatus import LaudoStatus


@dataclass
class _dependencies:
    AI_SERVICE: IAIService


_AI_API_BASE_URL: str = config("AI_API_BASE_URL")
DEPENDENCIES = _dependencies(
    AI_SERVICE=AIServiceHTTPImp(
        status_url=f"{_AI_API_BASE_URL}laudo/{'{}'}/status",
        new_report_url=f"{_AI_API_BASE_URL}laudo",
        get_report_url=f"{_AI_API_BASE_URL}laudo/{'{}'}",
        token=config("AI_API_TOKEN", default="dev-token"),
    )
)

__all__: list[str] = [
    "DEPENDENCIES",
    "IAIService",
    "LaudoPayload",
    "LaudoPayloadModel",
    "LaudoStatus",
]
