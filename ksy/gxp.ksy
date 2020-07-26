meta:
  id: gxp
  title: gxp file
  file-extension: gxp
  endian: le

seq:
  - id: header
    type: header
  - id: file_entries
    size: header.file_entries_size

types:
  header:
    seq:
      - id: magic
        contents: "GXP\x00"
      - id: unk_04
        type: u4
      - id: unk_08
        type: u4
      - id: unk_0c
        type: u4
      - id: unk_10
        type: u4
      - id: unk_14
        type: u4
      - id: file_entries_count
        type: u4
      - id: file_entries_size
        type: u4
      - id: raw_file_data_size
        type: u4
      - id: unk_24
        type: u4
      - id: raw_file_data_offset
        type: u4
      - id: unk_2c
        type: u4

  file_entry:
    seq:
      - id: entry_size
        type: u4
      - id: file_size
        type: u4
      - id: unk_08
        type: u4
      - id: file_name_utf16_len
        type: u4
      - id: unk_10
        type: u4
      - id: unk_14
        type: u4
      - id: file_offset
        type: u4
      - id: unk_1c
        type: u4
      - id: file_name
        type: str
        size: entry_size - 0x20
        encoding: UTF-16LE

instances:
  raw_file_data:
    pos: header.raw_file_data_offset
    size: header.raw_file_data_size
