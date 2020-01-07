from dataclasses import dataclass, field
from decimal import Decimal
from enum import IntEnum

DECIMALS = 10 ** 18


class Wei(int):
    unit = 'eth'

    def __str__(self):
        return f"{self.to_eth()} {self.unit}"

    @classmethod
    def from_eth(cls, eth: Decimal):
        return cls(eth * DECIMALS)

    def to_eth(self) -> Decimal:
        return Decimal(self) / DECIMALS


class Tributes(Wei):
    unit = 'trb'


class StakerStatus(IntEnum):
    NOT_STAKED = 0
    STAKED = 1
    WITHDRAWING = 2
    DISPUTED = 3


@dataclass
class CurrentVariables:
    challenge: bytes = field(repr=False)
    request: int
    difficulty: int
    query: str
    granularity: int
    tip: int
