# xtclass

[![PyPI version](https://img.shields.io/pypi/v/xtclass.svg)](https://pypi.org/project/xtclass/)
[![Python versions](https://img.shields.io/pypi/pyversions/xtclass.svg)](https://pypi.org/project/xtclass/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A collection of useful mixin classes for Python that add common functionality like dictionary-style access, attribute handling, and iteration support.

## Features

-   **Dictionary-style access**: Use `obj[key]` syntax to get/set/delete attributes
-   **Enhanced attribute handling**: Safe attribute access with default values
-   **Iteration support**: Iterate over object attributes like a dictionary
-   **Smart string representation**: Automatic `__repr__` with all attributes
-   **Metaclass magic**: Dynamic mixin application based on class attributes
-   **Utility classes**: Specialized classes like `SetOnceDict` for specific use cases

## Installation

```bash
pip install xtclass
```

## Quick Start

### Basic Usage

```python
from xtclass import BaseCls

class Person(BaseCls):
    def __init__(self, name, age):
        self.name = name
        self.age = age

# Create an instance
person = Person("Alice", 30)

# Dictionary-style access
print(person["name"])  # Alice
person["city"] = "New York"
print(person["city"])  # New York

# Attribute access with defaults
print(person.nonexistent)  # None (no AttributeError)

# Iteration
for key, value in person:
    print(f"{key}: {value}")

# Enhanced string representation
print(person)  # Person(name='Alice', age=30, city='New York')
```

### Using Individual Mixins

```python
from xtclass import ItemMixin, AttrMixin, IterMixin

class MyClass(ItemMixin, AttrMixin, IterMixin):
    def __init__(self):
        self.data = "test"

obj = MyClass()
obj["key"] = "value"  # Dictionary-style access
print(obj.nonexistent)  # None (safe attribute access)
for k, v in obj:  # Iteration
    print(f"{k}: {v}")
```

### Using the Metaclass

```python
from xtclass import MixinClsParent

class MyClass(MixinClsParent):
    MixinItem = True    # Enable dictionary-style access
    MixinAttr = True    # Enable safe attribute access
    MixinIter = True    # Enable iteration
    MixinRepr = True    # Enable enhanced string representation

    def __init__(self):
        self.value = 42

obj = MyClass()
print(obj["value"])  # 42
print(obj)  # MyClass(value=42)
```

### Utility Classes

```python
from xtclass import SetOnceDict

# Create a dictionary that only allows setting values once
sod = SetOnceDict()
sod["key"] = "value"
sod["key"] = "new_value"  # This won't change the value
print(sod["key"])  # "value"
```

## API Reference

### Mixin Classes

#### ItemMixin

Provides dictionary-style access (`obj[key]`) for getting, setting, and deleting attributes.

#### AttrMixin

Provides safe attribute access that returns `None` for non-existent attributes instead of raising `AttributeError`.

#### IterMixin

Makes objects iterable, allowing you to iterate over their attributes.

#### ReprMixin

Provides enhanced string representation showing all object attributes.

#### BaseCls

A convenience class that combines all common mixins (`AttrMixin`, `ItemMixin`, `IterMixin`, `ReprMixin`).

### Metaclass

#### MixinClsMeta

A metaclass that automatically applies mixins based on class attributes:

-   `MixinItem = True`: Apply `ItemMixin`
-   `MixinAttr = True`: Apply `AttrMixin`
-   `MixinIter = True`: Apply `IterMixin`
-   `MixinRepr = True`: Apply `ReprMixin`

#### MixinClsParent

A base class that uses `MixinClsMeta` for easy mixin application.

### Utility Classes

#### SetOnceDict

A dictionary-like class that only allows setting values once per key.

## Examples

### Configuration Object

```python
from xtclass import BaseCls

class Config(BaseCls):
    def __init__(self):
        self.debug = False
        self.timeout = 30

config = Config()

# Load from dictionary
config_data = {"debug": True, "host": "localhost"}
for key, value in config_data.items():
    config[key] = value

print(config)  # Config(debug=True, timeout=30, host='localhost')
```

### Data Container

```python
from xtclass import ItemMixin, IterMixin

class DataContainer(ItemMixin, IterMixin):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self[key] = value

data = DataContainer(name="test", value=123)
print(dict(data))  # {'name': 'test', 'value': 123}
```

## Development

### Setup

```bash
git clone https://github.com/sandorn/xtclass.git
cd xtclass
pip install -e .
```

### Testing

```bash
# Run tests
just test

# Run all quality checks
just qa

# Run tests with coverage
just coverage
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run quality checks: `just qa`
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyfeldroy/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
