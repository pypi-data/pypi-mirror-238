#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""password manager"""

from __future__ import annotations

import sys
from typing import Any, List

import armour.pdb.header

from . import pwdmgr_home, util
from .pwdmgr_clipboard import clip, clipboard_clear, clipboard_timer

try:
    import readline
except ImportError:
    readline: Any = None  # type: ignore


__version__: str = "1.0.0"


def main() -> int:
    """entry / main function"""

    if len(sys.argv) >= 3:
        try:
            return pwdmgr_home.HomeCmds().cmd_open(sys.argv[1], sys.argv[2])
        except Exception as e:
            return util.err(f"failed to open the db : {e}")

    clipboard_timer()
    print(f"welcome to pwdmgr v{__version__} for pDB {armour.pdb.header.VERSION}\n")

    if readline:
        readline.parse_and_bind("tab: complete")
        readline.set_history_length(-1)

    ex: int = 0
    cmds: pwdmgr_home.HomeCmds = pwdmgr_home.HomeCmds()

    while True:
        try:
            cmd: str = input(f"<{clip[0]}>[{ex}]> ")
        except EOFError:
            print()
            clipboard_clear()
            return ex
        except KeyboardInterrupt:
            print("\n")
            continue

        if not (cmd := cmd.strip()):
            print()
            continue

        argv: List[str] = cmd.split()

        if (cmd_fn := getattr(cmds, f"cmd_{argv[0]}", None)) is None:
            util.log(f"unkown command {argv[0]!r}\n")
            continue

        try:
            ex = cmd_fn(*argv[1:])
        except Exception as e:
            ex = util.err(str(e))
        finally:
            print()


if __name__ == "__main__":
    raise SystemExit(main())
