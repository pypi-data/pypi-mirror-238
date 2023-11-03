"""
This module provides the core functionality of the Juice Core Uplink API Client
in a more convenient way than the generated code.

May functionalities are not yet implemented, but some are.
"""

from importlib_metadata import version

__version__ = version("juice-core-uplink-api-client")


from .SHTRestInterface import SHTRestInterface, expand_column
