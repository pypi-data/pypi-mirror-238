import logging
from os import environ

from rich.logging import RichHandler
from trongrid_extractoor.helpers.string_constants import PACKAGE_NAME
# from trongrid_extractoor.request_params import DEFAULT_MAX_RECORDS_PER_REQUEST

LOG_LEVEL = environ.get('LOG_LEVEL', 'INFO')


class Config:
    max_records_per_request = 200  # TODO: move to constanst file or something
    flatten_json = False
    quit_after = None


log = logging.getLogger(PACKAGE_NAME)
