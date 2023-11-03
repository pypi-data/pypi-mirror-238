from enum import Enum


class InstrumentMembershipType(str, Enum):
    MEMBER = "MEMBER"
    PI = "PI"

    def __str__(self) -> str:
        return str(self.value)
