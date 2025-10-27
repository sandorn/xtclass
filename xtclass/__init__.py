# !/usr/bin/env python
"""xtclass - A collection of useful mixin classes for Python.

This package provides a set of mixin classes that add common functionality
to Python classes, including dictionary-style access, attribute handling,
iteration support, and more.
"""

from __future__ import annotations

# Import metaclass functionality
from .metaclass import MixinClsMeta, MixinClsParent, MixinConfig

# Import all mixin classes
from .mixins import AttrDelMixin, AttrGetMixin, AttrMixin, AttrSetMixin, GetSetDelMixin, ItemDelMixin, ItemGetMixin, ItemMixin, ItemSetMixin, IterMixin, MixinError, ReDictMixin, ReprMixin

# Import utility classes
from .utils import SetOnceDict


# Convenience base class that combines all common mixins
class BaseCls(AttrMixin, ItemMixin, IterMixin, ReprMixin):
    """Base class with all common mixin functionality.

    This class combines:
    - AttrMixin: Attribute access with default values
    - ItemMixin: Dictionary-style item access
    - IterMixin: Iteration over attributes
    - ReprMixin: Enhanced string representation
    """

    pass


# Public API
__all__ = [
    # Mixin classes
    'AttrDelMixin',
    'AttrGetMixin',
    'AttrMixin',
    'AttrSetMixin',
    'GetSetDelMixin',
    'ItemDelMixin',
    'ItemGetMixin',
    'ItemMixin',
    'ItemSetMixin',
    'IterMixin',
    'ReDictMixin',
    'ReprMixin',
    # Metaclass functionality
    'MixinClsMeta',
    'MixinClsParent',
    'MixinConfig',
    # Utility classes
    'SetOnceDict',
    # Base class
    'BaseCls',
    # Exceptions
    'MixinError',
]

# Package metadata
__version__ = '0.1.0'
__author__ = 'sandorn'
__email__ = 'sandorn@live.cn'
__description__ = 'A collection of useful mixin classes for Python'
