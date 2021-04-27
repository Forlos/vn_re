# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Iar(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.ensure_fixed_contents(b"\x69\x61\x72\x20")
        self.header = self._root.Header(self._io, self, self._root)
        self.entry_index_table = [None] * (self.header.entry_count)
        for i in range(self.header.entry_count):
            self.entry_index_table[i] = self._io.read_u8le()


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.major_version = self._io.read_u2le()
            self.minor_version = self._io.read_u2le()
            self.unk0 = self._io.read_u4le()
            self.some_size = self._io.read_u4le()
            self.timestamp = self._io.read_u4le()
            self.unk3 = self._io.read_u4le()
            self.entry_count = self._io.read_u4le()
            self.entry_count2 = self._io.read_u4le()


    class FileEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.version = self._io.read_u4le()
            self.unk0 = self._io.read_u4le()
            self.decompressed_file_size = self._io.read_u4le()
            self.unk2 = self._io.read_u4le()
            self.file_size = self._io.read_u4le()
            self.unk3 = self._io.read_u4le()
            self.unk4 = self._io.read_u4le()
            self.unk5 = self._io.read_u4le()
            self.width = self._io.read_u4le()
            self.height = self._io.read_u4le()
            self.unknown = self._io.read_bytes(32)


    class SubImage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.parent_index = self._io.read_u4le()
            self.top = self._io.read_u4le()
            self.height = self._io.read_u4le()



