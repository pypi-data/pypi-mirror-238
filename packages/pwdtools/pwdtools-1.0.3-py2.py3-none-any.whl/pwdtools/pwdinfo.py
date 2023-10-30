#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""password info"""

from __future__ import annotations

import getpass

from armour.gen.info import PasswordInfo

__version__: str = "1.0.0"


def main() -> int:
    """entry / main function"""

    print(PasswordInfo(getpass.getpass("( password, hidden ) ").encode()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
