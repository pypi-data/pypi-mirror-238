#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""password info based on zxcvbn"""

from __future__ import annotations

import sys
from getpass import getpass
from typing import Any, Tuple

import zxcvbn  # type: ignore

__version__: str = "1.0.0"


SCORE_STRINGS: Tuple[str, ...] = (
    "very bad",
    "bad",
    "not good",
    "good",
    "strong",
)


def log(message: str, header: str = "WARNING") -> None:
    """log a message"""

    sys.stderr.write(f" * {header}: {message}\n")
    sys.stderr.flush()


def main() -> int:
    """entry / main function"""

    password = getpass("( password, hidden ) ")

    stats: Any = zxcvbn.zxcvbn(password)
    crack: Any = stats["crack_times_seconds"]

    print(
        f"""
count of guesses            {stats['guesses']}
count of sequences          {len(stats['sequence'])}
crack times in seconds
    online, throttling, 100 hps     {crack['online_throttling_100_per_hour']}
    online, no throttling, 10 hps   {crack['online_no_throttling_10_per_second']}
    offline, slow, 1e4 hps          {crack['offline_slow_hashing_1e4_per_second']}
    offline, fast, 1e10 hps         {crack['offline_fast_hashing_1e10_per_second']}
score                       {SCORE_STRINGS[stats['score']]} ( {stats['score']} )
""".strip()
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
