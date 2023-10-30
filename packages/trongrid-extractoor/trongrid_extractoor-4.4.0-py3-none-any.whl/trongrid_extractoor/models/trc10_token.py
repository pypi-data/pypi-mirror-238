"""
Dataclass representing one TRC10 token.

{
    "id": 1001427,
    "abbr": "MQTRC10",
    "description": "",
    "name": "MQTRC10",
    "num": 1000000,
    "precision": 6,
    "url": "https://www.google.com",
    "total_supply": 900000000000000000,
    "trx_num": 1000000,
    "vote_score": 0,
    owner_address: str
    "start_time": 1690819200000,
    "end_time": 1690905600000
}
"""
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

from pendulum import DateTime

from trongrid_extractoor.config import log
from trongrid_extractoor.helpers.address_helpers import coerce_to_base58
from trongrid_extractoor.helpers.string_constants import (AMOUNT, DATA, DST, FROM, TO, VALUE, SRC, RESULT, TRANSFER, WAD, SAD)
from trongrid_extractoor.helpers.time_helpers import ms_to_datetime
from trongrid_extractoor.exceptions import UnparseableResponse


@dataclass(kw_only=True)
class Trc10Token:
    id: int
    abbr: str
    description: str
    name: str
    num: int
    precision: int
    url: str
    total_supply: int
    trx_num: int
    vote_score: int
    owner_address: str
    start_time: int | DateTime
    end_time: int | DateTime

    def __post_init__(self) -> None:
        self.start_time = ms_to_datetime(self.start_time)
        self.end_time = ms_to_datetime(self.end_time)
        self.owner_address = coerce_to_base58(self.owner_address)
        self.unique_id = self.id  # For ProgressTracker uniqueness only

    # TODO: rename
    @classmethod
    def from_event_dict(cls, row: Dict[str, str|int]) -> 'Trc10Token':
        """Parse from response."""
        return cls(**row)
