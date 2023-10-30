#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""password generator"""

from __future__ import annotations

import string
import sys
from optparse import Option, OptionParser, make_option
from typing import Any, Dict, Final, NoReturn, Optional, Tuple

from armour.gen import gen, info

__version__: str = "1.0.0"

MOD_LEN_DELTA: int = 2


def opt_bytes(
    option: Option,
    _: str,
    value: str,
    parser: OptionParser,
) -> None:
    """optional bytes type"""

    if option.dest is None:
        raise ValueError("no `dest` specified")

    setattr(parser.values, option.dest, value.encode("utf-8"))


EXCLUDE_ARGS: Final[Tuple[str, ...]] = (
    "modify",
    "iters",
    "unicode",
    "end",
    "debug",
    "count",
    "yank",
)

STATE: Dict[str, Any] = {}

OPTIONS: OptionParser = OptionParser(
    version=__version__,
    description="generate secure passwords based off your criteria",
    epilog="values of -1 for integers and floats show 'any'",
    option_list=(
        make_option(
            "-B",
            "--byteset",
            action="callback",
            type="string",
            help="the byteset / alphabet",
            dest="byteset",
            callback=opt_bytes,
            default=string.printable.strip().encode(),
        ),
        make_option(
            "-L",
            "--length",
            action="store",
            type="long",
            dest="length",
            help="the minimum length of the password",
            default=128,
        ),
        make_option(
            "-l",
            "--lower",
            action="store",
            type="long",
            dest="min_lower",
            help="the minimum count of lowercase letters in the password",
            default=gen.D,
        ),
        make_option(
            "-u",
            "--upper",
            action="store",
            type="long",
            dest="min_upper",
            help="the minimum count of uppercase letters in the password",
            default=gen.D,
        ),
        make_option(
            "-n",
            "--numbers",
            action="store",
            type="long",
            dest="min_numbers",
            help="the minimum count of numerical characters in the password",
            default=gen.D,
        ),
        make_option(
            "-s",
            "--special",
            action="store",
            type="long",
            dest="min_special",
            help="the minimum count of special characters in the password",
            default=gen.D,
        ),
        make_option(
            "-a",
            "--alphabet",
            action="store",
            type="long",
            dest="min_alphabet",
            help="the minimum length of the password alphabet",
            default=gen.D,
        ),
        make_option(
            "-q",
            "--sequences",
            action="store",
            type="long",
            dest="max_sequences",
            help="the maximum count of sequences in the password",
            default=gen.D,
        ),
        make_option(
            "-p",
            "--patterns",
            action="store",
            type="long",
            dest="max_common_patterns",
            help="the maximum count of common patterns in the password",
            default=gen.D,
        ),
        make_option(
            "-e",
            "--entropy",
            action="store",
            type="float",
            dest="min_entropy",
            help="the minimum entropy of the password",
            default=gen.D,
        ),
        make_option(
            "-t",
            "--strength",
            action="store",
            type="float",
            dest="min_strength",
            help="the minimum strength of the password",
            default=gen.D,
        ),
        make_option(
            "-w",
            "--weakness",
            action="store",
            type="float",
            dest="max_weakness",
            help="the maximum weakness of the password",
            default=gen.D,
        ),
        make_option(
            "-c",
            "--actual-strength",
            action="store",
            type="float",
            dest="min_actual_strength",
            help="the minimum actual strength of the password",
            default=gen.D,
        ),
        make_option(
            "-P",
            "--passes",
            action="store",
            type="long",
            dest="max_passes",
            help="the minimum passes of generation",
            default=1024,
        ),
        make_option(
            "-M",
            "--no-modify",
            action="store_false",
            dest="modify",
            help="do not modify the criteria to match it better if no pw is generated",
            default=True,
        ),
        make_option(
            "-I",
            "--iters",
            action="store",
            type="long",
            dest="iters",
            help="how many times to try to generate a password",
            default=32,
        ),
        make_option(
            "-U",
            "--unicode",
            action="store",
            type="string",
            dest="unicode",
            help="unicode range for the password in a format `from,to`",
            default=None,
        ),
        make_option(
            "-E",
            "--end",
            action="store",
            type="string",
            dest="end",
            help="password line ending when displaying",
            default=b"\n",
        ),
        make_option(
            "-D",
            "--debug",
            action="store_true",
            dest="debug",
            help="print debug output",
            default=False,
        ),
        make_option(
            "-C",
            "--count",
            action="store",
            type="long",
            dest="count",
            help="how many passwords to generate",
            default=1,
        ),
        make_option(
            "-Y",
            "--yank",
            action="store_true",
            dest="yank",
            help="yank password to clipboard",
            default=False,
        ),
    ),
)


