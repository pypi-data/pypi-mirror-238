"""
Dataclass representing one Tron transaction (like an actual transaction, not a TRC20 txn).
"""
from dataclasses import InitVar, asdict, dataclass, field, fields
from typing import Any, ClassVar, Dict, List, Optional, Tuple, Union

import pendulum
from rich.align import Align
from rich.console import Console, ConsoleOptions, RenderResult
from rich.panel import Panel
from rich.text import Text

from trongrid_extractoor.config import log
from trongrid_extractoor.helpers.address_helpers import coerce_to_base58
from trongrid_extractoor.helpers.rich_helpers import console, pretty_print
from trongrid_extractoor.helpers.string_constants import (BLOCK_NUMBER, BLOCK_TIMESTAMP, BLOCK_WRITTEN_AT,
     CALLER_CONTRACT_ADDRESS, CONTRACT, CONTRACT_ADDRESS, INTERNAL_TRANSACTIONS, PARAMETER, TRANSACTION_ID,
     TRIGGER_SMART_CONTRACT, VALUE)
from trongrid_extractoor.models.function import Function

COMMON_HEADER = [TRANSACTION_ID, BLOCK_NUMBER, BLOCK_WRITTEN_AT, 'function_name']
FEE_COLS = ['net_usage', 'net_fee', 'energy_fee', 'energy_usage', 'energy_usage_total']
KEYS_TO_STRIP_FROM_FLAT_DICT = ['raw_data', 'raw_txn', 'method_args']


@dataclass(kw_only=True)
class TronTxn:
    # Key/value store of contract address => method IDs should be populated before use.
    contract_method_info: ClassVar[Dict[str, Dict[str, Function]]] = {}

    transaction_id: str
    block_number: int
    block_written_at: int|pendulum.DateTime
    raw_data: Dict[str, Any]
    internal_transactions: List[Dict[str, Any]]
    net_usage: int
    net_fee: int
    energy_fee: int
    energy_usage: int
    energy_usage_total: int
    raw_txn: Dict[str, Any]

    # Derived fields
    txn_type: Optional[str] = None
    contract_address: Optional[str] = None
    contract_owner: Optional[str] = None
    caller_contract_address: Optional[str] = None
    function_name: Optional[str] = None
    method_id: Optional[str] = None
    method_args: Optional[Dict[str, int|str|bool]] = None

    def __post_init__(self) -> None:
        """Compute various derived fields."""
        self.block_written_at = pendulum.from_timestamp(int(self.block_written_at / 1000.0), pendulum.tz.UTC)
        self.unique_id = self.transaction_id  # There is no log_index / event_index for an actual txn
        self.caller_contract_address = self.raw_txn.get(CALLER_CONTRACT_ADDRESS)
        self.internal_transactions = self.internal_transactions or []
        self.txn_type = None
        self.function = None

        if CONTRACT not in self.raw_data:
            log.warning(f"No contract in this txn '{self.transaction_id}'...")
            return

        contracts = self.raw_data[CONTRACT]
        contract = contracts[0]
        self.txn_type = contract['type']

        if not self.is_trigger_smart_contract_txn():
            return
        if len(contracts) > 1:
            raise ValueError(f"{self.transaction_id} has {len(contracts)} contracts in it...")

        try:
            parameter_value = contract[PARAMETER][VALUE]
            self.contract_address = coerce_to_base58(parameter_value.get(CONTRACT_ADDRESS))
            self.contract_owner = coerce_to_base58(parameter_value['owner_address'])
            function_call_data = parameter_value.get('data')
        except KeyError:
            console.print_exception()
            self._log_raw_json()
            raise

        # Function ID is the first 8 chars
        self.method_id = function_call_data[0:8]
        method_args = [arg.lstrip('0') for arg in self._split_data(function_call_data[8:])]

        if self.contract_address not in type(self).contract_method_info:
            log.warning(f"Unknown contract_address: {self.contract_address}")
            return

        try:
            self.function = type(self).contract_method_info[self.contract_address][self.method_id]
            self.function_name = self.function.name

            if len(method_args) != len(self.function.args):
                raise ValueError(f"Expected {len(self.function.args)} args but got {len(self.method_args)} for {self}")

            self.method_args = {
                arg.name: arg.coerce_arg_value(method_args[i], True)
                for i, arg in enumerate(self.function.args)
            }
        except Exception:
            console.print_exception()
            console.print(f"\n\n--------DATA START-----------")
            pretty_print(self.raw_txn)
            console.print(f"---------DATA-END-----------\n\n")
            raise

    @classmethod
    def from_json_obj(cls, txn: Dict[str, Any], method_ids: Optional[Dict[str, Any]] = None) -> 'TronTxn':
        """Build an event from the json data returned by Trongrid."""
        return cls(
            transaction_id=txn['txID'],
            block_number=txn['blockNumber'],
            block_written_at=txn[BLOCK_TIMESTAMP],
            raw_data=txn['raw_data'],
            internal_transactions=txn[INTERNAL_TRANSACTIONS],
            net_usage=txn['net_usage'],
            net_fee=txn['net_fee'],
            energy_fee=txn['energy_fee'],
            energy_usage=txn['energy_usage'],
            energy_usage_total=txn['energy_usage_total'],
            raw_txn=txn
        )

    def to_properties_dict(self, include_fee_cols: bool = False) -> Dict[str, bool|float|int|str]:
        """Convert to a flat key/value store with most important properties."""
        base_dict = asdict(self)

        if not include_fee_cols:
            for key in FEE_COLS:
                del base_dict[key]

        for key in KEYS_TO_STRIP_FROM_FLAT_DICT:
            del base_dict[key]

        base_dict.update(self.method_args or {})
        base_dict[INTERNAL_TRANSACTIONS] = '; '.join([tx['internal_tx_id'] for tx in (self.internal_transactions)])
        return base_dict

    def is_trigger_smart_contract_txn(self) -> bool:
        """Is this txn created by the triggering of a smart contract?"""
        return TRIGGER_SMART_CONTRACT == self.txn_type

    def block_written_at_str(self) -> str:
        """ISO8601 version of block_written at."""
        return self.block_written_at.format('YYYY-MM-DDTHH:mm:ss')

    def _split_data(self, data: str) -> List[str]:
        """The 'data' field is a concatenated list of args in one monster hex string."""
        return list(map(''.join, zip(*[iter(data)] * 64)))

    def _log_raw_json(self) -> None:
        """Pretty print the raw JSON response from the API."""
        console.print(f"\n\n--------DATA START-----------")
        pretty_print(self.raw_txn)
        console.print(f"---------DATA-END-----------\n\n")

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        panel_txt = Text('[').append(self.block_written_at_str(), style='time').append('] ')
        panel_txt.append(self.transaction_id, style=TRANSACTION_ID)
        panel_txt.append('\n[Contract] ').append(str(self.contract_address), style=CONTRACT_ADDRESS)
        panel_txt.append('   [Owner] ').append(str(self.contract_owner), style=CONTRACT_ADDRESS)

        if self.function is not None:
            panel_txt.append('\n[Fxn] ').append(self.function.__rich__())

        yield(Panel(panel_txt, expand=False))

        if self.method_args is not None:
            for arg_name, arg_value in self.method_args.items():
                yield Text(f"    ").append(arg_name, style='green bold').append(': ').append(str(arg_value))

    def __str__(self) -> str:
        msg = f"[{self.block_written_at_str()}] {self.transaction_id}\n[Contract] {self.contract_address}"

        if self.function is not None:
            msg += f"\n[Fxn] {self.function.method_signature()}"

        return msg
