# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Tlg5(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.ensure_fixed_contents(b"\x54\x4C\x47\x35\x2E\x30\x00\x72\x61\x77\x1A")
        self.header = self._root.Tlg5Header(self._io, self, self._root)

    class Tlg5Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.colors = self._io.read_u1()
            self.width = self._io.read_u4le()
            self.height = self._io.read_u4le()
            self.block_height = self._io.read_u4le()

        @property
        def block_count(self):
            if hasattr(self, '_m_block_count'):
                return self._m_block_count if hasattr(self, '_m_block_count') else None

            self._m_block_count = ((self.height - 1) // self.block_height + 1)
            return self._m_block_count if hasattr(self, '_m_block_count') else None


    class Tlg5Block(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data_entry = [None] * (self._parent.header.colors)
            for i in range(self._parent.header.colors):
                self.data_entry[i] = self._root.Tlg5Data(self._io, self, self._root)



    class Tlg5Data(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.is_compressed = self._io.read_u1()
            self.data_size = self._io.read_u4le()
            self.data = self._io.read_bytes(self.data_size)


    @property
    def blocks(self):
        if hasattr(self, '_m_blocks'):
            return self._m_blocks if hasattr(self, '_m_blocks') else None

        _pos = self._io.pos()
        self._io.seek((13 + (4 * self.header.block_count)))
        self._m_blocks = [None] * ((self.header.height // self.header.block_height if (self.header.height % self.header.block_height) == 0 else (self.header.height // self.header.block_height + 1)))
        for i in range((self.header.height // self.header.block_height if (self.header.height % self.header.block_height) == 0 else (self.header.height // self.header.block_height + 1))):
            self._m_blocks[i] = self._root.Tlg5Block(self._io, self, self._root)

        self._io.seek(_pos)
        return self._m_blocks if hasattr(self, '_m_blocks') else None


