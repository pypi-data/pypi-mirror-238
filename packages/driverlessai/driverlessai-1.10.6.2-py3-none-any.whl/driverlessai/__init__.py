#!/usr/bin/env python
# Copyright 2020 H2O.ai; Proprietary License;  -*- encoding: utf-8 -*-

import sys
import warnings

from driverlessai import token_providers
from driverlessai.__about__ import __build_info__, __version__
from driverlessai._core import Client, is_server_up

__all__ = [
    "__version__",
    "__build_info__",
    "Client",
    "is_server_up",
    "token_providers",
]

if sys.version_info[0] == 3 and sys.version_info[1] <= 7:
    warnings.warn(
        "Warning! Support for Python 3.7 will be dropped from v1.10.7 onwards.",
        stacklevel=2,
    )
