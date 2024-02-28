# SPDX-License-Identifier: MIT

from gclib.gx_enums import ImageFormat
from PIL import Image

from piki_tools.misc import open_helper
from piki_tools.txe import decode_dolphin_texture, encode_dolphin_texture, map_mode_to_texfmt

def help_decode():
    print("Usage: piki_txe DECODE <*.txe path> [image path]\n"
          "By default, the decoded image will write to \"<*.txe path>.png\"")
#
    
def help_encode():
    print("Usage: piki_txe ENCODE <format> <image path> [*.txe path]\n"
          "By default, the encoded dolphin texture will write to \"<image path>.txe\"\n"
          "Texture Formats: [RGB565, CMPR, RGB5A3, I4, I8, IA4, IA8, RGBA8]\n"
          "                 [     0,    1,      2,  3,  4,   5,   6,     7]")
#

def help():
    help_decode()
    print()
    help_encode()
#

map_str_to_texfmt = {
    "rgb565" : ImageFormat.RGB565,
    "cmpr" : ImageFormat.CMPR,
    "rgb5a3" : ImageFormat.RGB5A3,
    "i4" : ImageFormat.I4,
    "i8" : ImageFormat.I8,
    "ia4" : ImageFormat.IA4,
    "ia8" : ImageFormat.IA8,
    "rgba8" :ImageFormat.RGBA32,
    "rgba32" :ImageFormat.RGBA32,  # The more common name
}

def get_texfmt_from_str(s: str):
    s_casefold = s.casefold()
    if s_casefold in map_str_to_texfmt:
        return map_str_to_texfmt[s_casefold]
    mode = int(s)  # Will raise ValueError if it fails
    if mode in map_mode_to_texfmt:
        return map_mode_to_texfmt[mode]
    raise ValueError
#

def main_decode(args: list[str]):
    if len(args) < 3:
        help_decode()
        return
    with open(args[2], "rb") as f:
        decode_dolphin_texture(f)[0].save(args[2] + ".png" if len(args) < 4 else args[3])
#

def main_encode(args: list[str]):
    if len(args) < 4:
        help_encode()
        return
    try: texfmt = get_texfmt_from_str(args[2])
    except ValueError:
        print(f"Texture format \"{args[2]}\" is not recognized")
        return
    with Image.open(args[3]) as image:
        with open_helper(args[3] + ".txe" if len(args) < 5 else args[4], "wb", make_dirs=True) as f:
            f.write(encode_dolphin_texture(image, texfmt))
#

def main():
    from sys import argv
    
    if len(argv) < 2:
        help()
        return
    match argv[1].casefold():
        case "decode":
            main_decode(argv)
            return
        case "encode":
            main_encode(argv)
            return
    help()
#

if __name__ == "__main__":
    main()
