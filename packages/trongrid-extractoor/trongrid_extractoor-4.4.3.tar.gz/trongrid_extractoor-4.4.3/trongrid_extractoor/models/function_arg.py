"""
Dataclass containing info about argument to a smart contract function.
"""
from dataclasses import asdict, dataclass
from typing import Any, List, Optional

from rich.text import Text

from trongrid_extractoor.config import log
from trongrid_extractoor.helpers.address_helpers import coerce_to_base58
from trongrid_extractoor.helpers.string_constants import ADDRESS, UINT256


@dataclass
class FunctionArg:
    arg_type: str
    name: str = 'anon'

    @classmethod
    def from_function_args(cls, arguments: str) -> List['FunctionArg']:
        """Alternate constructor to convert comma separated list of args to list of FunctionArg objects."""
        args = [arg.strip() for arg in arguments.split(',')]
        return [cls(*arg.split(' ')) for arg in args]

    def coerce_arg_value(self, value: Any, ints_are_hex: bool = False) -> int|str|bool:
        """
        Coerce addresses to the base58 form, amounts to ints, and bools to bools.
        'ints_are_hex': accounts for the fact that raw txns return args as hex strings but events are base10.
        """

        if not isinstance(value, str):
            return value

        if self.arg_type == ADDRESS:
            return coerce_to_base58(value)
        elif self.arg_type == UINT256:
            return int(value, 16) if ints_are_hex else int(value)
        elif self.arg_type == 'bool':
            if value.lower() == 'true':
                return True
            elif value.lower() == 'false':
                return False
            else:
                raise ValueError(f"Cannot coerce '{value}' to boolean")
        else:
            log.warning(f"Unknown type '{self.arg_type}', cannot coerce '{value}' so returning string...")
            return value

    def __eq__(self, other: 'FunctionArg') -> bool:
        return self.arg_type == other.arg_type and self.name == other.name

    def __rich__(self) -> Text:
        return Text('').append(self.name, style='arg_name').append(': ').append(self.arg_type, style='arg_type')

    def __str__(self) -> str:
        return self.__rich__().plain.replace(':', '')

    @staticmethod
    def encode_parameter(parameter: int|str) -> str:
        """Calling smart contracts requires a 64 character long 0 padded hex encoded string."""
        if isinstance(parameter, int):
            return hex(parameter)[2:].zfill(64)
        else:
            raise NotImplementedError(f"encode_parameter() only works with int for now")
