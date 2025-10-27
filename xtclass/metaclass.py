# !/usr/bin/env python
"""Metaclass functionality for xtclass package."""

from __future__ import annotations

from typing import Any, ClassVar

from .mixins import AttrMixin, ItemMixin, IterMixin, ReprMixin


class MixinClsMeta(type):
    """智能元类，根据类属性动态选择并应用相应的Mixin类.

    该元类通过检查类定义中的Mixin*属性，自动将对应的Mixin类添加到基类列表中。
    支持的Mixin属性包括：MixinAttr、MixinItem、MixinIter、MixinRepr。

    本实现结合了MethodClsMeta的优点，包括避免重复添加Mixin类，
    同时优化了基类列表构建策略，避免MRO冲突问题。

    示例用法:
    ```python
    class BaseClsMeta(metaclass=MixinClsMeta):
        MixinAttr = True  # 启用属性访问支持
        MixinItem = True  # 启用下标操作支持
        MixinIter = True  # 启用迭代支持
        MixinRepr = True  # 启用友好的字符串表示支持
    ```
    """

    # 预定义Mixin映射
    MIXIN_MAP: ClassVar[dict[str, Any]] = {
        'MixinItem': ItemMixin,
        'MixinAttr': AttrMixin,
        'MixinIter': IterMixin,
        'MixinRepr': ReprMixin,
    }

    def __new__(cls, name: str, bases: tuple[type, ...], dct: dict[str, Any], **kwds: Any) -> type:
        """创建新的类对象，并根据类属性添加相应的Mixin类.

        Args:
            name: 要创建的类名
            bases: 原始基类元组
            dct: 类的属性字典
            **kwds: 额外的关键字参数

        Returns:
            创建的新类
        """
        # 收集需要添加的Mixin类
        mixin_classes = []
        for mixin_key, mixin_class in cls.MIXIN_MAP.items():
            if dct.get(mixin_key):
                mixin_classes.append(mixin_class)

        # 优化基类列表构建
        new_bases = list(bases)
        existing_mixins = {base for base in bases if base in cls.MIXIN_MAP.values()}

        for mixin_cls in mixin_classes:
            if mixin_cls not in existing_mixins:
                new_bases.append(mixin_cls)

        return super().__new__(cls, name, tuple(new_bases), dct)


class MixinConfig:
    """Mixin配置类."""

    DEFAULT_MIXINS: ClassVar[dict[str, Any]] = {
        'item': ItemMixin,
        'attr': AttrMixin,
        'iter': IterMixin,
        'repr': ReprMixin,
    }

    @classmethod
    def get_mixins(cls, config: dict[str, bool]) -> list[type]:
        """根据配置获取Mixin类列表."""
        return [mixin for key, mixin in cls.DEFAULT_MIXINS.items() if config.get(key)]


class MixinClsParent(metaclass=MixinClsMeta):
    """可直接继承的Mixin功能基类.

    该类结合了MixinClsMeta元类，提供更简洁的使用方式。
    通过设置类属性控制启用哪些Mixin功能，实现"混入继承"。

    示例用法:
    ```python
    class MyClass(MixinClsParent):
        MixinAttr = True  # 启用属性访问支持
        MixinItem = True  # 启用下标操作支持
    ```

    这样MyClass就直接继承了MixinClsParent，并且根据设置的类属性自动获得相应的Mixin功能。
    """

    pass
