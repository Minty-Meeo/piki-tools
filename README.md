# Piki Tools
Some tools written in Python for file formats found in Pikmin 1.

## Installation
Run the command `pip install "piki-tools @ git+https://github.com/Minty-Meeo/piki-tools.git"`.  It may be necessary to use the `--break-system-packages` option if you are on Linux.  piki-tools is dependent on [Pillow](https://pypi.org/project/Pillow/), [more-itertools](https://pypi.org/project/more-itertools/), and [gclib](https://github.com/LagoLunatic/gclib/tree/master).

## Entry Points
- `piki_arcdir`: Command-line tool to pack and extract Paired ARC + DIR Files archives.
- `piki_bun`: Command-line tool to pack and extract Bundle archives.
- `piki_txe`: Command-line tool to encode and decode Dolphin Texture files.

## Modules
- `arcdir`: Library for Paired ARC + DIR Files archives.
- `bun`: Library for Bundle archives.
- `txe`: Library for Dolphin Texture files.
