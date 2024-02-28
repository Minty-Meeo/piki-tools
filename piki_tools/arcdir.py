# SPDX-License-Identifier: CC0-1.0

from os.path import relpath
from struct import pack, unpack
from typing import BinaryIO

from piki_tools.misc import decode_c_string, open_helper, pad_len_pow2, read_exact

def extract_paired_arc_dir(arc: BinaryIO, dir: BinaryIO, filepaths: dict[str, str] = dict(), encoding: str = "shift-jis"):
    dir_size, count = unpack(">II", read_exact(dir, 8))
    for _ in range(count):
        offset, size, strlen = unpack(">III", read_exact(dir, 12))
        path = decode_c_string(read_exact(dir, strlen), encoding)
        if filepaths:
            if path in filepaths:
                path = filepaths[path]
            else:
                continue
        with open_helper(path, "wb", make_dirs=True) as f:
            arc.seek(offset)
            f.write(read_exact(arc, size))
    assert(dir.tell() == dir_size)  # Sanity check
#

def pack_paired_arc_dir(arc: BinaryIO, dir: BinaryIO, filepaths: list[str] = list(), encoding: str = "shift-jis"):
    count: int = 0
    dir.seek(8)
    for filepath in filepaths:
        with open(filepath, "rb") as f:
            filepath = relpath(filepath)  # Remove bits like "./" or "//"
            filepath = filepath.encode(encoding)
            filepath = filepath + b'\0' * pad_len_pow2(len(filepath), 4)
            data = f.read()
            dir.write(pack(">III", arc.tell(), len(data), len(filepath)))
            dir.write(filepath)
            arc.write(data)
            arc.write(b'\xCC' * pad_len_pow2(arc.tell(), 32))  # Imitate MSVCRTD uninitialized bytes
        count += 1
    dir_size = dir.tell()
    dir.seek(0)
    dir.write(pack(">II", dir_size, count))
#
