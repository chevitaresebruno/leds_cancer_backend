from dataclasses import dataclass

from scripts import IAIService


@dataclass
class _dependencies:
    AI_SERVICE: IAIService


DEPENDENCIES = _dependencies()  # TODO
