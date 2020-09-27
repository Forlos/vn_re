# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Ypf(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.ensure_fixed_contents(b"\x59\x50\x46\x00")
        self.header = self._root.Header(self._io, self, self._root)
        self.entry_data = self._io.read_bytes(self.header.entry_data_size)

    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.archive_version = self._io.read_u4le()
            self.entry_count = self._io.read_u4le()
            self.entry_data_size = self._io.read_u4le()
            self.padding = self._io.read_bytes(16)


    class FileEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unk0 = self._io.read_u4le()
            self.name_size = self._io.read_u1()
            self.name = self._io.read_bytes(self.name_size)
            self.unk1 = self._io.read_u1()
            self.flags = self._io.read_u1()
            self.file_size = self._io.read_u4le()
            self.compressed_file_size = self._io.read_u4le()
            self.file_offset = self._io.read_u8le()
            self.unk7 = self._io.read_u4le()



