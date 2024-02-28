# SPDX-License-Identifier: CC0-1.0

from io import BytesIO
from struct import unpack, pack
from typing import BinaryIO

from gclib.fs_helpers import read_all_bytes
from gclib.gx_enums import ImageFormat, WrapMode
from gclib.texture_utils import decode_image, encode_image
from PIL.Image import Image

from piki_tools.misc import read_exact

# Analogous to gxTexFmts
map_mode_to_texfmt = (
    ImageFormat.RGB565,
    ImageFormat.CMPR,
    ImageFormat.RGB5A3,
    ImageFormat.I4,
    ImageFormat.I8,
    ImageFormat.IA4,
    ImageFormat.IA8,
    ImageFormat.RGBA32,  # RGBA8
#   ImageFormat(0x11),  # Z8 (texture copy format)
)

map_texfmt_to_mode = {
    ImageFormat.RGB565 : 0,
    ImageFormat.CMPR : 1,
    ImageFormat.RGB5A3 : 2,
    ImageFormat.I4 : 3,
    ImageFormat.I8 : 4,
    ImageFormat.IA4 : 5,
    ImageFormat.IA8 : 6,
    ImageFormat.RGBA32 : 7,  # RGBA8
#   ImageFormat(0x11): 8,  # Z8 (texture copy format)
}

def decode_dolphin_texture_header(header: bytes):
    # TexImg::importTxe(Texture* texture, RandomAccessStream& stream)
    # {
    #    this->width   = stream.readShort()
    #    this->height  = stream.readShort()
    #    this->mode    = stream.readShort() & 0xFFFF
    #    texture->wrap = this->mode >> 8;  // Questionable bitfield storing texture wrap info... and this only sets the wrap_s part... wtf Nintendo!
    #    this->mode    = this->mode & 0xFF
    #    (void)stream.readShort()
    #    (void)stream.readInt()  // Vestigial data size field that sometimes is set, other times is not (halowhit.txe, shadow.txe).
    #    for (int i = 0; i < 10; ++i)
    #      (void)stream.readShort()
    #    ...
    # }
    return unpack(">hhbb2xi20x", header)
#

# Returns a tuple of (image, wrap_s).
def decode_dolphin_texture(io: BinaryIO) -> tuple[Image, WrapMode]:
    width, height, wrap_s, mode, data_size = decode_dolphin_texture_header(read_exact(io, 32))
    data = io.read()
    if len(data) != data_size:
        print(f"Vestigial data size field ({data_size}) != actual data size ({len(data)}).")
    return (decode_image(BytesIO(data), None, map_mode_to_texfmt[mode], None, None, width, height), wrap_s)
#

# I kid you not, you can set the wrap_s but not the wrap_t.
def encode_dolphin_texture(image: Image, texfmt: ImageFormat, wrap_s: WrapMode = WrapMode.ClampToEdge) -> bytes:
    data = read_all_bytes(encode_image(image, texfmt, None, 0)[0])
    header = pack(">hhbb2xi20x", image.width, image.height, wrap_s.value, map_texfmt_to_mode[texfmt], len(data))
    return header + data
#
