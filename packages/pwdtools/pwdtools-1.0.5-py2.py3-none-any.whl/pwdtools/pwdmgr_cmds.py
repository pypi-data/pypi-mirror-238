#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pwdmgr base commands"""

import multiprocessing as mp
from abc import ABC
from sys import exit as sys_exit
from typing import NoReturn

from . import pwdgen, pwdinfo, pwdzxc, util
from .pwdmgr_clipboard import clipboard_clear


class Cmds(ABC):
    """function eq to 'external' cmds"""

    def cmd_help(self) -> int:
        """print help"""

        for cmd in dir(self):
            if cmd[:4] == "cmd_":
                util.log(
                    f"{cmd[4:]} -- {getattr(self, cmd).__doc__ or 'no help provided'}",
                )

        return 0

    def cmd_gen(self, *argv: str) -> int:
        """runs `pwdgen`"""

        p: mp.Process = mp.Process(
            target=lambda: pwdgen.main(
                pwdgen.OPTIONS.parse_args(list(argv))[0].__dict__,
            ),
        )
        p.start()
        p.join()

        return p.exitcode or 0

    def cmd_info(self) -> int:
        """runs `pwdinfo`"""

        p: mp.Process = mp.Process(target=pwdinfo.main)
        p.start()
        p.join()

        return p.exitcode or 0

    def cmd_zxc(self) -> int:
        """runs `pwdzxc`"""

        p: mp.Process = mp.Process(target=pwdzxc.main)
        p.start()
        p.join()

        return p.exitcode or 0

    def cmd_exit(self) -> NoReturn:
        """exit"""
        clipboard_clear()
        sys_exit(0)

    def cmd_c(self) -> int:
        """clear clipboard"""
        clipboard_clear()
        return 0

    def cmd_cc(self) -> int:
        """clear screen"""
        print("\033[H\033[J", end="")
        return 0