def log(msg: str) -> None:
    """log a message"""

    if STATE["debug"]:
        print(f" * {msg}", file=sys.stderr)


def err(msg: str) -> NoReturn:
    """log a message"""

    print(f" !! ERROR : {msg}", file=sys.stderr)
    sys.exit(1)


def check_kwargs(kwargs: Dict[str, Any]) -> None:
    """checks if kwargs are valid"""

    assert kwargs["length"] > 0, "`length` is too small"
    assert kwargs["max_passes"] > 0, "`max_passes` is too small"


def update_kwargs(kwargs: Dict[str, Any]) -> None:
    """update kwargs based off the state"""

    if STATE["unicode"]:
        try:
            from_b, to_b = tuple(map(int, STATE["unicode"].split(",", maxsplit=1)))

            assert 256 >= from_b >= 0, "invalid `from` range"
            assert 256 >= to_b >= 0, "invalid `to` range"
            assert to_b > from_b, "invalid `from-to` range"
        except Exception as e:
            err(f"invalid unicode range : {e}")

        log(f"updating byteset to be from {from_b} to {to_b} byte range")

        kwargs["byteset"] = bytes(range(from_b, to_b))


def gen_pwdgen(**kwargs: Any) -> gen.PwGenerator:
    """generate password based off the cli"""
    return gen.PwGenerator(**{k: v for k, v in kwargs.items() if k not in EXCLUDE_ARGS})


def gen_pw(pgen: gen.PwGenerator) -> Optional[bytes]:
    """generate password based off the cli"""

    pw: Optional[info.PasswordInfo]

    for idx in range(STATE["iters"]):
        log(f"generating password #{idx}")

        if (pw := pgen.gen()) is not None:
            log("generated password")
            log("\n   ".join(str(pw).splitlines()))
            return pw.pw

        if STATE["modify"]:
            if pgen.byteset is not None:
                pgen.byteset += bytes([pgen.rand.choice(pgen.byteset)])
                log(f"added byte {chr(pgen.byteset[-1])!r} to the byteset")

            pgen.length += MOD_LEN_DELTA
            log(f"password length = {pgen.length}")

    log(f"could not generate a good password after {STATE['iters']} tries")

    return None


def main(kwargs: Optional[Dict[str, Any]] = None) -> int:
    """entry / main function"""

    if kwargs is None:
        kwargs = OPTIONS.parse_args(sys.argv)[0].__dict__

    if kwargs["yank"]:
        try:
            import pyperclip  # type: ignore
        except ImportError:
            err(
                "( pip ) install ( --upgrade --user --break-system-packages ) \
`pyperclip` for --yank / -Y support"
            )

    try:
        check_kwargs(kwargs)
    except Exception as e:
        err(f"invalid arguments : {e}")

    STATE.update(kwargs)
    update_kwargs(kwargs)

    pgen: gen.PwGenerator = gen_pwdgen(**kwargs)

    for _ in range(STATE["count"]):
        pw: Optional[bytes] = gen_pw(pgen)

        if pw is None:
            err("no password that matches your criteria")

        if kwargs["yank"]:
            pyperclip.copy(pw.decode("latin-1"))  # type: ignore
            log("copied the first password to clipboard")
            break

        sys.stdout.buffer.write(pw + kwargs["end"])
        sys.stdout.buffer.flush()
        sys.stdout.flush()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
