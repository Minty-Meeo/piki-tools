# SPDX-License-Identifier: MIT

from os.path import abspath, dirname

from piki_tools.barc import extract_barc, pack_barc

def help_extract():
    print("Usage: piki_barc EXTRACT <*.hed path> [*.arc folder location]\n"
          "The associated *.arc file is assumed to be in the same directory as the *.hed file unless specified. The archive contents will be extracted into the current working directory.")
#

def help_pack():
    print("Usage: piki_barc PACK <*.hed path> <*.arc path> [filepath 1] [filepath 2] ... [filepath N]\n"
          "Each optional path argument will pack that file into the archive. Supply the filepath \"dummy\" to create a dummy entry at that index.")
#

def help():
    print("Run this program from the directory you want the *.jam file paths to be relative to\n")
    help_extract()
    print()
    help_pack()
#

def main_extract(args: list[str]):
    if (len(args) < 3):
        help_extract()
        return
    extract_barc(open(args[2], "rb"), dirname(abspath(args[2])) if len(args) < 4 else args[3])
#

def main_pack(args: list[str]):
    if (len(args) < 4):
        help_pack()
        return
    pack_barc(open(args[2], "wb"), args[3], args[4:])
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
        case "pack":
            main_pack(argv)
            return
    help()
#

if __name__ == "__main__":
    main()
