# SPDX-License-Identifier: CC0-1.0

def main():
    from setuptools import setup
    import piki_tools as app

    setup(
        name         = app.__project__,
        version      = app.__version__,
        entry_points = app.__entry_points__,
        packages     = ["piki_tools"]
    )
#

if __name__ == '__main__':
    main()
