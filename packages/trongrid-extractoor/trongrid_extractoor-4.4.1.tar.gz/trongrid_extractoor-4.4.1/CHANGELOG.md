# NEXT RELEASE

### 4.4.1
* Handle extremely far out `end_date` in `Trc10Token` class
* Clarify `ms_to_datetime()` and `seconds_to_datetime()` methods

## 4.4.0
* Add `Api.list_trc10_tokens()` method

### 4.3.6
* Default `TronTxn.txn_type` to `None`

### 4.3.5
* Debug logging

### 4.3.4
* Add `TronTxn.__str__()` method.
* Remove unused constants.

### 4.3.3
* Fix rich text output for `TronTxn`

### 4.3.2
* Add `search_internal` argument to `Api.account_txns()`
* Add `order_by` to `RequestParams`

### 4.3.1
* Track earliest / latest timestamps seen as datetimes, not epoch timestamps

## 4.3.0
* Add `TronTxn.to_properties_dict()` method
* Rename `Api.txns_for_address()` to `Api.account_txns()`

### 4.2.1
* Downgrade `pycryptodome` requirement to 3.18.0

## 4.2.0
* Add `Api.txns_for_address()` method to get actual txns
* Add `Api.read_contract_data()` to call a read only on chain method
* Rename `RequestParams` to `RequestParams`

## 4.1.0
* Add `TronEvent.event_properties()` and `TronEvent.to_properties_dict()` methods
* Refactor extracting events from API responses
* Remove `compile_csvs.py` script

### 4.0.1
* Fix `TronEvent.__str__()`

# 4.0.0
* Rename `contract_events()` to `write_contract_events()`
* Introduce `contract_events()` that yields lists of events
* Introduce `get_all_contract_events()` method

## 3.1.0
* Add `txn_events()` method to get events for a given txn
* Address coercion works with 0x form of hex addresses

### 3.0.4
* Don't retry `KeyboardInterrupt`

### 3.0.3
* Make Tron retries great again

### 3.0.2
* Fix unparseable JSON response

### 3.0.1
* Print warning and return `None` if unparseable JSON response for `get_account()`

# 3.0.0
* `get_contract()` returns a `TronContract` object instead of a dict

## 2.3.0
* Add `tron_address_info` and `tron_contract_info` CLI scripts
* Add deploying wallet info to contract address names/labels

## 2.2.0
* Add `Api.get_account()` method

### 2.1.9
* Add shorthand for `TRA` and `TBC`

### 2.1.8
* Add `BinancePeg-BUSD`

### 2.1.7
* Add `jwstUSDT` shorthand

### 2.1.6
* Fix parsing for WTRX `Transfer` events
* Privatize some methods on `Response` object

### 2.1.5
* `WBT` address

### 2.1.4
* Allow `APENFT` _or_ `NFT`

### 2.1.3
* `APENFT` is really `NFT`, add `LTCT`. `WBT`, `DCT`, `ETHT` addresses.
* Separate `--token` from `--contract-address` arguments

### 2.1.2
* Typo

### 2.1.1
* Re-enable automatic retries

## 2.1.0
* Add `Api.get_contract()`

### 2.0.1
* Rename `events_for_contract()` to `contract_events()`
* Rename `--token` arg `--contract-address`
* Re-rename `contract_addr` to `contract_address` (not `token_address`)
* Improve JSON events output
* Log event counts, first time encountering different event names
* Log timestamps even when not exactly modulo 4000 rows written
* Add `--version` flag

# 2.0.0 (YANKED)
* Allow for a `StringIO` object to be passed in to `events_for_contract()` and written to instead of writing to disk
* Log timestamp of the event every 4000 rows
* Rename `contract_addr` arg in `events_for_contract()` to `token_address`
* Rename `--resume-from-csv` argument

### 1.2.7
* Add missing `exceptions.py`

### 1.2.6
* Standardize rounding of floats to ints

### 1.2.5
* Retry rate limit exceeded errors
* Fix warning message in ms_to_datetime

### 1.2.4
* Log a warning that includes the duplicate transaction id if duplicates are encountered

### 1.2.3
* Add symbol shorthand for many tokens

### 1.2.2
* Truncate the `.0` off of the `amount` and `ms_from_epoch` column (turn them to integers, which is what they actually are)

### 1.2.1
* Two underscores between each section of csv filename

## 1.2.0
* Add `--event-name` argument to CLI (and API)
* Allow pulling of all events with `--event-name None`
* Events other than `Transfer` write to JSON
* Rename `extract_tron_transactions` to `extract_tron_events`

## 1.1.0
* Add `parse_written_at_from_filename()` method
* `TCNH` and `wstUSDT` token shorthand

# 1.0.0
* As of mid July 2023 TronGrid seems to have repaired their API so it no longer just gives up after returning 5 pages of responses. This dramatically simplifies the code in this package.
* Guarantee there is always a CSV with a header row at the end even if there's no rows returned by query.
* enable `jUSDC` and `stUSDT` token shorthand symbols

## 0.4.0
* `--resume` option automatically determines the token address from the CSV
* `--debug` option for `extract_tron_transactions` CLI
* `--list-symbols` option for `extract_tron_transactions` CLI
* Accept command line args without timezone (assume UTC)
* Log count of rows extracted.
* Fix crash when throwing error about unable to resume from CSV

### 0.3.12
* `RequestParams` class, better logging

### 0.3.11
* Only use Rich formatted logging when running with the CLI

### 0.3.10
* Reduce verbosity of logged writes

### 0.3.9
* Don't consider small timespan queries failures in need of rescuing if they return 0 rows.

### 0.3.8
* Fix buggy handling of false completes

### 0.3.7
* Delete output CSV if it already exists
* Fix bug with resuming from CSV with out of order rows
* Only do a rescue when it is impossible to load next page
* Add a bunch of tokens (`HT`, `SUN`, `JST`, `BTT`, etc.)

### 0.3.6
* Simplify inner logic and retries etc.

### 0.3.5
* Avoid endless loop on `is_false_complete_response()`
* Refactor `response.pretty_print()`
* Don't allow walkbacks to walk back past the start of the period

### 0.3.4
* `Response` object refactor
* Smarter logging
* Strip `:` and `/` from CSV filenames

### 0.3.3
* Add `filename_suffix` arg

### 0.3.2
* Tidbits

### 0.3.1
* Better 0 txn response handling
* `compile_csvs.py` script

# 0.3.0
* `--resume-csv` option
* Use floats instead of strings for timestamps. Add `_is_paging_complete()` method
* Handle src/dst/wad txns

# 0.2.0
* `ProgressTracker` class
* `event_number` column
* Accept symbols like `USDT` as argument instead of just addresses
* Accept `--since`, `--until`, and `--output-dir` options on the command line

# 0.1.0
* Initial release.
