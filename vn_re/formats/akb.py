# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Akb(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.ensure_fixed_contents(b"\x41\x4B\x42\x20")
        self.width = self._io.read_u2le()
        self.height = self._io.read_u2le()
        self.compression = self._io.read_u4le()
        self.fill = self._io.read_u4le()
        self.left = self._io.read_u4le()
        self.top = self._io.read_u4le()
        self.right = self._io.read_u4le()
        self.bottom = self._io.read_u4le()
        self.image_data = self._io.read_bytes_full()


