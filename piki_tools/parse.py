# SPDX-License-Identifier: CC0-1.0

from os import walk
from os.path import isdir, join

from more_itertools import chunked
    
def filepath_redirect_dict(paths: list[str]):
    return dict[str, str]([pair for pair in chunked(paths, 2, True)])  # TODO: Python 3.12 replace with batched
#

# Filepaths found recursively will be filtered by the file extension(s) given. Filepaths explicitly given are not.
def nodes_to_filepaths_recursive(nodes: list[str], ext: str | tuple[str] = ""):
    filepaths = list[str]()
    for node in nodes:
        if (isdir(node)):
            for root, _, filenames in walk(node):
                filepaths.extend(join(root, filename) for filename in filenames if filename.casefold().endswith(ext))
        else:
            filepaths.append(node)
    return sorted(filepaths)  # GfxConverter seems to sort the filepaths alphabetically.
#
