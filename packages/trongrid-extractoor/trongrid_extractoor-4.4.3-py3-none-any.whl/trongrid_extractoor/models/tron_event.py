"""
Dataclass representing one TRC20 token transfer.
"""
from dataclasses import asdict, dataclass, field, fields
from typing import Any, Dict, List, Optional, Tuple, Union

import pendulum
from rich.text import Text

from trongrid_extractoor.config import log
from trongrid_extractoor.helpers.address_helpers import coerce_to_base58
from trongrid_extractoor.helpers.rich_helpers import color_picker
from trongrid_extractoor.helpers.string_constants import (BLOCK_NUMBER, BLOCK_TIMESTAMP, CONTRACT_ADDRESS,
     EVENT_NAME, RESULT, RESULT_TYPE, TRANSACTION_ID)
from trongrid_extractoor.helpers.time_helpers import ms_to_datetime
from trongrid_extractoor.models.function_arg import FunctionArg

KEYS_TO_STRIP_FROM_FLAT_DICT = ['ms_from_epoch', 'raw_event']


@dataclass(kw_only=True)
class TronEvent:
    event_name: str
    token_address: str  # TODO: Should be contract_address
    transaction_id: str
    event_index: int
    ms_from_epoch: int  # TODO: rename block_timestamp and get rid of the timestamp version
    raw_event: Optional[Dict[str, Union[dict, str, float, int]]] = None
    block_number: Optional[int] = None
    block_written_at: Optional[pendulum.DateTime] = None  # Derived field; not passed in constructor

    def __post_init__(self):
        self.block_written_at = ms_to_datetime(self.ms_from_epoch)
        self.unique_id = f"{self.transaction_id}/{self.event_index}"

    @classmethod
    def from_json_obj(cls, row: Dict[str, str|float|int]) -> 'TronEvent':
        """Build an event from the json data returned by Trongrid."""
        return cls(
            event_name=row[EVENT_NAME],
            token_address=row[CONTRACT_ADDRESS],
            ms_from_epoch=int(float(row[BLOCK_TIMESTAMP])),
            block_number=int(row[BLOCK_NUMBER]),
            transaction_id=row[TRANSACTION_ID],
            event_index=int(row['event_index']),
            raw_event=row
        )

    def event_properties(self) -> Dict[str, bool|float|int|str]:
        """
        Normalize the 'result' dict which is where the event specific properties live.
        Other conversions:
           - hex addresses converted to base58
           - booleans and numbers coerced to native types
        """
        if self.raw_event is None:
            raise ValueError(f"No 'raw_event' to normalize!")

        result = self.raw_event[RESULT]
        result_types = self.raw_event[RESULT_TYPE]

        if 2 * len(result_types) != len(result):
            log.warning(f"Found {len(result_types)} result types for {len(result)} results! Naming may be incorrect.")

        return {
            arg_name: FunctionArg(arg_type).coerce_arg_value(result[arg_name])
            for arg_name, arg_type in result_types.items()
        }

    def to_properties_dict(self) -> Dict[str, bool|float|int|str]:
        """Convert to a flat key/value store with all relevant properties."""
        base_dict = asdict(self)
        base_dict['caller_contract_address'] = self.raw_event['caller_contract_address']
        base_dict[CONTRACT_ADDRESS] = base_dict['token_address']
        del base_dict['token_address']

        for key in KEYS_TO_STRIP_FROM_FLAT_DICT:
            del base_dict[key]

        base_dict.update(self.event_properties())
        return base_dict

    def __str__(self) -> str:
        msg = f"{self.event_name}: {self.token_address}, ID: {self.transaction_id}/{self.event_index}"
        return msg

    def __rich__(self) -> Text:
        color = color_picker.pick_color(self.event_name)
        txt = Text('[').append(str(self.block_written_at)).append('] ').append(self.event_name, style=color).append('\n')

        for k, v in self.event_properties().items():
            txt.append(f"    {k}", style='white').append(": ").append(str(v) + '\n', style='color(217)')

        return txt.append('\n')
