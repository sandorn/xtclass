#!/usr/bin/env python
"""Core mixin classes for xtclass package."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


class MixinError(Exception):
    """Mixin相关错误.

    This exception is raised when there are issues with mixin operations,
    such as failed attribute access or invalid operations.
    """

    def __init__(self, message: str, original_error: Exception | None = None) -> None:
        """Initialize MixinError.

        Args:
            message: Error message describing the issue
            original_error: The original exception that caused this error
        """
        super().__init__(message)
        self.original_error = original_error
        self.message = message

    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.original_error:
            return f'{self.message} (Original error: {self.original_error})'
        return self.message


class ItemGetMixin:
    """提供下标访问([key])获取属性值的功能.

    通过__getitem__方法，允许对象使用字典风格的下标访问方式获取属性值。
    直接从实例的__dict__中获取值，如果键不存在则返回None。
    """

    def __getitem__(self, key: str) -> Any:
        """获取指定键的值.

        Args:
            key: 要获取的属性名

        Returns:
            属性值，如果不存在则返回None

        Raises:
            MixinError: 当获取属性时发生错误
        """
        try:
            return self.__dict__.get(key)
        except AttributeError as e:
            raise MixinError('Object has no __dict__ attribute', e) from e
        except Exception as e:
            raise MixinError(f"Failed to get item '{key}': {e}", e) from e


class ItemSetMixin:
    """提供下标访问([key])设置属性值的功能.

    通过__setitem__方法，允许对象使用字典风格的下标访问方式设置属性值。
    直接在实例的__dict__中设置键值对。
    """

    def __setitem__(self, key: str, value: Any) -> None:
        """设置指定键的值.

        Args:
            key: 要设置的属性名
            value: 要设置的属性值

        Raises:
            MixinError: 当设置属性时发生错误
        """
        try:
            self.__dict__[key] = value
        except AttributeError as e:
            raise MixinError('Object has no __dict__ attribute', e) from e
        except Exception as e:
            raise MixinError(f"Failed to set item '{key}': {e}", e) from e


class ItemDelMixin:
    """提供下标访问([key])删除属性的功能.

    通过__delitem__方法，允许对象使用字典风格的下标访问方式删除属性。
    直接从实例的__dict__中删除指定的键值对。
    """

    def __delitem__(self, key: str) -> None:
        """删除指定键的值.

        Args:
            key: 要删除的属性名

        Raises:
            MixinError: 当删除属性时发生错误
        """
        try:
            self.__dict__.pop(key, None)
        except AttributeError as e:
            raise MixinError('Object has no __dict__ attribute', e) from e
        except Exception as e:
            raise MixinError(f"Failed to delete item '{key}': {e}", e) from e


class ItemMixin(ItemGetMixin, ItemSetMixin, ItemDelMixin):
    """统一的字典风格访问Mixin."""

    def keys(self) -> list[str]:
        """返回所有键的列表."""
        return list(self.__dict__.keys())

    def values(self) -> list[Any]:
        """返回所有值的列表."""
        return list(self.__dict__.values())

    def items(self) -> list[tuple[str, Any]]:
        """返回所有键值对的列表."""
        return list(self.__dict__.items())


class AttrGetMixin:
    """提供属性访问功能，支持默认值."""

    def __getattr__(self, key: str) -> Any:
        """当属性不存在时返回默认值."""
        # 避免递归，直接返回None
        return None


class AttrSetMixin:
    """提供属性设置(cls.key = value)的功能.

    重写__setattr__方法，在设置属性值时记录日志，然后调用父类的方法完成实际设置。
    """

    def __setattr__(self, key: str, value: Any) -> None:
        """设置属性值并记录日志.

        Args:
            key: 要设置的属性名
            value: 要设置的属性值
        """
        super().__setattr__(key, value)  # 直接调用父类方法完成设置


class AttrDelMixin:
    """提供属性删除(del cls.key)的功能.

    重写__delattr__方法，在删除属性时记录日志，然后调用父类的方法完成实际删除。
    """

    def __delattr__(self, key: str) -> None:
        """删除属性并记录日志.

        Args:
            key: 要删除的属性名
        """
        super().__delattr__(key)  # 直接调用父类方法完成删除


class AttrMixin(AttrGetMixin, AttrSetMixin, AttrDelMixin):
    """组合了所有属性访问(cls.key)相关的功能.

    同时继承了AttrGetMixin、AttrSetMixin和AttrDelMixin，
    提供完整的属性操作支持(获取、设置、删除)，其中属性不存在时返回None。
    """

    pass


class GetSetDelMixin(ItemMixin, AttrMixin):
    """组合了下标操作和属性访问功能的混合类.

    同时继承了ItemMixin和AttrMixin，提供完整的字典风格下标操作([])
    和属性访问操作(.)的支持，包括获取、设置和删除。
    """

    pass


class ReDictMixin:
    """提供重新生成__dict__的功能.

    主要用于只读限制场景，通过get_dict方法重新构建实例的__dict__。
    提供了两个方法：get_dict_from_instance和get_dict_from_class，分别从实例和类层面收集属性。
    """

    def get_dict_from_instance(self) -> dict[str, Any]:
        """从实例层面收集所有非魔术方法和非可调用属性到__dict__.

        Returns:
            包含实例所有属性的字典
        """
        if not hasattr(self, '__dict__') or not self.__dict__:
            # 优化：使用更高效的方式收集属性，避免重复调用getattr
            attrs = {}
            for key in dir(self):
                if not key.startswith('__'):
                    try:
                        value = getattr(self, key)
                        if not callable(value):
                            attrs[key] = value
                    except AttributeError:
                        continue
            self.__dict__ = attrs
        return self.__dict__

    def get_dict_from_class(self) -> dict[str, Any]:
        """从类层面收集所有非魔术方法和非可调用属性到__dict__.

        Returns:
            包含类所有属性的字典
        """
        if not hasattr(self, '__dict__') or not self.__dict__:
            # 优化：直接从类字典中过滤，避免重复计算
            attrs = {}
            for key, value in self.__class__.__dict__.items():
                if not key.startswith('__') and not callable(value):
                    attrs[key] = value
            self.__dict__ = attrs

        return self.__dict__

    get_dict = get_dict_from_class


class IterMixin:
    """提供迭代功能的混合类.

    使继承该类的对象可以直接用于for循环，迭代其__dict__中的所有键值对。
    支持Python的Iterable接口。
    """

    def __iter__(self) -> Iterator[tuple[str, Any]]:
        """返回一个迭代器，用于迭代实例的所有属性."""
        yield from self.__dict__.items()


class ReprMixin(ReDictMixin):
    """提供更好的字符串表示形式的混合类.

    继承自ReDictMixin，重写__repr__方法，使对象在打印或转换为字符串时，
    以更易读的格式显示其所有属性。
    """

    def __repr__(self) -> str:
        """返回对象的字符串表示，包含所有属性.

        Returns:
            格式为"ClassName(attr1=value1, attr2=value2, ...)"的字符串
        """
        # 优化：缓存类名，避免重复访问
        class_name = self.__class__.__qualname__

        # 使用__dict__，如果为空则调用get_dict()
        dic = self.__dict__ or self.get_dict()

        # 优化：使用join而不是多次字符串拼接
        if not dic:
            return f'{class_name}()'

        # 构建格式为"ClassName(attr1=value1, attr2=value2, ...)"的字符串
        items = [f'{k}={v!r}' for k, v in dic.items()]
        return f'{class_name}({", ".join(items)})'
