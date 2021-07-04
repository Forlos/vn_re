# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Crx(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.ensure_fixed_contents(b"\x43\x52\x58\x47")
        self.header = self._root.Header(self._io, self, self._root)
        if self.header.has_alpha == 258:
            self.color_table_with_alpha = self._io.read_bytes(1024)

        if self.header.has_alpha == 257:
            self.color_table = self._io.read_bytes(768)

        if self.header.unk2 > 2:
            self.headers_count = self._io.read_u4le()

        if self.header.unk2 > 2:
            self._raw_headers = self._io.read_bytes((self.headers_count * 16))
            io = KaitaiStream(BytesIO(self._raw_headers))
            self.headers = self._root.Headers(io, self, self._root)

        if (self.header.unk3 & 16) != 0:
            self.compressed_size = self._io.read_u4le()

        self.image_data = self._io.read_bytes_full()

    class Headers(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.headers = []
            i = 0
            while not self._io.is_eof():
                self.headers.append(self._root.SecondaryHeader(self._io, self, self._root))
                i += 1



    class SecondaryHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unk = self._io.read_bytes(16)


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unk0 = self._io.read_u2le()
            self.unk1 = self._io.read_u2le()
            self.width = self._io.read_u2le()
            self.height = self._io.read_u2le()
            self.unk2 = self._io.read_u2le()
            self.unk3 = self._io.read_u2le()
            self.has_alpha = self._io.read_u2le()
            self.unk5 = self._io.read_u2le()



