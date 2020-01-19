# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Tlg0(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.ensure_fixed_contents(b"\x54\x4C\x47\x30\x2E\x30\x00\x73\x64\x73\x1A")
        self.raw_length = self._io.read_u4le()
        self.tlg_raw_data = self._io.read_bytes(self.raw_length)

    class Tlg0Chunk(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = self._io.read_bytes(4)
            self.chunk_size = self._io.read_u4le()
            self.data = self._io.read_bytes(self.chunk_size)


    @property
    def raw_data_magic(self):
        if hasattr(self, '_m_raw_data_magic'):
            return self._m_raw_data_magic if hasattr(self, '_m_raw_data_magic') else None

        _pos = self._io.pos()
        self._io.seek(15)
        self._m_raw_data_magic = self._io.read_bytes(11)
        self._io.seek(_pos)
        return self._m_raw_data_magic if hasattr(self, '_m_raw_data_magic') else None

    @property
    def info_data_point(self):
        if hasattr(self, '_m_info_data_point'):
            return self._m_info_data_point if hasattr(self, '_m_info_data_point') else None

        self._m_info_data_point = ((self.raw_length + 11) + 4)
        return self._m_info_data_point if hasattr(self, '_m_info_data_point') else None

    @property
    def chunks(self):
        if hasattr(self, '_m_chunks'):
            return self._m_chunks if hasattr(self, '_m_chunks') else None

        _pos = self._io.pos()
        self._io.seek(self.info_data_point)
        self._m_chunks = []
        i = 0
        while not self._io.is_eof():
            self._m_chunks.append(self._root.Tlg0Chunk(self._io, self, self._root))
            i += 1

        self._io.seek(_pos)
        return self._m_chunks if hasattr(self, '_m_chunks') else None


