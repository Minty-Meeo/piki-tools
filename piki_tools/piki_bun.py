# SPDX-License-Identifier: MIT

from piki_tools.bun import extract_bundle, pack_bundle
from piki_tools.parse import filepath_redirect_dict, nodes_to_filepaths_recursive

def help_extract():
    print("Usage: piki_bun EXTRACT <*.bun path> [<file 1> <destination 1>] [<file 2> <destination 2>] ... [<file N> <destination N>]\n"
          "You may provide optional file and destination argument pairs to extract individual files to an exact destination. Otherwise, all files will be extracted to their relative filepaths.")
#

def help_pack():
    print("Usage: piki_bun PACK <*.bun path> [node 1] [node 2] ... [node N]\n"
          "       piki_bun PACK_PCR <*.bun path> [node 1] [node 2] ... [node N]\n"
          "       piki_bun PACK_BTI <*.bun path> [node 1] [node 2] ... [node N]\n"
          "       piki_bun PACK_DC? <*.bun path> [node 1] [node 2] ... [node N]\n"
          "Each optional path argument will pack that file (or directory, recursively) into the archive. The latter commands will filter recursively found files by their extension.")
#

def help():
    print("All filepaths are relative to the current working directory, so it is recommended to run this program from the dataDir directory of Pikmin 1 when packing.\n")
    help_extract()
    print()
    help_pack()
#

def main_extract(args: list[str]):
    if (len(args) < 3 or len(args) % 2 - 1):
        help_extract()
        return
    extract_bundle(open(args[2], "rb"), filepath_redirect_dict(args[3:]))
#

def main_pack(args: list[str], ext: str | tuple[str] = ""):
    if (len(args) < 3):
        help_pack()
        return
    pack_bundle(open(args[2], "wb"), nodes_to_filepaths_recursive(args[3:], ext))
#

def main():
    from sys import argv

    if (len(argv) < 2):
        help()
        return
    match argv[1].casefold():
        case "extract":
            main_extract(argv)
            return
        case "pack_pcr":
            main_pack(argv, "pcr")
            return
        case "pack_bti":
            main_pack(argv, "bti")
            return
        case "pack_dc?":
            main_pack(argv, ("dca", "dck"))
            return
        case "pack":
            main_pack(argv)
            return
    help()
#

if __name__ == "__main__":
    main()
