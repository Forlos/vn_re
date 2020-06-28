# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Cpz7(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = self._root.Header(self._io, self, self._root)
        self.archive_data = self._io.read_bytes(self.header.archive_data_size_decrypted)
        self.file_data = self._io.read_bytes(self.header.file_data_size_decrypted)
        self.encryption_data = self._root.EncryptionData(self._io, self, self._root)

    class ArchiveDataEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.entry_size = self._io.read_u4le()
            self.file_count = self._io.read_u4le()
            self.unknown_8 = self._io.read_u4le()
            self.file_decrypt_key = self._io.read_u4le()
            self.name = self._io.read_bytes((self.entry_size - 16))


    class ArchiveData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.entries = []
            i = 0
            while not self._io.is_eof():
                self.entries.append(self._root.ArchiveDataEntry(self._io, self, self._root))
                i += 1



    class EncryptionData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.md5_checksum = self._io.read_bytes(16)
            self.data_size = self._io.read_u4le()
            self.key = self._io.read_u4le()
            self.data = self._io.read_bytes((self._parent.header.encryption_data_size_decrypted - 24))


    class Files(KaitaiStruct):
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



    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.ensure_fixed_contents(b"\x43\x50\x5A\x37")
            self.archive_data_entry_count = self._io.read_u4le()
            self.archive_data_size = self._io.read_u4le()
            self.file_data_size = self._io.read_u4le()
            self.raw_data_md5 = self._io.read_bytes(16)
            self._raw_cpz7_md5 = self._io.read_bytes(16)
            self.cpz7_md5 = KaitaiStream.process_xor_many(self._raw_cpz7_md5, b"\x1A\x7C\xDE\x43\x16\xF4\x65\xCC\x3D\xA9\x16\xD0\x9B\xBA\xA3\x97")
            self.archive_data_key = self._io.read_u4le()
            self.unknown_34 = self._io.read_u4le()
            self.file_decrypt_key = self._io.read_u4le()
            self.unknown15_3c = self._io.read_u4le()
            self.encryption_data_size = self._io.read_u4le()
            self.checksum = self._io.read_u4le()

        @property
        def archive_data_entry_count_decrypted(self):
            if hasattr(self, '_m_archive_data_entry_count_decrypted'):
                return self._m_archive_data_entry_count_decrypted if hasattr(self, '_m_archive_data_entry_count_decrypted') else None

            self._m_archive_data_entry_count_decrypted = (self.archive_data_entry_count ^ 4265235418)
            return self._m_archive_data_entry_count_decrypted if hasattr(self, '_m_archive_data_entry_count_decrypted') else None

        @property
        def unknown_34_decrypted(self):
            if hasattr(self, '_m_unknown_34_decrypted'):
                return self._m_unknown_34_decrypted if hasattr(self, '_m_unknown_34_decrypted') else None

            self._m_unknown_34_decrypted = (self.unknown_34 ^ 4218661206)
            return self._m_unknown_34_decrypted if hasattr(self, '_m_unknown_34_decrypted') else None

        @property
        def file_data_size_decrypted(self):
            if hasattr(self, '_m_file_data_size_decrypted'):
                return self._m_file_data_size_decrypted if hasattr(self, '_m_file_data_size_decrypted') else None

            self._m_file_data_size_decrypted = (self.file_data_size ^ 2054109741)
            return self._m_file_data_size_decrypted if hasattr(self, '_m_file_data_size_decrypted') else None

        @property
        def file_decrypt_key_decrypted(self):
            if hasattr(self, '_m_file_decrypt_key_decrypted'):
                return self._m_file_decrypt_key_decrypted if hasattr(self, '_m_file_decrypt_key_decrypted') else None

            self._m_file_decrypt_key_decrypted = (self.file_decrypt_key ^ 934082610)
            return self._m_file_decrypt_key_decrypted if hasattr(self, '_m_file_decrypt_key_decrypted') else None

        @property
        def archive_data_size_decrypted(self):
            if hasattr(self, '_m_archive_data_size_decrypted'):
                return self._m_archive_data_size_decrypted if hasattr(self, '_m_archive_data_size_decrypted') else None

            self._m_archive_data_size_decrypted = (self.archive_data_size ^ 938645736)
            return self._m_archive_data_size_decrypted if hasattr(self, '_m_archive_data_size_decrypted') else None

        @property
        def encryption_data_size_decrypted(self):
            if hasattr(self, '_m_encryption_data_size_decrypted'):
                return self._m_encryption_data_size_decrypted if hasattr(self, '_m_encryption_data_size_decrypted') else None

            self._m_encryption_data_size_decrypted = (self.encryption_data_size ^ 1710201331)
            return self._m_encryption_data_size_decrypted if hasattr(self, '_m_encryption_data_size_decrypted') else None

        @property
        def archive_data_key_decrypted(self):
            if hasattr(self, '_m_archive_data_key_decrypted'):
                return self._m_archive_data_key_decrypted if hasattr(self, '_m_archive_data_key_decrypted') else None

            self._m_archive_data_key_decrypted = (self.archive_data_key ^ 2927442359)
            return self._m_archive_data_key_decrypted if hasattr(self, '_m_archive_data_key_decrypted') else None


    class FileEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.entry_size = self._io.read_u4le()
            self.offset = self._io.read_u4le()
            self.unknown_8 = self._io.read_u4le()
            self.file_size = self._io.read_u4le()
            self.unknown_10 = self._io.read_u4le()
            self.unknown_14 = self._io.read_u4le()
            self.file_decrypt_key = self._io.read_u4le()
            self.file_name = self._io.read_bytes((self.entry_size - 28))


    @property
    def raw_header(self):
        if hasattr(self, '_m_raw_header'):
            return self._m_raw_header if hasattr(self, '_m_raw_header') else None

        _pos = self._io.pos()
        self._io.seek(0)
        self._m_raw_header = self._io.read_bytes(68)
        self._io.seek(_pos)
        return self._m_raw_header if hasattr(self, '_m_raw_header') else None

    @property
    def raw_data(self):
        if hasattr(self, '_m_raw_data'):
            return self._m_raw_data if hasattr(self, '_m_raw_data') else None

        _pos = self._io.pos()
        self._io.seek(72)
        self._m_raw_data = self._io.read_bytes(((self.header.archive_data_size_decrypted + self.header.file_data_size_decrypted) + self.header.encryption_data_size_decrypted))
        self._io.seek(_pos)
        return self._m_raw_data if hasattr(self, '_m_raw_data') else None

    @property
    def raw_file_data(self):
        if hasattr(self, '_m_raw_file_data'):
            return self._m_raw_file_data if hasattr(self, '_m_raw_file_data') else None

        _pos = self._io.pos()
        self._io.seek((((self.header.archive_data_size_decrypted + self.header.file_data_size_decrypted) + self.header.encryption_data_size_decrypted) + 72))
        self._m_raw_file_data = self._io.read_bytes_full()
        self._io.seek(_pos)
        return self._m_raw_file_data if hasattr(self, '_m_raw_file_data') else None


