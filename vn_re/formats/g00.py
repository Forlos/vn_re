# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class G00(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.version = self._io.read_u1()
        self.width = self._io.read_u2le()
        self.height = self._io.read_u2le()
        if self.version == 2:
            self.header_count = self._io.read_u4le()

        if self.version == 2:
            self._raw_headers = self._io.read_bytes((self.header_count * 24))
            io = KaitaiStream(BytesIO(self._raw_headers))
            self.headers = self._root.Headers(io, self, self._root)

        self.pixel_data = self._root.PixelData(self._io, self, self._root)

    class Chunk(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.left = self._io.read_u2le()
            self.top = self._io.read_u2le()
            self.flag = self._io.read_u2le()
            self.width = self._io.read_u2le()
            self.height = self._io.read_u2le()


    class Sprite(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unk0 = self._io.read_u2le()
            self.chunk_count = self._io.read_u2le()
            self.a = self._io.read_u4le()
            self.b = self._io.read_u4le()
            self.width = self._io.read_u4le()
            self.height = self._io.read_u4le()
            self.unk6 = self._io.read_u4le()
            self.unk7 = self._io.read_u4le()
            self.full_width = self._io.read_u4le()
            self.full_height = self._io.read_u4le()


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.left = self._io.read_u4le()
            self.top = self._io.read_u4le()
            self.right = self._io.read_u4le()
            self.bottom = self._io.read_u4le()
            self.unk4 = self._io.read_u4le()
            self.unk5 = self._io.read_u4le()


    class PixelData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.compressed_image_size = self._io.read_u4le()
            self.uncompressed_image_size = self._io.read_u4le()
            self.data = self._io.read_bytes((self.compressed_image_size - 8))


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
                self.headers.append(self._root.Header(self._io, self, self._root))
                i += 1




