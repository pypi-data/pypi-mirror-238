#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pwdmgr pdb commands"""

from __future__ import annotations

import csv
import multiprocessing as mp
import os
from typing import Dict, Final, Optional, Tuple

import armour
import pyfzf  # type: ignore

from . import util
from .pwdmgr_clipboard import clipboard_cp
from .pwdmgr_cmds import Cmds

JOBS: Final[int] = round((os.cpu_count() or 1) * 0.75)


def _import_worker(
    state: Tuple[armour.pdb.header.PdbHeader, Dict[bytes, str], Dict[str, str]],
) -> armour.pdb.entries.PdbPwdEntry:
    """import command worker"""

    e: armour.pdb.entries.PdbPwdEntry = armour.pdb.entries.PdbPwdEntry(
        state[0],
        fields={
            f: (state[2][cf].encode() if cf else b"") for f, cf in state[1].items()
        },
    )

    util.log(f"hasing and encrypting entry {e.name!r}")

    return e.rehash()  # type: ignore


class PdbCmds(Cmds):
    """pdb mode commands"""

    def __init__(self, p: armour.pdb.header.PdbHeader, dbp: str) -> None:
        """pass in the header to use"""

        self.dbp: str = dbp
        self.p: armour.pdb.header.PdbHeader = p
        self.e: armour.pdb.entries.PdbEntries = armour.pdb.entries.PdbEntries(
            p
        ).gather()
        self.modified: bool = False

    def _select(self, data: Tuple[str, ...]) -> Tuple[str, ...]:
        """select multiple"""

        if not data:
            return tuple()

        return tuple(
            pyfzf.FzfPrompt().prompt(  # type: ignore
                data,
                "--multi",
            )
        )

    def _select_entries_idx(self) -> Tuple[int, ...]:
        """select multiple entries as indexes"""

        if not self.e.ents:
            return tuple()

        return tuple(
            int(e.split(" | ", maxsplit=1)[0])
            for e in self._select(
                tuple(
                    f"{idx} | {e.name!r} | {e.remark!r}"  # type: ignore
                    for idx, e in enumerate(self.e.ents)
                ),
            )
        )

    def _select_entries(self) -> Tuple[armour.pdb.entries.PdbPwdEntry, ...]:
        """select multiple entries"""

        if not self.e.ents:
            return tuple()

        return tuple(
            self.e.ents[idx] for idx in self._select_entries_idx()  # type: ignore
        )

    def _select_fields(self) -> Tuple[str, ...]:
        """select fields"""
        return self._select(
            tuple(map(bytes.decode, armour.pdb.entries.PdbPwdEntry.all_fields))
        )

    def _select_fields_b(self) -> Tuple[bytes, ...]:
        """select fields as bytes"""

        util.log("n = name, u = username, p = password, r = remark")

        return tuple(
            map(
                str.encode,
                self._select(
                    tuple(map(bytes.decode, armour.pdb.entries.PdbPwdEntry.all_fields))
                ),
            )
        )

    def cmd_what(self) -> int:
        """print the current db info"""
        print(self.p)
        return 0

    def cmd_commit(self) -> int:
        """commit changes to the database"""

        if not self.modified and not util.yn(
            "do you want to commit to an unchanged db, will rehash"
        ):
            return 0

        util.log("commiting to db")
        self.e.commit()

        db_bin: bytes = self.p.to_pdb()

        with open(self.dbp, "wb") as fp:
            fp.write(db_bin)
            util.log(f"wrote db to {fp.name!r}")

        self.modified = False

        return 0

    def cmd_new(self, name: str) -> int:
        """create a new entry in the database"""

        util.log(f"creating new entry {name!r} -- do not forget to `commit`")

        self.e.add_entry(
            armour.pdb.entries.PdbPwdEntry(
                self.p,
                fields={
                    b"n": name.encode(),
                    b"u": util.sinp("username").encode(),
                    b"p": util.sinp("password").encode(),
                    b"r": util.inp("remark").encode(),
                },
            ).rehash()
        )

        self.modified = True
        util.log(f"saved entry #{len(self.e.ents)}")

        return 0

    def cmd_ls(self) -> int:
        """list all entries"""

        for idx, e in enumerate(self.e.ents):
            print(f"entry #{idx}")
            print(e)
            print()

        return 0

    def cmd_show(self) -> int:
        """show entries in full"""

        for idx, e in enumerate(self._select_entries()):
            print(
                f"""entry #{idx}

name        {e.name!r}
username    {e.username!r}
password    {e.password!r}
remark      {e.remark!r}
"""
            )

        return 0

    def cmd_ed(self) -> int:
        """edit entry fields"""

        fields: Tuple[bytes, ...] = self._select_fields_b()
        entries: Tuple[armour.pdb.entries.PdbPwdEntry, ...] = self._select_entries()

        if not entries or not fields:
            return 0

        for entry in entries:
            for field in fields:
                entry[field] = (
                    util.sinp
                    if field in armour.pdb.entries.PdbPwdEntry.encrypted_fields
                    else util.inp
                )(
                    f"field {field.decode()!r} of entry \
{entry.name.decode()!r} ( {entry.remark.decode()!r} )",
                    entry[field].decode(),
                ).encode()

            entry.rehash().revalidate()
            print()

        self.modified = True
        return 0

    def cmd_export(self, out: str) -> int:
        """export the database in csv"""

        if os.path.exists(out) and not util.yn(
            f"are you sure that you want to overwrite {out!r}",
            "n",
        ):
            return 0

        with open(out, "w", newline="", encoding="utf-8") as fp:
            dw: csv.DictWriter[str] = csv.DictWriter(
                fp,
                [f.decode("utf-8") for f in armour.pdb.entries.PdbPwdEntry.all_fields],
            )

            dw.writeheader()

            util.log("writing and decrypting all entries")

            dw.writerows(
                {k: e[k.encode()].decode() for k in dw.fieldnames} for e in self.e.ents
            )

        return 0

    def cmd_import(self, file: str) -> int:
        """import db from csv"""

        if not os.path.exists(file):
            return util.err(f"export {file!r} does not exist")

        util.log("parsing csv")

        with open(file, "r", encoding="utf-8") as fp:
            d: Tuple[Dict[str, str], ...] = tuple(csv.DictReader(fp))

        keys: Tuple[str, ...] = tuple(d[0].keys())
        util.log(f"found fields : {', '.join(keys)}")

        fields: Dict[bytes, str] = {}

        util.log("n = name, u = username, p = password, r = remark")

        for field in armour.pdb.entries.PdbPwdEntry.all_fields:
            if field.decode() in keys:
                util.log(f"using {field.decode()!r}")
                fields[field] = field.decode()
            else:
                util.log(f"select field for {field.decode()!r}")
                fields[field] = (self._select(keys) or ("",))[0]

        if util.yn(
            "should the database be overwritten rather than merged",
            "n",
        ):
            util.log("clearing entries")
            self.e.clear()

        self.modified = True

        util.log(f"using {JOBS} jobs")

        with mp.Pool(JOBS) as p:
            r: armour.pdb.entries.PdbEntry

            for r in p.map(_import_worker, ((self.p, fields, c) for c in d)):
                util.log(f"adding entry {r.name!r}")
                self.e.add_entry(r)

        return 0

    def cmd_cp(self) -> int:
        """copy field of an entry to clipboard, or display it"""

        entries = self._select_entries()

        if not entries:
            return util.err("no entry selected")

        fields = self._select_fields_b()

        if not fields:
            return util.err("no field selected")

        clipboard_cp(entries[0][fields[0]])
        util.log(
            f"copied field {fields[0].decode()!r} of entry "
            f"{entries[0].name.decode()!r} "
            "to clipboard"
        )

        return 0

    def cmd_rm(self, index: Optional[str] = None) -> int:
        """remove entries from the db, takes optional argument `index`"""

        if index is not None:
            idx: int = int(index)

            if idx < 0 or idx >= len(self.e.ents):
                return util.err(f"index oob [0;{len(self.e.ents)})")

            util.log(f"removing entry #{idx}")
            print(self.e.ents.pop(idx))
        else:
            e: armour.pdb.entries.PdbPwdEntry = armour.pdb.entries.PdbPwdEntry(self.p)

            for idx in self._select_entries_idx():
                util.log(f"removing entry #{idx}")
                print(self.e.ents[idx])
                print()
                self.e.ents[idx] = e

            self.e.ents = list(
                filter(lambda item: item is not e, self.e.ents),
            )

        self.modified = True
        return 0
