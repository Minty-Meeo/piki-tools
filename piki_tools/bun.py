# SPDX-License-Identifier: CC0-1.0

from struct import pack, unpack
from os.path import relpath, splitext
from typing import BinaryIO

from piki_tools.misc import decode_c_string, open_helper, pad_dist_pow2, read_exact

map_file_ext_to_magic = {
#   ".pcr": 0,  # Are *.pcr files actually magic 0, or is that just the default?
    ".bti": 1,
    ".dca": 2,
    ".dck": 3,
}

def get_magic(file_ext: str):
    file_ext = file_ext.casefold()
    return map_file_ext_to_magic[file_ext] if file_ext in map_file_ext_to_magic else 0
#

def extract_bundle(bun: BinaryIO, filepaths: dict[str, str] = dict(), encoding: str = "shift-jis"):
    count, = unpack(">I", read_exact(bun, 4))
    for _ in range(count):
        magic, size, strlen = unpack(">III", read_exact(bun, 12))
        filepath = decode_c_string(read_exact(bun, strlen), encoding)
        if magic != get_magic(splitext(filepath)[1]):
            print(f"File magic {magic} was unexpected for \"{filepath}\".")
        if filepaths:
            if filepath in filepaths:
                filepath = filepaths[filepath]
            else:
                continue
        with open_helper(filepath, "wb", make_dirs=True) as f:
            print(f"extracted \"{filepath}\"")
            f.write(read_exact(bun, size))
#

def pack_bundle(bun: BinaryIO, filepaths: list[str] = list(), encoding: str = "shift-jis"):
    count: int = 0
    bun.seek(4)
    for filepath in filepaths:
        with open(filepath, "rb") as f:
            magic = get_magic(splitext(filepath)[1])
            filepath = relpath(filepath)  # Remove bits like "./" or "//"
            filepath = filepath.encode(encoding)
            filepath = filepath + b'\0' * pad_dist_pow2(len(filepath), 4)
            data = f.read()
            bun.write(pack(">III", magic, len(data), len(filepath)))
            bun.write(filepath)
            bun.write(data)
            # Surprisingly, the start of the next file is not padded to any multiple of bytes by GfxConverter.
        count += 1
    bun.seek(0)
    bun.write(pack(">I", count))
#
