#!/usr/bin/env python
"""Utility classes for xtclass package."""

from __future__ import annotations

from typing import Any


class SetOnceDict:
    """限制下标[key]赋值的字典类.

    该类实现了一种特殊的字典，其中键值对只能被设置一次(当键不存在或值为None时)。
    主要特点是通过内部的_dict字典存储数据，且对属性访问(如obj.key)无效，只支持下标访问。
    """

    __slots__ = ('_dict',)  # 限制实例只能有_dict属性，优化内存使用

    def __init__(self) -> None:
        """初始化SetOnceDict实例.

        创建一个空的内部字典用于存储键值对。
        """
        self._dict: dict[Any, Any] = {}

    def __setitem__(self, key: str, value: Any) -> None:
        """设置指定键的值，但仅当键不存在或当前值为None时允许设置.

        Args:
            key: 要设置的键
            value: 要设置的值

        注意：如果键已存在且值不为None，则记录日志但不覆盖原有值。
        """
        if key in self._dict and self._dict[key] is not None:
            return
        self._dict[key] = value

    def __getitem__(self, key: str) -> Any:
        """获取指定键的值.

        Args:
            key: 要获取的键

        Returns:
            键对应的值

        Raises:
            KeyError: 如果键不存在
        """
        return self._dict[key]

    def __repr__(self) -> str:
        """返回对象的字符串表示.

        Returns:
            内部字典的字符串表示
        """
        return repr(self._dict)
