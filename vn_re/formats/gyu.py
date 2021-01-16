# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Gyu(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.ensure_fixed_contents(b"\x47\x59\x55\x1A")
        self.version = self._io.read_u4le()
        self.mt_seed = self._io.read_u4le()
        self.bpp = self._io.read_u4le()
        self.width = self._io.read_u4le()
        self.height = self._io.read_u4le()
        self.data_size = self._io.read_u4le()
        self.alpha_channel_size = self._io.read_u4le()
        self.color_table_size = self._io.read_u4le()
        self.color_table = self._io.read_bytes((self.color_table_size * 4))
        self.data = self._io.read_bytes(self.data_size)
        self.alpha_channel = self._io.read_bytes(self.alpha_channel_size)


