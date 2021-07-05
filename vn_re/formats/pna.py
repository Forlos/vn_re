# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Pna(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.read_bytes(4)
        _on = self.magic
        if _on == b"\x50\x4E\x41\x50":
            self.data = self._root.Pnap(self._io, self, self._root)
        elif _on == b"\x57\x50\x41\x50":
            self.data = self._root.Wpap(self._io, self, self._root)
        self.image_data = self._io.read_bytes_full()

    class WpapEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = self._io.read_u4le()
            self.id = self._io.read_u4le()
            self.left_offset = self._io.read_u4le()
            self.top_offset = self._io.read_u4le()
            self.width = self._io.read_u4le()
            self.height = self._io.read_u4le()
            self.unk0 = self._io.read_bytes(12)
            self.size = self._io.read_u4le()


    class Wpap(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header = self._root.WpapHeader(self._io, self, self._root)
            self.entries = [None] * (self.header.some_count)
            for i in range(self.header.some_count):
                self.entries[i] = self._root.WpapEntry(self._io, self, self._root)



    class PnapEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = self._io.read_u4le()
            self.id = self._io.read_u4le()
            self.left_offset = self._io.read_u4le()
            self.top_offset = self._io.read_u4le()
            self.width = self._io.read_u4le()
            self.height = self._io.read_u4le()
            self.unk0 = self._io.read_bytes(12)
            self.size = self._io.read_u4le()


    class PnapHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unk0 = self._io.read_u4le()
            self.unk1 = self._io.read_u4le()
            self.unk2 = self._io.read_u4le()
            self.some_count = self._io.read_u4le()


    class WpapHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unk0 = self._io.read_u4le()
            self.unk1 = self._io.read_u4le()
            self.unk2 = self._io.read_u4le()
            self.some_count = self._io.read_u4le()


    class Pnap(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header = self._root.PnapHeader(self._io, self, self._root)
            self.entries = [None] * (self.header.some_count)
            for i in range(self.header.some_count):
                self.entries[i] = self._root.PnapEntry(self._io, self, self._root)




