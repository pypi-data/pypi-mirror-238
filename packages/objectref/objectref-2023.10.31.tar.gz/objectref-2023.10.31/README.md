# objectref

objectref is a library to parse object references and find referenced objects.

## Notations

Object references are notations to locate modules or objects from the top level of a module.

```text
package.module
package.module:object.attr
```

The first form simply refers a module, while the second form an object in module.
It is also described in [here][1].

This library also supports relative object references (prefixed with dots).

[1]: https://packaging.python.org/en/latest/specifications/entry-points/#data-model

## Usage

* `find(ref: str, package: str | None = None) -> Any`

  The `find` function takes an object reference or `parse()` result,
  and returns the object pointed by the reference.

  The `package` argument must be set when the reference is relative.

  If qualified name is unspecified (the first form), the result is a module (`types.ModuleType` instance).

  `ModuleNotFoundError` is raised if the module cannot be found nor imported;
  `LookupError` if the object is not accessible from the top level of the module.

* `parse(ref: str) -> tuple[str, str | None]`

  The `parse` function takes an object reference,
  and results in a tuple of module name and qualified name.
  The qualified name would be `None` in first form.

  `ValueError` is raised if the reference is invalid.

## Example

```python
import os.path

import objectref

print(objectref.find("os.path") == os.path)  # True
print(objectref.find("os.path:join") == os.path.join)  # True
print(objectref.parse("os.path"))  # ("os.path", None)
print(objectref.parse("os.path:join"))  # ("os.path", "join")

```

## Entrypoint example

There are two main ways to execute a Python program.

* Run `python -m myapp.main` in shells, which executes the module as `__main__` under the hood.
  This relates to the first form of notation.

* Run `myapp` installed by pip. It is generated according to entrypoint defined in the project metadata
  (e.g. `myapp = myapp.main:main`).
  This requires the second form notation with callable objects.

Here is a code snippet to unify these two ways and start a program by its object reference.

```python
import objectref


def run(ref: str, package: str | None = None):
    modname, qualname = objectref.parse(ref)

    if qualname is None:
        # Use runpy to run a module with __name__ = "__main__"
        if modname.startswith("."):
            # runpy does not support relative module name.
            from importlib.util import resolve_name
            modname = resolve_name(modname, package)
        import runpy
        return runpy.run_module(modname, run_name="__main__")

    fn = objectref.find((modname, qualname), package)
    return fn()


if __name__ == "__main__":
    run("this")  # run the "this" module dynamically.

```
