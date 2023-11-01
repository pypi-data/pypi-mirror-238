import os.path
from typing import Optional

import pytest

import objectref

_ERROR = object()


@pytest.mark.parametrize(
    "ref,result",
    [
        # modname only
        ("mod", ("mod", None)),
        ("mod.", ValueError),  # empty part
        ("mod.sub", ("mod.sub", None)),
        ("mod.0sub", ValueError),  # bad modname
        # modname and qualname
        ("mod:", ValueError),  # colon with empty qualname
        ("mod:const", ("mod", "const")),
        ("mod:0const", ValueError),
        ("mod:const.", ValueError),
        ("mod:.const", ValueError),
        ("mod:const.attr", ("mod", "const.attr")),
        ("mod:.const.attr", ValueError),
        ("mod:const.attr.", ValueError),
        # relative modname
        (".mod", (".mod", None)),
        (".mod.sub", (".mod.sub", None)),
        ("..mod", ("..mod", None)),
        # relative modname and qualname
        (".:const", (".", "const")),
        # count(colon) > 1
        ("mod:const:", ValueError),
        ("mod:const:xxx", ValueError),
        ("", ValueError),  # empty reference
        (":", ValueError),  # colon only
        (" ", ValueError),  # bad identifier
        (":const", ValueError),  # missing module name
    ],
)
def test_parse(ref: str, result: object):
    if isinstance(result, type) and issubclass(result, BaseException):
        with pytest.raises(result):
            objectref.parse(ref)
    else:
        assert objectref.parse(ref) == result


@pytest.mark.parametrize(
    "ref,obj",
    [
        ("os", os),
        ("os.path", os.path),
        ("os.path:join", os.path.join),
        ("os.does_not_exist", ModuleNotFoundError),  # from importlib
        ("os.path:does_not_exist", LookupError),
    ],
)
def test_find_object(ref: str, obj: object):
    if isinstance(obj, type) and issubclass(obj, BaseException):
        with pytest.raises(obj):
            objectref.find(ref)
    else:
        assert objectref.find(ref) == obj


@pytest.mark.parametrize(
    "ref,pkg,obj",
    [
        (".path", "os", os.path),
        (".does_not_exist", "os", ModuleNotFoundError),  # from importlib
        (".:path.join", "os", os.path.join),
        (".:join", "os.path", os.path.join),
        (".:name", None, TypeError),  # from importlib
    ],
)
def test_find_object_with_package(ref: str, pkg: Optional[str], obj: object):
    if isinstance(obj, type) and issubclass(obj, BaseException):
        with pytest.raises(obj):
            objectref.find(ref, package=pkg)
    else:
        assert objectref.find(ref, package=pkg) == obj
