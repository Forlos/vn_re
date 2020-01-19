meta:
  id: acv1
  title: ACV1 file
  file-extension: dat
  endian: le

seq:
  - id: magic
    contents: "ACV1"
  - id: count
    type: u4
    doc: |
      Number of entries XORed with master key
  - id: entries
    type: entry
    repeat: expr
    repeat-expr: entry_count
    doc: |
      Archive entries

types:
  entry:
    seq:
      - id: checksum
        type: u8
        doc: |
          Crc64 of file name
      - id: flags 
        type: u1
        doc: |
          Variable containing bit flags specifying
          XOR with hash[0] to decrypt
      - id: offset
        type: u4
        doc: |
          Offset of resource in archive file
          XOR with hash[0:4] then
          XOR with MASTER_KEY to decrypt
          if flags AND 2 == 1 then
          XOR with file_name[len(file_name) << 1]
      - id: size
        type: u4
        doc: |
          Size of compressed resource
          XOR with hash[0:4] to decrypt
          if flags AND 2 == 1 then
          XOR with file_name[len(file_name) << 2]
      - id: uncompressed_size
        type: u4
        doc: |
          Size of uncompressed resource
          XOR with hash[0:4] to decrypt
          if flags AND 2 == 1 then
          XOR with file_name[len(file_name) << 3]

instances:
  master_key:
    value: 0x8B6A4E5F
    doc: Key that is used to entry encryption
  script_key:
    value: 0x9D0BE0FA
    doc: Key that is used to decrypt scripts
  entry_count:
    value: count ^ master_key
    doc: XOR count with master key to get number of entries

enums:
  acv_flags:
    0: plain
    1: encrypted
    2: compressed
    4: text_file
