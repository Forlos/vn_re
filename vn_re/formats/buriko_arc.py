# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class BurikoArc(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.ensure_fixed_contents(b"\x42\x55\x52\x49\x4B\x4F\x20\x41\x52\x43")
        self.version = (self._io.read_bytes(2)).decode(u"ascii")
        self.entry_count = self._io.read_u4le()
        self.file_entries = [None] * (self.entry_count)
        for i in range(self.entry_count):
            self.file_entries[i] = self._root.FileEntry(self._io, self, self._root)


    class FileEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = self._io.read_bytes(96)
            self.file_offset = self._io.read_u4le()
            self.file_size = self._io.read_u4le()
            self.unknown = self._io.read_bytes(24)


    @property
    def file_contents_offset(self):
        if hasattr(self, '_m_file_contents_offset'):
            return self._m_file_contents_offset if hasattr(self, '_m_file_contents_offset') else None

        self._m_file_contents_offset = (16 + (self.entry_count * 128))
        return self._m_file_contents_offset if hasattr(self, '_m_file_contents_offset') else None


