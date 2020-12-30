# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Silky(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.entries_size = self._io.read_u4le()
        self._raw_entries = self._io.read_bytes(self.entries_size)
        io = KaitaiStream(BytesIO(self._raw_entries))
        self.entries = self._root.FileEntries(io, self, self._root)

    class FileEntries(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.entries = []
            i = 0
            while not self._io.is_eof():
                self.entries.append(self._root.FileEntry(self._io, self, self._root))
                i += 1



    class FileEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name_length = self._io.read_u1()
            self.name = self._io.read_bytes(self.name_length)
            self.file_size = self._io.read_u4le()
            self.uncompressed_file_size = self._io.read_u4le()
            self.file_offset = self._io.read_u4le()


    @property
    def file_data_offset(self):
        if hasattr(self, '_m_file_data_offset'):
            return self._m_file_data_offset if hasattr(self, '_m_file_data_offset') else None

        self._m_file_data_offset = (self.entries_size + 4)
        return self._m_file_data_offset if hasattr(self, '_m_file_data_offset') else None


