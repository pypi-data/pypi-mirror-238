#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pwdmgr clipboard"""

from threading import Thread
from time import sleep
from typing import List

from .util import cp, log

clip: List[int] = [0, False]


def clipboard_cp(data: bytes) -> None:
    """copy to clipboard"""

    clipboard_timer()
    cp(data, False)
    clipboard_reset()


def clipboard_clear(logging: bool = True) -> None:
    """clear clipboard"""

    if logging:
        log("clearing clipboard")

    cp(b"", False)
    clip[0] = 0


def clipboard_timer() -> None:
    """start a clipboard timer"""

    if clip[1]:
        return

    def worker() -> None:
        """worker thread"""

        log("started clipboard worker thread")

        while True:
            sleep(1)

            if clip[0] <= 0:
                continue

            clip[0] -= 1

            if clip[0] <= 0:
                clipboard_clear(False)

    Thread(target=worker, daemon=True).start()
    clip[1] = True


def clipboard_reset() -> None:
    """reset clipboard"""
    log("resetting clipboard timer to 30 s")
    clip[0] = 30
