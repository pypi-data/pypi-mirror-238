# Usage
No configuration is needed to use `trongrid_extractoor` either from the command line or from your own python code.

## Command Line
The `extract_tron_events` script will extract events from Trongrid to either CSV (for `Transfer` events) or JSON (for all other event types). Run `extract_tron_events --help` to see the command line options. `--since` and `--until` arguments should be specified in ISO8601 time format.

Examples:
```sh
# By address
extract_tron_events --until 2023-06-26T16:07:39+00:00 -t TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t

# For symbol (only works for some preconfigured tokens)
extract_tron_events --since 2023-06-26T16:07:39+00:00 -t USDT

# All events (not just 'Transfer')
extract_tron_events -t wstUSDT --e all

# Resume an extraction you already started
extract_tron_events --resume-csv events_HT_TDyvndWuvX5xTBwHPYJi7J3Yq8pq8yh62h.csv
```

#### Other Helpful Command Line Tools
Convert between timestamp seconds and ISO8601 format strings:

```shell
$ epoch_ms_to_datetime 1616507145000
=> 2021-03-23T13:45:45+00:00

$ datetime_to_epoch_ms 2021-03-23T13:45:45
=> 1616507145000000
```

Convert between address formats:
```shell
# From hex format (starting with "0x" (eth) or "41" (tron)):
$ hex_address_to_tron 41102af1de57f7389468e22a72c529d78f2d4a5fde
=> TBShFz6ZKyEySS2vgd4s2yDsCTkQxtfqvy
hex_address_to_tron 0x102af1de57f7389468e22a72c529d78f2d4a5fde
=> TBShFz6ZKyEySS2vgd4s2yDsCTkQxtfqvy

# From base58 ("Tron format)
tron_address_to_hex TBShFz6ZKyEySS2vgd4s2yDsCTkQxtfqvy
=> 0x102af1de57f7389468e22a72c529d78f2d4a5fde
```

Get Tronscan / Trongrid account info:
```shell
$ tron_address_info TBShFz6ZKyEySS2vgd4s2yDsCTkQxtfqvy
╭────────────────────────────────────────────────────────────────╮
│ [NO_TYPE]: TBShFz6ZKyEySS2vgd4s2yDsCTkQxtfqvy (p2pb2bexchange) │
╰────────────────────────────────────────────────────────────────╯

{
   'account_name': 'p2pb2bexchange',
   'address': 'TBShFz6ZKyEySS2vgd4s2yDsCTkQxtfqvy',
   'balance': 3720438,
   'create_time': 1576393722000,
   'latest_opration_time': 1693071735000,
   'latest_withdraw_time': 1662297549000,
   'latest_consume_time': 1621455285000,
   'latest_consume_free_time': 1693071735000,
   'net_window_size': 28800000,
   'net_window_optimized': True,
   'account_resource': {
      'latest_consume_time_for_energy': 1685804475000,
      'energy_window_size': 28800000,
      'energy_window_optimized': True
   }
}
```

Show contract info (functions, events, arguments, etc.)
```shell
$ tron_contract_info TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t
╭──────────────────────────────────────────────────╮
│ TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t (TetherToken) │
╰──────────────────────────────────────────────────╯
{
   'bytecode': '[REDACTED_FOR_BREVITY]',
   'consume_user_resource_percent': 30,
   'name': 'TetherToken',
   'origin_address': 'THPvaUhoh2Qn2y9THCZML3H815hhFhn5YC',
   'abi': {
      'entrys': [
         {
            'outputs': [
               {
                  'type': 'string'
               }
            ],
            'constant': True,
            'name': 'name',
            'stateMutability': 'View',
            'type': 'Function'
         },
         <...snip...>
         {
            'name': 'Pause',
            'type': 'Event'
         },
         {
            'name': 'Unpause',
            'type': 'Event'
         },
         {
            'inputs': [
               {
                  'indexed': True,
                  'name': 'previousOwner',
                  'type': 'address'
               },
               {
                  'indexed': True,
                  'name': 'newOwner',
                  'type': 'address'
               }
            ],
            'name': 'OwnershipTransferred',
            'type': 'Event'
         },
         <...snip...>
      ]
   },
   'origin_energy_limit': 10000000,
   'contract_address': 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t',
   'code_hash': '99bb60e56b4cd2642c6847e372b18b6e0f9514229e3086d3a042d60a4c7b78a9'
}
```

