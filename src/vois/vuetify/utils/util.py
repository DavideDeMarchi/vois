import warnings
from typing import Callable, Dict, Any
import functools


def deprecation_class_warning(old_class_name: str):
    warnings.warn('DeprecationWarning: The {} class is deprecated, please use {}.'.format(old_class_name,
                                                                                          old_class_name.capitalize()),
                  stacklevel=2)


def deprecated_init_alias(**aliases: str) -> Callable:
    """Decorator for deprecated function and method arguments.

    Use as follows:

    @deprecated_alias(old_arg='new_arg')
    def myfunc(new_arg):
        ...

    """

    def deco(f: Callable):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            rename_kwargs(f.__name__, kwargs, aliases, args[0])
            return f(*args, **kwargs)

        return wrapper

    return deco


def rename_kwargs(func_name: str, kwargs: Dict[str, Any], aliases: Dict[str, str], obj=None):
    """Helper function for deprecating function arguments."""
    for alias, new in aliases.items():
        if alias in kwargs:
            if new in kwargs:
                raise TypeError(
                    f"{func_name} received both '{alias}' and '{new}' as arguments!"
                    f" '{alias}' is deprecated, use '{new}' instead."
                )
            warnings.warn(
                message=(
                    f"'{alias}' is deprecated as an argument to '{func_name}'; use"
                    f" '{new}' instead."
                ),
                category=DeprecationWarning,
                stacklevel=2,
            )

            deprecation_message = "Do not use it anymore! '{}' is deprecated as property; use '{}' instead".format(alias, new)

            def generic_getter(_obj):
                warnings.warn(
                    message=deprecation_message,
                    category=DeprecationWarning,
                    stacklevel=2,
                )
                return getattr(_obj, new)

            def generic_setter(_obj, val):
                warnings.warn(
                    message=deprecation_message,
                    category=DeprecationWarning,
                    stacklevel=2,
                )
                setattr(_obj, new, val)

            kwargs[new] = kwargs.pop(alias)
            if obj:
                setattr(obj.__class__, alias, property(fget=generic_getter, fset=generic_setter))
