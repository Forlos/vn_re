# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Compressedbg(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.ensure_fixed_contents(b"\x43\x6F\x6D\x70\x72\x65\x73\x73\x65\x64\x42\x47\x5F\x5F\x5F\x00")
        self.header = self._root.Header(self._io, self, self._root)
        self.some_alloc = self._io.read_bytes(self.header.some_size)
        self.pixel_data = self._io.read_bytes_full()

    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.width = self._io.read_u2le()
            self.height = self._io.read_u2le()
            self.bpp = self._io.read_u2le()
            self.unk0 = self._io.read_u2le()
            self.unk1 = self._io.read_u4le()
            self.unk2 = self._io.read_u4le()
            self.unk3 = self._io.read_u4le()
            self.prng_seed = self._io.read_u4le()
            self.some_size = self._io.read_u4le()
            self.unk7 = self._io.read_u1()
            self.unk8 = self._io.read_u1()
            self.unk9 = self._io.read_u2le()



