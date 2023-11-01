import importlib
from typing import Any, Optional, Tuple, Union

__author__ = "Aaron Tsang"
__version__ = "2023.10.31"
__all__ = (
    "parse",
    "find",
)


def parse(ref: str) -> Tuple[str, Optional[str]]:
    """
    Parse an object reference into module name and qualified name.

    The qualified name is ``None`` when the reference is of the form
     ``package.module``.

    :param ref: object reference
    :return: a tuple of module and qualified name.
    :raise ValueError: if the reference is invalid.
    """

    modname, colon, qualname = ref.partition(":")

    if not modname:
        raise ValueError("Empty module name")

    # remove prefixed dots in relative module
    stripped = modname.lstrip(".")
    if stripped and not all(s.isidentifier() for s in stripped.split(".")):
        raise ValueError(f"Bad object reference: {ref!r}")

    if not colon:
        # no colon => no qualname
        return modname, None

    if not qualname:
        raise ValueError("Missing qualname")

    if ":" in qualname:
        raise ValueError("More than one colon in object reference")

    if not all(s.isidentifier() for s in qualname.split(".")):
        raise ValueError(f"Bad object reference: {ref!r}")

    return modname, qualname


def find(
    ref: Union[str, Tuple[str, Optional[str]]],
    package: Optional[str] = None,
) -> Any:
    """
    Find the referenced object.

    :param ref: object reference string or :func:`.parse`. result.
    :param package: anchor when the module name is relative
    :raise ModuleNotFoundError: if the module cannot be imported
    :raise LookupError: if the qualified name is specified but cannot be found.
    """
    if isinstance(ref, str):
        modname, qualname = parse(ref)
    else:
        modname, qualname = ref

    module = importlib.import_module(modname, package)
    if qualname is None:
        return module

    result = module

    try:
        for name in qualname.split("."):
            result = getattr(result, name)
    except AttributeError:
        raise LookupError(ref) from None

    return result
