# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Gxp(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = self._root.Header(self._io, self, self._root)
        self.file_entries = self._io.read_bytes(self.header.file_entries_size)

    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.ensure_fixed_contents(b"\x47\x58\x50\x00")
            self.unk_04 = self._io.read_u4le()
            self.unk_08 = self._io.read_u4le()
            self.unk_0c = self._io.read_u4le()
            self.unk_10 = self._io.read_u4le()
            self.unk_14 = self._io.read_u4le()
            self.file_entries_count = self._io.read_u4le()
            self.file_entries_size = self._io.read_u4le()
            self.raw_file_data_size = self._io.read_u4le()
            self.unk_24 = self._io.read_u4le()
            self.raw_file_data_offset = self._io.read_u4le()
            self.unk_2c = self._io.read_u4le()


    class FileEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.entry_size = self._io.read_u4le()
            self.file_size = self._io.read_u4le()
            self.unk_08 = self._io.read_u4le()
            self.file_name_utf16_len = self._io.read_u4le()
            self.unk_10 = self._io.read_u4le()
            self.unk_14 = self._io.read_u4le()
            self.file_offset = self._io.read_u4le()
            self.unk_1c = self._io.read_u4le()
            self.file_name = (self._io.read_bytes((self.entry_size - 32))).decode(u"UTF-16LE")


    @property
    def raw_file_data(self):
        if hasattr(self, '_m_raw_file_data'):
            return self._m_raw_file_data if hasattr(self, '_m_raw_file_data') else None

        _pos = self._io.pos()
        self._io.seek(self.header.raw_file_data_offset)
        self._m_raw_file_data = self._io.read_bytes(self.header.raw_file_data_size)
        self._io.seek(_pos)
        return self._m_raw_file_data if hasattr(self, '_m_raw_file_data') else None


