# -*- coding: utf-8 -*-
"""
    pip_services4_commons.data.__init__
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Abstract, portable data types. For example – anytype, anyvalues, anyarrays, anymaps, stringmaps
    (on which many serializable objects are based on – configmap,
    filtermaps, connectionparams – all extend stringvaluemap).
    Includes standard design patterns for working with data
    (data paging, filtering, GUIDs).

    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

__all__ = [
    'AnyValue', 'AnyValueArray', 'AnyValueMap', 'ICloneable', 'StringValueMap'
]

from .AnyValue import AnyValue
from .AnyValueArray import AnyValueArray
from .AnyValueMap import AnyValueMap
from .ICloneable import ICloneable
from .StringValueMap import StringValueMap