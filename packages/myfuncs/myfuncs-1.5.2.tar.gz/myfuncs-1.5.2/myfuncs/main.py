import base64 as b64
import inspect
import os
import platform
import random
import re
import string
import subprocess as subproc
import sys
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

ALPHANUMERIC_CHARS = string.ascii_letters + string.digits
USERNAME_ASCII_CHARS = ALPHANUMERIC_CHARS + '_-'


def nlprint(*args, **kwargs) -> None:
    """Identical to print() but also print()'s before and after"""
    print()
    print(*args, **kwargs)
    print()


def is_jwt(s: Union[str, bytes]) -> bool:
    """Check if a string is a valid JWT (JSON Web Token).
    Args:
        s (Union[str, bytes]): Input suspected jwt bytes or string.
    Returns:
        bool: True if the input is a valid JWT, False otherwise.
    """
    # If the input is bytes, try to decode it as UTF-8
    if isinstance(s, bytes):
        try:
            s = s.decode('utf-8')
        except UnicodeDecodeError:
            return False

    parts = s.split('.')

    # A valid JWT should have exactly three parts separated by dots
    if len(parts) != 3:
        return False

    try:
        for part in parts:
            # Ensure that the part has proper padding to be a valid base64 string
            while len(part) % 4 != 0:
                part += '='
            # Attempt to decode the part as base64
            b64.urlsafe_b64decode(part)
    except ValueError:
        return False
    return True


def is_jwt_str(*args, **kwargs) -> bool:
    """legacy func passing to is_jwt"""
    return is_jwt(*args, **kwargs)


def ranstr(
    min_length: int = 16,
    max_length: Optional[int] = None,
    chars: Iterable = ALPHANUMERIC_CHARS,
    as_generator: bool = False,
) -> Union[Generator, str]:
    """Generates str with random chars between min and max length
    Args:
        min_length (int) = 16: The length of the string.
        max_length (Optional[int]): The maximum length of the string.
            If None, min_length is used with no variance on ranstr len
        chars (Iterable = ALPHANUMERIC_CHARS): Characters used for random str
        as_generator (bool) = False: Return a generator instead of a string
    Returns:
        Generator | str: The random str or generator for random str
    """
    if max_length is None:
        _length = min_length
    else:
        _length = random.randint(min_length, max_length)

    if as_generator:
        return (random.choice(chars) for _ in range(_length))
    return ''.join(random.choice(chars) for _ in range(_length))


def runcmd(
    cmd: str, output: bool = True, *args, **kwargs
) -> Optional[List[str]]:
    """Runs a single command in the shell.
    Args:
        cmd (str): Str that will be treated as if pasted into shell
        output (bool) = True:
            equivalent to check=True text=True capture_output=True
    Returns:
        List[str] | None: output of cmd if output=True, None otherwise
    """
    if output:
        return subproc.run(
            cmd.split(),
            check=True,
            text=True,
            capture_output=True,
            *args,
            **kwargs,
        ).stdout.splitlines()
    else:
        subproc.run(
            cmd.split(),
            check=False,
            text=False,
            capture_output=False,
            *args,
            **kwargs,
        )


def get_terminal_width(default: int = 80) -> int:
    """Gets current terminal width or default 80 if not detectable"""
    try:
        return os.get_terminal_size().columns
    except OSError:
        return default


def print_middle(
    obj: any, char: str = '=', noprint: bool = False, *args, **kwargs
) -> str:
    """prints object str in middle of line of $chars based on terminal width
    passes *args/**kwargs to print()
    Args:
        obj (Any): The object whose string representation needs to be printed.
        char (str): Char used for line default '='
        noprint (bool) = False: If True, don't print, just return str
    """
    terminal_width = get_terminal_width()
    _obj = str(obj)

    padding = (terminal_width - len(_obj) - 2) // 2

    # not using fstring for backwards compatibility
    result = '%s %s %s' % (char * padding, _obj, char * padding)

    if not noprint:
        print(result, *args, **kwargs)
    return result


def print_columns(
    iterable: Iterable[str],
    separator: str = "  ",
    terminal_width: Optional[int] = None,
) -> List[str]:
    """Print a list of objects in columns based on the terminal width.
    Args:
        iterable (Iterable): The iterable to be printed.
        separator (str) = "  ": The separator to be used between columns.
        terminal_width (Optional[int]): The terminal width to be used.
    Returns:
        List[str]: The list of strings that were printed.
    """
    termwidth = terminal_width or get_terminal_width()

    objs = [str(obj) for obj in iterable]
    longest = max(len(obj) for obj in objs)

    printed = []

    curline = ""
    while objs:
        curobj = objs.pop(0)
        curobj += " " * (longest - len(curobj))
        curobj += separator

        if len(curline) + len(curobj) > termwidth:
            print(curline)
            printed.append(curline)
            curline = ""
        else:
            curline += curobj

    return printed


