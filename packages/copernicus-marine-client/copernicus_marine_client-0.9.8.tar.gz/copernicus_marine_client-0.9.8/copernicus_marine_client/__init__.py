"""
.
"""

from importlib.metadata import version
import pathlib

import json
import logging.config
import time

__version__ = version("copernicus-marine-client")

log_configuration_dict = json.load(
    open(
        pathlib.Path(
            pathlib.Path(__file__).parent, "logging_conf.json"
        )
    )
)
logging.config.dictConfig(log_configuration_dict)
logging.Formatter.converter = time.gmtime

from copernicus_marine_client.python_interface.login import login
from copernicus_marine_client.python_interface.describe import describe
from copernicus_marine_client.python_interface.get import get
from copernicus_marine_client.python_interface.subset import subset
from copernicus_marine_client.python_interface.open_dataset import open_dataset
from copernicus_marine_client.python_interface.open_dataset import load_xarray_dataset  # depracated
from copernicus_marine_client.python_interface.read_dataframe import read_dataframe
from copernicus_marine_client.python_interface.read_dataframe import load_pandas_dataframe  # depracated
