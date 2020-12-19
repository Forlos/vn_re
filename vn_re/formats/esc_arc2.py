# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class EscArc2(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.ensure_fixed_contents(b"\x45\x53\x43\x2D\x41\x52\x43\x32")
        self.unk1 = self._io.read_u4le()
        self.file_count = self._io.read_u4le()
        self.unk2 = self._io.read_u4le()

    class FileEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.file_name_table_offset = self._io.read_u4le()
            self.file_offset = self._io.read_u4le()
            self.file_size = self._io.read_u4le()


    @property
    def key(self):
        if hasattr(self, '_m_key'):
            return self._m_key if hasattr(self, '_m_key') else None

        self._m_key = 1705808741
        return self._m_key if hasattr(self, '_m_key') else None

    @property
    def file_entry_size(self):
        if hasattr(self, '_m_file_entry_size'):
            return self._m_file_entry_size if hasattr(self, '_m_file_entry_size') else None

        self._m_file_entry_size = 12
        return self._m_file_entry_size if hasattr(self, '_m_file_entry_size') else None


