# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Acv1(KaitaiStruct):

    class AcvFlags(Enum):
        plain = 0
        encrypted = 1
        compressed = 2
        text_file = 4
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.ensure_fixed_contents(b"\x41\x43\x56\x31")
        self.count = self._io.read_u4le()
        self.entries = [None] * (self.entry_count)
        for i in range(self.entry_count):
            self.entries[i] = self._root.Entry(self._io, self, self._root)


    class Entry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.checksum = self._io.read_u8le()
            self.flags = self._io.read_u1()
            self.offset = self._io.read_u4le()
            self.size = self._io.read_u4le()
            self.uncompressed_size = self._io.read_u4le()


    @property
    def master_key(self):
        """Key that is used to entry encryption."""
        if hasattr(self, '_m_master_key'):
            return self._m_master_key if hasattr(self, '_m_master_key') else None

        self._m_master_key = 2338999903
        return self._m_master_key if hasattr(self, '_m_master_key') else None

    @property
    def script_key(self):
        """Key that is used to decrypt scripts."""
        if hasattr(self, '_m_script_key'):
            return self._m_script_key if hasattr(self, '_m_script_key') else None

        self._m_script_key = 2634801402
        return self._m_script_key if hasattr(self, '_m_script_key') else None

    @property
    def entry_count(self):
        """XOR count with master key to get number of entries."""
        if hasattr(self, '_m_entry_count'):
            return self._m_entry_count if hasattr(self, '_m_entry_count') else None

        self._m_entry_count = (self.count ^ self.master_key)
        return self._m_entry_count if hasattr(self, '_m_entry_count') else None