## As Python Package
#### Event Extraction
`contract_events()` hits the `contracts/[CONTRACT_ADDRESS]/events` endpoint and can pull all transfers for a given contract by filtering for `event_name=Transfer`. Other endpoints like `contracts/[CONTRACT_ADDRESS]/transactions` don't seem to really work.
Arguments for `contract_events()` can be found [here](trongrid_extractoor/api.py).

```python
from trongrid_extractoor.api import Api

api = Api()

# For when there's a reasonably small number of events you can use get_all_contract_events()
mints = api.get_all_contract_events(self, 'Mint')

# If there's a whole lot of events it's good to page through them
for events in api.contract_events('TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t', since='2022-05-05', until='2022-08-31'):
    for event in events:
        do_something_with(event)

# Get contract:
usdt = api.get_contract('TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t')

# Get account info:
tether_tronscan_account = api.get_account('TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t')
```

# Resources
* [Trongrid API documentation](https://developers.tron.network/v4.0/reference/note)
* [`TronPy`](https://github.com/andelf/tronpy), a different package

# Contributing
This project was developed with `poetry` and as such is probably easier to work with using `poetry` to manage dependencies in the dev environment. Install with:
```
poetry install --with=dev
```

### Running Tests
```
pytest
```

### Publishing to PyPi
Configuration:
1. `poetry config repositories.chain_argos_pypi https://upload.pypi.org/legacy/`
1. `poetry config pypi-token.chain_argos_pypi [API_TOKEN]`

Publishing:
1. Update `pyproject.toml` version number
1. Update `CHANGELOG.md`
1. `poetry publish --build --repository chain_argos_pypi`

# TODO
1. Walk forward not backward
1. Weird that this yielded dupes on the first page:
   ```
   {request_params.py:29} INFO - Request URL: https://api.trongrid.io/v1/contracts/TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t/events
   Params requesting 'Transfer' events from 2021-04-01T04:00:01+00:00 to 2021-04-01T05:00:00+00:00 (no extra params).
   {response.py:48} INFO - New query requesting data from 2021-04-01T04:00:01+00:00 to 2021-04-01T05:00:00+00:00.
   {progress_tracker.py:67} INFO -   Removed 11 duplicate transactions...
   ```
1. USDT looks incomplete here as 9pm was the last time:
   ```
   WARNING - 0 txns found. We seem to be stuck at 2020-07-09T21:04:24+00:00.
   [2023-06-29, 06:34:36 UTC] {logging_mixin.py:137} INFO -                     WARNING    Last request params:                   api.py:127
                             {'only_confirmed': 'true', 'limit': 200,
                             'min_timestamp': 1594252801000.0,
                             'max_timestamp': 1594328664000.0,
                             'event_name': 'Transfer'}
    ```
1. USDD around this time should be double checked:
   ```
    INFO       Returning 1000 transactions from _rescue_extraction(), modified params in place.                                    api.py:191
    INFO     Writing 1000 rows to 'events_USDD_written_2023-06-28T04.22.00.csv'...                                           csv_helper.py:17
    [06/28/23 10:22:34] INFO       Removed 200 duplicate transactions...                                                                   progress_tracker.py:47
    WARNING  0 txns found. We seem to be stuck at 2023-01-26T03:18:54+00:00.                                                       api.py:103
    WARNING    Last request params: {'only_confirmed': 'true', 'limit': 200, 'min_timestamp': 1483228800000.0, 'max_timestamp':    api.py:104
            1674703134000.0, 'event_name': 'Transfer'}
    ```
