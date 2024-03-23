# SPDX-License-Identifier: CC0-1.0

from os import getcwd
from os.path import relpath, split
from struct import pack, unpack
from typing import BinaryIO

from piki_tools.misc import decode_c_string, open_helper, read_exact

def extract_barc(hed: BinaryIO, arc_location: str = getcwd(), encoding: str = "shift-jis"):
    magic, count, arc_name = unpack(">8s4xI16s", read_exact(hed, 32))
    assert magic == b'BARC----', "BARC header was missing magic identifier."
    arc_name = decode_c_string(arc_name, encoding)
    with open(f"{arc_location}/{arc_name}", "rb") as arc:
        for _ in range(count):
            # I didn't research what's up with the two bytes of padding followed by a short.
            # All I know is the short equals 0 when the sequence is a dummy.
            jam_name, unk, offset, size = unpack(">12s2xh8xII", read_exact(hed, 32))
            if unk == 0:
                continue
            jam_name = decode_c_string(jam_name, encoding)
            with open_helper(jam_name, "wb", make_dirs=True) as f:
                arc.seek(offset)
                f.write(read_exact(arc, size))
#

def pack_barc(hed: BinaryIO, arc_path: str, jam_names: list[str], encoding: str = "shift-jis"):
    arc_name = split(arc_path)[1].encode(encoding)  # Get just the filename.
    assert len(arc_name) <= 16, f"File name {arc_name.decode(encoding)} for *.arc is too long."
    with open_helper(arc_path, "wb", make_dirs=True) as arc:
        count: int = len(jam_names)
        hed.write(pack(">8s4xI16s", b'BARC----', count, arc_name))
        for jam_name in jam_names:
            if jam_name == "dummy":
                unk = offset = size = 0
            else:
                jam_name = relpath(jam_name)  # Remove bits like "./" or "//"
                with open(jam_name, "rb") as f:
                    unk = -1
                    offset = arc.tell()
                    arc.write(f.read())  # TODO: Is there any alignment to do?
                    size = f.tell()
            jam_name = jam_name.encode(encoding)
            if (len(jam_name) > 12):
                print(f"Warning: File entry name \"{jam_name.decode(encoding)}\" will be truncated to \"{jam_name[0:12].decode(encoding, 'ignore')}\"")
            hed.write(pack(">12s2xh8xII", jam_name, unk, offset, size))
#
