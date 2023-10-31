# -*- coding: utf-8 -*-
"""
    pip_services3_commons.data.__init__
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
    'IIdentifiable', 'IStringIdentifiable', 'IChangeable',
    'INamed', 'ITrackable', 'IVersioned', 'MultiString',
]

from .IChangeable import IChangeable
from .IIdentifiable import IIdentifiable
from .INamed import INamed
from .IStringIdentifiable import IStringIdentifiable
from .ITrackable import ITrackable
from .IVersioned import IVersioned
from .MultiString import MultiString
