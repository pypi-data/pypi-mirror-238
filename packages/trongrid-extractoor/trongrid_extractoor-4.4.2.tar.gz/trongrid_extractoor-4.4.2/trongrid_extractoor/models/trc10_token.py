"""
Dataclass representing one TRC10 token.
"""
import re
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

from pendulum import DateTime

from trongrid_extractoor.config import log
from trongrid_extractoor.helpers.address_helpers import coerce_to_base58
from trongrid_extractoor.helpers.rich_helpers import console
from trongrid_extractoor.helpers.string_constants import (AMOUNT, DATA, DST, FROM, TO, VALUE, SRC, RESULT, TRANSFER, WAD, SAD)
from trongrid_extractoor.helpers.string_helpers import remove_unprintable_chars
from trongrid_extractoor.helpers.time_helpers import ms_to_datetime, seconds_to_datetime
from trongrid_extractoor.exceptions import UnparseableResponse

YEAR_OUT_OF_RANGE_REGEX = re.compile(r'year \d{4,} is out of range')
INVALID_URLS = ['', 'N/A', 'http://', 'https://']


@dataclass(kw_only=True)
class Trc10Token:
    id: int
    abbr: str
    description: Optional[str]
    name: str
    num: int
    precision: int
    url: Optional[str]
    total_supply: int
    trx_num: int
    vote_score: int
    owner_address: str
    start_time: int | DateTime
    end_time: Optional[int|DateTime]
    raw_json: Dict[str, int|float|str]

    def __post_init__(self) -> None:
        self.description = None if self.description == '' else remove_unprintable_chars(self.description.strip())
        self.owner_address = coerce_to_base58(self.owner_address)
        self.url = None if self.url in INVALID_URLS else self.url
        self.unique_id = self.id  # For ProgressTracker uniqueness only
        self.start_time = ms_to_datetime(self.start_time)

        # Sometimes they set end_time to 50,000 years in the future
        try:
            self.end_time = ms_to_datetime(self.end_time)
        except ValueError as e:
            if YEAR_OUT_OF_RANGE_REGEX.match(str(e)):
                self._warn_and_set_end_time_to_none()
            else:
                log.error(f"FAILED TO PARSE END TIME")
                console.print(self)
                raise e
        except OSError as e:
            if 'Value too large' in str(e):
                self._warn_and_set_end_time_to_none()
            else:
                raise e

    # TODO: rename
    @classmethod
    def from_json_obj(cls, row: Dict[str, str|int]) -> 'Trc10Token':
        """Parse from response."""
        return cls(raw_json=row, **row)

    def to_properties_dict(self) -> Dict[str, bool|float|int|str]:
        """Convert to a flat key/value store with most important properties."""
        base_dict = asdict(self)
        del base_dict['raw_json']
        return base_dict

    def _warn_and_set_end_time_to_none(self) -> None:
        """Print a warning and set end_time to None."""
        log.warning(f"Setting end time of ({self.end_time}) to None...")
        self.end_time = None
