from enum import StrEnum


class LaudoStatus(StrEnum):
    IN_PROCESSING = "in_processing"
    FINISHED = "fineshed"
    ERROR = "error"
