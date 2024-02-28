# SPDX-License-Identifier: CC0-1.0

from os import makedirs
from pathlib import Path
from typing import IO

# Python's read methods are stupid.
def read_exact(io: IO, size: int):
    data = io.read(size)
    if len(data) != size:
        raise EOFError()
    return data
#

def decode_c_string(c_string: bytes, encoding: str = "utf-8", errors: str = "strict") -> str:
    if b'\0' in c_string:
        return c_string[:c_string.find(b'\0')].decode(encoding, errors)
    return c_string.decode(encoding, errors)
#

def align_down(value: int, size: int):
    return value - value % size
#

def align_up(value: int, size: int):
    return align_down(value + size - 1, size)
#

def pad_len_pow2(value: int, size: int):
    return ~(value - 1) & (size - 1)
#

def open_helper(file, mode, make_dirs = False, overwrite = True, buffering = -1, encoding = None, errors = None, newline = None, closefd = True, opener = None):
    file = Path(file).resolve()
    if not overwrite and file.exists(): raise FileExistsError
    if make_dirs: makedirs(file.parent, exist_ok=True)
    return open(file, mode, buffering, encoding, errors, newline, closefd, opener)
#
