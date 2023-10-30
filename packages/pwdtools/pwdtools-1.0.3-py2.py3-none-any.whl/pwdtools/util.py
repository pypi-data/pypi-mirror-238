#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""utils"""

from __future__ import annotations

import sys
from getpass import getpass
from typing import Any, Callable, Optional

import pyperclip  # type: ignore

try:
    import readline
except ImportError:
    readline: Any = None  # type: ignore


def log(msg: str, padding: str = "") -> None:
    """log a message"""
    print(f"{padding} * {msg}", file=sys.stderr)
    sys.stderr.flush()


def err(msg: str) -> int:
    """log an error"""

    print(f" err : {msg}", file=sys.stderr)
    sys.stderr.flush()
    return 1


def _inp(
    input_fn: Callable[[str], str],
    prompt: str,
    default: Any = "",
    t: Callable[[str], Any] = str,
) -> Any:
    """get input"""

    if default is not None:
        default = str(default)

    if default and readline:

        def hook() -> None:
            readline.insert_text(default)
            readline.redisplay()

        readline.set_pre_input_hook(hook)

    while True:
        try:
            user_input: str = input_fn(f"( {prompt} ) ")
        except KeyboardInterrupt:
            print()
            continue
        except EOFError:
            sys.exit(0)

        try:
            r: Any = t(user_input)
            if readline:
                readline.set_pre_input_hook()
            return r
        except Exception:
            continue


def sinp(
    prompt: str,
    default: Any = None,
    t: Callable[[str], Any] = str,
) -> Any:
    """get secret input and convert"""
    return _inp(getpass, f"{prompt}, hidden", default, t)


def inp(
    prompt: str,
    default: Any = None,
    t: Callable[[str], Any] = str,
) -> Any:
    """get secret input and convert"""
    return _inp(input, prompt, default, t)


def inp_range(
    prompt: str,
    min_r: int,
    max_r: int,
    default: Optional[int] = None,
) -> int:
    """get input in range"""

    r: Optional[int] = None

    while r is None or r < min_r or r > max_r:
        r = inp(f"{prompt} -- from {min_r} to {max_r}", default, int)

    return r


def yn(prompt: str, default: str = "y") -> bool:
    """yes / no"""
    return (inp(f"{prompt} ? [yn]", default) + default).lower()[0] == "y"


def cp(data: bytes, display: bool = True) -> None:
    """copy to clipboard"""

    try:
        pyperclip.copy(data.decode())  # type: ignore
    except Exception:
        if display and yn("clipboard unavailable, display", "n"):
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()
            sys.stdout.flush()
            print()
