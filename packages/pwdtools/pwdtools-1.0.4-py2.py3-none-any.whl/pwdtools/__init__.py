#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pwdtools -- tools for password generation, management and checking"""

from __future__ import annotations

from typing import Tuple

from . import pwdgen, pwdinfo, pwdmgr, pwdzxc

__version__: str = "1.0.4"
__all__: Tuple[str, ...] = (
    "__version__",
    "pwdgen",
    "pwdinfo",
    "pwdmgr",
    "pwdzxc",
)