def objinfo(obj: Any) -> None:
    """Print information about an object."""
    terminal_width = get_terminal_width()

    obj_type = type(obj)
    obj_name = obj.__name__ if hasattr(obj, "__name__") else "N/A"
    obj_attrs = sorted(
        str(attr) for attr in dir(obj) if not callable(getattr(obj, attr))
    )
    obj_methods = sorted(
        str(method) for method in dir(obj) if callable(getattr(obj, method))
    )
    obj_doc = inspect.getdoc(obj) or "No documentation available."
    obj_scope = (
        "Local"
        if obj in inspect.currentframe().f_back.f_locals.values()
        else "Global"
    )
    obj_size = sys.getsizeof(obj)
    obj_mutability = "Mutable" if hasattr(obj, "__dict__") else "Immutable"
    obj_identity = id(obj)

    header = "{} ({})".format(obj_name, obj_type)
    subheader = (
        "Size: {}".format(obj_size),
        "Scope: {}".format(obj_scope),
        "Mutability: {}".format(obj_mutability),
        "Identity: {}".format(obj_identity),
    )
    nlprint(print_middle(header, noprint=True))
    print_columns(subheader)

    # not using fstring for old versions of python
    nlprint(print_middle("Attributes", "-", noprint=True))
    print_columns(obj_attrs)
    nlprint(print_middle("Methods", "-", noprint=True))
    print_columns(obj_methods)
    nlprint(print_middle("Documentation", "-", noprint=True))
    print(obj_doc)
    nlprint('-' * terminal_width)


def default_repr(
    obj: Any, transform: Optional[Callable] = None, *args, **kwargs
) -> str:
    """Return a string representation of a custom Python object.
    This representation is constructed such that the object can be
    reconstructed from the returned string, ideally. Complex objects
    may not be able to be reconstructed.
    Args:
        obj (Any): The input Python object.
        transform (Optional[Callable]): A function that will return the repr
            string with modifications. *args/**kwargs will be passed to this func
    Returns:
        str: The string representation of the object.
    """
    # If the object has a __dict__ attribute, use that
    if hasattr(obj, '__dict__'):
        attributes = ', '.join(
            "{}={}".format(key, repr(value))
            for key, value in obj.__dict__.items()
            if not hasattr(value, '__call__') and not str(key).startswith("_")
        )
    # Otherwise, use dir() to gather potential attributes
    else:
        if isinstance(obj, int):
            return 'int(%s)' % obj
        elif isinstance(obj, float):
            return 'float(%s)' % obj
        elif isinstance(obj, str):
            return 'str(%s)' % obj
        elif isinstance(obj, set):
            return 'set(%s)' % obj
        elif isinstance(obj, (list, tuple, dict)):
            return str(obj)

        attributes = ', '.join(
            "{}={}".format(attr, getattr(obj, attr))
            for attr in dir(obj)
            if not hasattr(obj, '__call__') and not str(attr).startswith('_')
        )

    if transform is not None:
        return transform(obj, *args, **kwargs)
    return "{}({})".format(obj.__class__.__name__, attributes)


def typed_evar(name: str, default: Optional[Any] = None):
    """Return an environment variable with an assumed type. Type from
    the default value, if provided, will be prioritized, otherwise
    the type will be inferred in order of: bool, int, float, str.
    Args:
        name (str): The name of the environment variable.
        default (Optional[Any]): The default value of the environment
            variable. The type of this value will be used to cast the
            environment variable value. If not provided, the type will
            be inferred from the environment variable value.
    """
    varval = os.environ.get(name)
    if varval is None:
        return default

    # use default's type
    if default is not None:
        vartype = type(default)

        # bool gets special treatment
        if vartype is bool:
            if varval.lower() in ('1', 'true'):
                return True
            elif varval.lower() in ('0', 'false', '-1'):
                return False
            else:
                raise ValueError(
                    "Invalid boolean value for environment variable %s: %s"
                    % (name, varval)
                )
        try:
            return vartype(varval)
        except:
            pass

    # otherwise assume type using a few simple types
    if varval.lower() in ('true', 'false'):
        return varval.lower() == 'true'

    for vartype in (int, float):
        try:
            return vartype(varval)
        except ValueError:
            continue

    return varval
