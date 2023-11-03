from enum import Enum


class RestApiPlanSimphonyOppsReadMode(str, Enum):
    OPEN = "open"
    STRICT = "strict"

    def __str__(self) -> str:
        return str(self.value)
