#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pwdmgr home mode commands"""

from __future__ import annotations

import os
from typing import Optional

import armour

from . import util
from .pwdmgr_clipboard import clip, clipboard_timer
from .pwdmgr_cmds import Cmds
from .pwdmgr_pdb import PdbCmds


class HomeCmds(Cmds):
    """home mode commands"""

    def cmd_new(self, name: str) -> int:
        """create a new database"""

        db: str = f"{name}.pdb"
        slt: str = f"{name}.slt"
        pwp: Optional[str] = None

        if os.path.exists(db) or os.path.exists(slt):
            return util.err(
                f"database file {db!r} and / or salt file {slt!r} already exists",
            )

        util.log(f"{db = }, {slt = }")

        pw: bytes = util.sinp("database password").encode()

        if not pw and not util.yn(
            "are you sure that you want to create a database with an empty "
            "password ( will generate one if no )",
            "n",
        ):
            pwp = f"{name}.pwd-with-slt-and-pdb"[-255:]

            pw_info: Optional[
                armour.gen.info.PasswordInfo
            ] = armour.gen.gen.PwGenerator(length=4096).gen()

            pw = armour.crypt.RAND.randbytes(4096) if pw_info is None else pw_info.pw

        slen: int = util.inp(
            "how big should your salt be ( anything below 128 is not sufficient )",
            2048,
            int,
        )

        if slen < 128:
            slen = 128
            util.log(f"salt length too insecure, set the salt length to {slen}")

        util.log("creating a new db")

        p: armour.pdb.header.PdbHeader = armour.pdb.header.PdbHeader.empty(
            password=pw,
            salt=armour.crypt.RAND.randbytes(slen),
        )

        util.log("pick a hash id")

        for hid, h in enumerate(armour.crypt.HASHES):
            util.log(f"{hid} -- {h.name}", "    ")

        p.hash_id = util.inp_range(
            "hash id ( lower = more secure )",
            0,
            len(armour.crypt.HASHES) - 1,
            p.hash_id,
        )

        p.zstd_comp_lvl = util.inp_range(
            "compression level",
            1,
            armour.pdb.header.ZSTD_MAX_COMPRESSION,
            p.zstd_comp_lvl,
        )

        p.hash_salt_len = util.inp_range(
            "hash salt length",
            1,
            255,
            p.hash_salt_len,
        )

        p.kdf_passes = util.inp_range(
            "kdf generation passes",
            2**8,
            (2**32) - 1,
            p.kdf_passes,
        )

        p.sec_crypto_passes = util.inp_range(
            "secure cryptography passes",
            1,
            (2**16) - 1,
            p.sec_crypto_passes,
        )

        p.isec_crypto_passes = util.inp_range(
            "insecure cryptography passes",
            1,
            (2**16) - 1,
            p.isec_crypto_passes,
        )

        p.aes_crypto_passes = util.inp_range(
            "AES cryptography passes",
            1,
            (2**16) - 1,
            p.aes_crypto_passes,
        )

        util.log("encrypting database")

        p.encrypt()

        util.log("dumping database")

        db_bin: bytes = p.to_pdb()

        with open(db, "wb") as fp:
            fp.write(db_bin)

        with open(slt, "wb") as fp:
            fp.write(p.salt)

        if pwp is not None:
            with open(pwp, "wb") as fp:
                util.log(f"dumping password to {fp.name}")
                fp.write(pw)

        util.log(
            f"keep {db!r} and {slt!r} safe and do not forget your password, "
            "you will use all of those to authenticate"
        )

        return 0

    def cmd_open(self, dbp: str, salt: str) -> int:
        """open a database"""

        if not all(map(os.path.exists, (dbp, salt))):
            return util.err(
                f"database file {dbp!r} and / or salt file {salt!r} does not exist",
            )

        util.log("loading database and salt")

        with open(dbp, "rb") as fp:
            db: bytes = fp.read()

        with open(salt, "rb") as fp:
            slt: bytes = fp.read()

        util.log("decrypting")

        p: armour.pdb.header.PdbHeader = armour.pdb.header.PdbHeader.from_db(
            db,
            util.sinp("database password").encode(),
            slt,
        )

        clipboard_timer()

        print("\nentered pdb mode\n")

        ex: int = 0
        cmds: PdbCmds = PdbCmds(p, dbp)

        while True:
            try:
                cmd: str = input(
                    f"{'*' if cmds.modified else ''}<{clip[0]}>[{ex}]\
({os.path.basename(dbp)}:{os.path.basename(salt)})> "
                )
            except EOFError:
                print()

                if cmds.modified and util.yn("commit changes"):
                    cmds.cmd_commit()

                return ex
            except KeyboardInterrupt:
                print("\n")
                continue

            if not (cmd := cmd.strip()):
                print()
                continue

            arg0, argv = (cmd.split(maxsplit=1) + [""])[:2]

            if (cmd_fn := getattr(cmds, f"cmd_{arg0}", None)) is None:
                util.log(f"unkown pdb command {arg0!r}\n")
                continue

            try:
                ex = cmd_fn(argv) if argv else cmd_fn()
            except Exception as e:
                ex = util.err(str(e))
            finally:
                print()
