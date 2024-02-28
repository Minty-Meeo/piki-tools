# SPDX-License-Identifier: MIT

from piki_tools.parse import filepath_redirect_dict, nodes_to_filepaths_recursive
from piki_tools.arcdir import extract_paired_arc_dir, pack_paired_arc_dir

def help_extract():
    print("Usage: piki_arcdir EXTRACT <*.arc path> <*.dir path> [<file 1> <destination 1>] [<file 2> <destination 2>] ... [<file N> <destination N>]\n"
          "You may provide optional file and destination argument pairs to extract individual files to an exact destination.")
#

def help_pack():
    print("Usage: piki_arcdir PACK <*.arc path> <*.dir path> [path 1] [path 2] ... [path N]\n"
          "       piki_arcdir PACK_BIN <*.arc path> <*.dir path> [path 1] [path 2] ... [path N]\n"
          "Each optional path argument will pack that file (or directory, recursively) into the archive. The latter command will filter recursively found files by their extension.")
#

def help():
    print("It is recommended to run this program from the dataDir directory of Pikmin 1\n")
    help_extract()
    print()
    help_pack()
#

def main_extract(args: list[str]):
    if (len(args) < 4 or len(args) % 2):
        help_extract()
        return
    extract_paired_arc_dir(open(args[2], "rb"), open(args[3], "rb"), filepath_redirect_dict(args[4:]))
#

def main_pack(args: list[str], ext: str | tuple[str] = ""):
    if (len(args) < 4):
        help_pack()
        return
    pack_paired_arc_dir(open(args[2], "wb"), open(args[3], "wb"), nodes_to_filepaths_recursive(args[4:], ext))
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
        case "pack_bin":
            main_pack(argv, "bin")
            return
        case "pack":
            main_pack(argv)
            return
    help()
#

if __name__ == "__main__":
    main()
