# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Tlg6(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.ensure_fixed_contents(b"\x54\x4C\x47\x36\x2E\x30\x00\x72\x61\x77\x1A")
        self.header = self._root.Tlg6Header(self._io, self, self._root)
        self.filter_types = self._root.Tlg6FilterTypes(self._io, self, self._root)
        self.lines = [None] * ((self.header.height // self.tlg6_h_block_size if (self.header.height % self.tlg6_h_block_size) == 0 else (self.header.height // self.tlg6_h_block_size + 1)))
        for i in range((self.header.height // self.tlg6_h_block_size if (self.header.height % self.tlg6_h_block_size) == 0 else (self.header.height // self.tlg6_h_block_size + 1))):
            self.lines[i] = self._root.Tlg6Line(self._io, self, self._root)


    class Tlg6Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.colors = self._io.read_u1()
            self.data_flag = self._io.read_u1()
            self.color_type = self._io.read_u1()
            self.external_golomb_table = self._io.read_u1()
            self.width = self._io.read_u4le()
            self.height = self._io.read_u4le()
            self.max_bit_length = self._io.read_u4le()

        @property
        def x_block_count(self):
            if hasattr(self, '_m_x_block_count'):
                return self._m_x_block_count if hasattr(self, '_m_x_block_count') else None

            self._m_x_block_count = ((self.width - 1) // self._root.tlg6_w_block_size + 1)
            return self._m_x_block_count if hasattr(self, '_m_x_block_count') else None

        @property
        def y_block_count(self):
            if hasattr(self, '_m_y_block_count'):
                return self._m_y_block_count if hasattr(self, '_m_y_block_count') else None

            self._m_y_block_count = ((self.height - 1) // self._root.tlg6_h_block_size + 1)
            return self._m_y_block_count if hasattr(self, '_m_y_block_count') else None


    class Tlg6FilterTypes(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.size = self._io.read_u4le()
            self.buffer = self._io.read_bytes(self.size)


    class Tlg6Line(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.bits = [None] * (self._parent.header.colors)
            for i in range(self._parent.header.colors):
                self.bits[i] = self._root.Tlg6Bits(self._io, self, self._root)



    class Tlg6Bits(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.length = self._io.read_u4le()
            self.bit_pool = self._io.read_bytes((self.length // self._root.tlg6_h_block_size if (self.length % self._root.tlg6_h_block_size) == 0 else (self.length // self._root.tlg6_h_block_size + 1)))

        @property
        def method(self):
            """two most significant bits of bit_length are entropy coding method:
            00 means Golomb method,
            01 means Gamma method (not yet suppoted),
            10 means modified LZSS method (not yet supported),
            11 means raw (uncompressed) data (not yet supported).
            """
            if hasattr(self, '_m_method'):
                return self._m_method if hasattr(self, '_m_method') else None

            self._m_method = ((self.length >> 30) & 3)
            return self._m_method if hasattr(self, '_m_method') else None


    @property
    def tlg6_w_block_size(self):
        if hasattr(self, '_m_tlg6_w_block_size'):
            return self._m_tlg6_w_block_size if hasattr(self, '_m_tlg6_w_block_size') else None

        self._m_tlg6_w_block_size = 8
        return self._m_tlg6_w_block_size if hasattr(self, '_m_tlg6_w_block_size') else None

    @property
    def tlg6_h_block_size(self):
        if hasattr(self, '_m_tlg6_h_block_size'):
            return self._m_tlg6_h_block_size if hasattr(self, '_m_tlg6_h_block_size') else None

        self._m_tlg6_h_block_size = 8
        return self._m_tlg6_h_block_size if hasattr(self, '_m_tlg6_h_block_size') else None

    @property
    def main_count(self):
        if hasattr(self, '_m_main_count'):
            return self._m_main_count if hasattr(self, '_m_main_count') else None

        self._m_main_count = self.header.width // self.tlg6_w_block_size
        return self._m_main_count if hasattr(self, '_m_main_count') else None

    @property
    def fraction(self):
        if hasattr(self, '_m_fraction'):
            return self._m_fraction if hasattr(self, '_m_fraction') else None

        self._m_fraction = (self.header.width - (self.main_count * self.tlg6_w_block_size))
        return self._m_fraction if hasattr(self, '_m_fraction') else None


