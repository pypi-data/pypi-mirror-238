# -*- coding: utf-8 -*-

"""
Zelfred public API.

Usage example:

.. code-block:: python

    import zelfred.api as zf
"""

from .item import Item
from .item import T_ITEM
from .query import Query
from .query import QueryParser
from .ui import UI
from .ui import T_HANDLER
from .action import open_url
from .action import open_file
from .action import copy_text
from .debug import debugger
from . import exc
