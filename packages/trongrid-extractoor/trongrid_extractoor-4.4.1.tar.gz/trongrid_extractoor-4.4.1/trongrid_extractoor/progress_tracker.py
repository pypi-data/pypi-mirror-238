"""
Class to track what objects we've already seen and the CSV to write to. Objects that will be tracked
by this class should have a 'unique_id' property. Works for both contract addresses and standard
wallet addresses.
"""
import csv
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union

from rich.text import Text

from trongrid_extractoor.config import log
from trongrid_extractoor.helpers.rich_helpers import print_error_and_exit
from trongrid_extractoor.helpers.string_constants import BLOCK_NUMBER, BLOCK_WRITTEN_AT, TRANSFER
from trongrid_extractoor.models.trc20_txn import Trc20Txn
from trongrid_extractoor.models.tron_event import TronEvent


class ProgressTracker:
    def __init__(self, address: Optional[str] = None, event_cls: Optional[Type] = None) -> None:
        self.address = address
        self.event_cls = event_cls
        # Initialize empty vars
        self.already_processed_uniq_ids = set()
        self.earliest_timestamp_seen = None
        self.latest_timestamp_seen = None
        self.min_block_number_seen = None
        self.max_block_number_seen = None
        self.rows_in_scanned_csv = 0

    @classmethod
    def for_event_name(cls, address: Optional[str] = None, event_name: str = 'Transfer') -> 'ProgressTracker':
        """Alternate constructor that takes uses the name of the event to determine the event class."""
        return cls(address, Trc20Txn if event_name == TRANSFER else TronEvent)

    def remove_already_processed_txns(self, txns: List[TronEvent]) -> List[TronEvent]:
        """
        Track already seen unique_ids ("transaction_id/event_index") and the earliest block_timestamp
        encountered. Remove any transactions w/IDs return the resulting list.
        """
        filtered_txns = []

        for txn in txns:
            if txn.unique_id in self.already_processed_uniq_ids:
                log.warning(f"Already processed: {txn}")
                continue

            if BLOCK_WRITTEN_AT in dir(txn):
                if self.earliest_timestamp_seen is None or txn.block_written_at < self.earliest_timestamp_seen:
                    self.earliest_timestamp_seen = txn.block_written_at
                if self.latest_timestamp_seen is None or txn.block_written_at > self.latest_timestamp_seen:
                    self.latest_timestamp_seen = txn.block_written_at

            if BLOCK_NUMBER in dir(txn):
                if self.min_block_number_seen is None or txn.block_number < self.min_block_number_seen:
                    self.min_block_number_seen = txn.block_number
                if self.max_block_number_seen is None or txn.block_number > self.max_block_number_seen:
                    self.max_block_number_seen = txn.block_number

            filtered_txns.append(txn)
            self.already_processed_uniq_ids.add(txn.unique_id)

        removed_txn_count = len(txns) - len(filtered_txns)

        if removed_txn_count > 0:
            log.warning(f"  Removed {removed_txn_count} duplicate transactions...")

        return filtered_txns

    def number_of_rows_written(self) -> int:
        return len(self.already_processed_uniq_ids) - self.rows_in_scanned_csv

    def load_csv_progress(self, resume_from_csv: Path) -> None:
        """Read a CSV and consider each row as having already been processed."""
        if not resume_from_csv.exists():
            raise ValueError(f"Can't resume from CSV because '{resume_from_csv}' doesn't exist!")

        with open(resume_from_csv, mode='r') as csvfile:
            for row in csv.DictReader(csvfile, delimiter=','):
                self.remove_already_processed_txns([Trc20Txn(**{'event_name': TRANSFER, **row})])
                row_address = row['token_address']

                if self.address is None:
                    self.address = row_address
                    log.info(f"Found token address '{self.address}' in CSV...")
                elif self.address != row_address:
                    msg = f"CSV contains data for '{row_address}' but '{self.address}' given as --token arg."
                    print_error_and_exit(msg)

                self.rows_in_scanned_csv += 1

        log.info(f"Processed {self.rows_in_scanned_csv} rows in '{resume_from_csv}',")
        log.info(f"   Resuming from {self.earliest_timestamp_seen}.")

    def log_state(self, response: 'Response') -> None:
        """Log info about extraction progress."""
        log.info(f"Extraction complete. Extracted {self.number_of_rows_written()} events.")
        log.info(f"     Lowest block_number seen: {self.min_block_number_seen}")
        log.info(f"    Highest block_number seen: {self.max_block_number_seen}\n\nLast API response:")
        response.print_abbreviated()
