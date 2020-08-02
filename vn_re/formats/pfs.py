# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Pfs(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.ensure_fixed_contents(b"\x70\x66\x38")
        self.header = self._root.Header(self._io, self, self._root)
        self.entries = [None] * (self.header.file_entries_count)
        for i in range(self.header.file_entries_count):
            self.entries[i] = self._root.FileEntry(self._io, self, self._root)


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.archive_data_size = self._io.read_u4le()
            self.file_entries_count = self._io.read_u4le()


    class FileEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.file_name_size = self._io.read_u4le()
            self.file_name = self._io.read_bytes(self.file_name_size)
            self.unk = self._io.read_u4le()
            self.file_offset = self._io.read_u4le()
            self.file_size = self._io.read_u4le()


    @property
    def raw_archive_data(self):
        if hasattr(self, '_m_raw_archive_data'):
            return self._m_raw_archive_data if hasattr(self, '_m_raw_archive_data') else None

        _pos = self._io.pos()
        self._io.seek(7)
        self._m_raw_archive_data = self._io.read_bytes(self.header.archive_data_size)
        self._io.seek(_pos)
        return self._m_raw_archive_data if hasattr(self, '_m_raw_archive_data') else None


