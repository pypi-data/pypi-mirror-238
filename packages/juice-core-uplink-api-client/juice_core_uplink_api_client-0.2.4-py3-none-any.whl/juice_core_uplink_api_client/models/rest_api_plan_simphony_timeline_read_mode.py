from enum import Enum


class RestApiPlanSimphonyTimelineReadMode(str, Enum):
    OPEN = "open"
    STRICT = "strict"

    def __str__(self) -> str:
        return str(self.value)
