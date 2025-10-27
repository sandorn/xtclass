# !/usr/bin/env python
"""Examples demonstrating xtclass usage."""

from __future__ import annotations

from xtclass import BaseCls, MixinClsParent, SetOnceDict


def basic_usage_example():
    """Demonstrate basic usage of BaseCls."""
    print('=== Basic Usage Example ===')

    class Person(BaseCls):
        def __init__(self, name, age):
            self.name = name
            self.age = age

    # Create an instance
    person = Person('Alice', 30)

    # Dictionary-style access
    print(f'Name: {person["name"]}')
    person['city'] = 'New York'
    print(f'City: {person["city"]}')

    # Attribute access with defaults
    print(f'Nonexistent attribute: {person.nonexistent}')

    # Iteration
    print('All attributes:')
    for key, value in person:
        print(f'  {key}: {value}')

    # Enhanced string representation
    print(f'String representation: {person}')
    print()


def metaclass_example():
    """Demonstrate metaclass usage."""
    print('=== Metaclass Example ===')

    class Config(MixinClsParent):
        MixinItem = True  # Enable dictionary-style access
        MixinAttr = True  # Enable safe attribute access
        MixinIter = True  # Enable iteration
        MixinRepr = True  # Enable enhanced string representation

        def __init__(self):
            self.debug = False
            self.timeout = 30

    config = Config()

    # Load from dictionary
    config_data = {'debug': True, 'host': 'localhost', 'port': 8080}
    for key, value in config_data.items():
        config[key] = value

    print(f'Config: {config}')
    print(f'Debug mode: {config.debug}')
    print(f'Host: {config["host"]}')
    print()


def set_once_dict_example():
    """Demonstrate SetOnceDict usage."""
    print('=== SetOnceDict Example ===')

    # Create a dictionary that only allows setting values once
    sod = SetOnceDict()

    # First set should work
    sod['database_url'] = 'postgresql://localhost:5432/mydb'
    print(f'Database URL: {sod["database_url"]}')

    # Second set should be ignored
    sod['database_url'] = 'mysql://localhost:3306/mydb'
    print(f'Database URL after second set: {sod["database_url"]}')

    # Setting None should work
    sod['api_key'] = None
    print(f'API Key: {sod["api_key"]}')

    # Setting a new value after None should work
    sod['api_key'] = 'secret-key-123'
    print(f'API Key after setting value: {sod["api_key"]}')
    print()


def data_container_example():
    """Demonstrate data container usage."""
    print('=== Data Container Example ===')

    from xtclass import ItemMixin, IterMixin

    class DataContainer(ItemMixin, IterMixin):
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                self[key] = value

        def to_dict(self):
            """Convert to regular dictionary."""
            return dict(self)

        def update(self, other_dict):
            """Update with another dictionary."""
            for key, value in other_dict.items():
                self[key] = value

    # Create data container
    data = DataContainer(name='test', value=123, active=True)

    # Add more data
    data['description'] = 'Test data container'
    data.update({'category': 'example', 'priority': 'high'})

    print(f'Data container: {data}')
    print(f'As dictionary: {data.to_dict()}')
    print()


def configuration_manager_example():
    """Demonstrate configuration manager usage."""
    print('=== Configuration Manager Example ===')

    class ConfigManager(BaseCls):
        def __init__(self, config_file=None):
            self.config_file = config_file
            self.load_defaults()
            if config_file:
                self.load_from_file(config_file)

        def load_defaults(self):
            """Load default configuration."""
            defaults = {
                'debug': False,
                'log_level': 'INFO',
                'max_connections': 100,
                'timeout': 30,
            }
            for key, value in defaults.items():
                self[key] = value

        def load_from_file(self, filename):
            """Simulate loading from file."""
            # In real implementation, this would read from file
            file_config = {
                'debug': True,
                'log_level': 'DEBUG',
                'database_url': 'sqlite:///app.db',
            }
            for key, value in file_config.items():
                self[key] = value

        def get(self, key, default=None):
            """Get configuration value with default."""
            return self[key] if key in self.keys() else default

        def set(self, key, value):
            """Set configuration value."""
            self[key] = value

        def show_config(self):
            """Display current configuration."""
            print('Current configuration:')
            for key, value in sorted(self.items()):
                print(f'  {key}: {value}')

    # Create configuration manager
    config = ConfigManager('config.json')

    # Show configuration
    config.show_config()

    # Get with default
    print(f'Cache size: {config.get("cache_size", 1000)}')

    # Set new value
    config.set('cache_size', 2000)
    print(f'Updated cache size: {config["cache_size"]}')
    print()


if __name__ == '__main__':
    basic_usage_example()
    metaclass_example()
    set_once_dict_example()
    data_container_example()
    configuration_manager_example()
