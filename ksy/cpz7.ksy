meta:
  id: cpz7
  title: cpz7 file
  file-extension: cpz
  endian: le

seq:
  - id: header
    type: header
  - id: archive_data
    size: header.archive_data_size_decrypted
  - id: file_data
    size: header.file_data_size_decrypted
  - id: encryption_data
    type: encryption_data

types:
  header:
    seq:
      - id: magic
        contents: "CPZ7"
      - id: archive_data_entry_count
        type: u4
      - id: archive_data_size
        type: u4
      - id: file_data_size
        type: u4
      - id: raw_data_md5
        size: 16
      - id: cpz7_md5
        size: 16
        process: xor([0x1A, 0x7C, 0xDE, 0x43, 0x16, 0xF4, 0x65, 0xCC, 0x3D, 0xA9, 0x16, 0xD0, 0x9B, 0xBA, 0xA3, 0x97])
      - id: archive_data_key
        type: u4
      - id: unknown_34
        type: u4
      - id: file_decrypt_key
        type: u4
      - id: unknown15_3c
        type: u4
      - id: encryption_data_size
        type: u4
      - id: checksum
        type: u4
    instances:
      archive_data_entry_count_decrypted:
        value: archive_data_entry_count ^ 0xFE3A53DA
      archive_data_size_decrypted:
        value: archive_data_size ^ 0x37F298E8
      file_data_size_decrypted:
        value: file_data_size ^ 0x7A6F3A2D
      encryption_data_size_decrypted:
        value: encryption_data_size ^ 0x65EF99F3
      archive_data_key_decrypted:
        value: archive_data_key ^ 0xAE7D39B7
      unknown_34_decrypted:
        value: unknown_34 ^ 0xFB73A956
      file_decrypt_key_decrypted:
        value: file_decrypt_key ^ 0x37ACF832

  archive_data:
    seq:
      - id: entries
        type: archive_data_entry
        repeat: eos

  archive_data_entry:
    seq:
      - id: entry_size
        type: u4
      - id: file_count
        type: u4
      - id: unknown_8
        type: u4
      - id: file_decrypt_key
        type: u4
      - id: name
        size: entry_size - 0x10

  files:
    seq:
      - id: entries
        type: file_entry
        repeat: eos

  file_entry:
    seq:
      - id: entry_size
        type: u4
      - id: offset
        type: u4
      - id: unknown_8
        type: u4
      - id: file_size
        type: u4
      - id: unknown_10
        type: u4
      - id: unknown_14
        type: u4
      - id: file_decrypt_key
        type: u4
      - id: file_name
        size: entry_size - 0x1C

  encryption_data:
    seq:
      - id: md5_checksum
        size: 16
      - id: data_size
        type: u4
      - id: key
        type: u4
      - id: data
        size: _parent.header.encryption_data_size_decrypted - 24


instances:
  raw_header:
    pos: 0
    size: 68
  raw_data:
    pos: 72
    size: header.archive_data_size_decrypted + header.file_data_size_decrypted + header.encryption_data_size_decrypted
  raw_file_data:
    pos: header.archive_data_size_decrypted + header.file_data_size_decrypted + header.encryption_data_size_decrypted + 0x48
    size-eos: true

  
