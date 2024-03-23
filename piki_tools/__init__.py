# SPDX-License-Identifier: CC0-1.0

__project__      = 'piki_tools'
__version__      = '1.0.0'

__entry_points__ = {
    "console_scripts": [
        "piki_arcdir = piki_tools.piki_arcdir:main",
        "piki_bun = piki_tools.piki_bun:main",
        "piki_barc = piki_tools.piki_barc:main",
        "piki_txe = piki_tools.piki_txe:main",
    ],
}

__requires__ = ["PIL", "more_itertools", "gclib"]
