meta:
  id: ypf
  title: ypf file
  file-extension: ypf
  endian: le

seq:
  - id: magic
    contents: "YPF\0"
  - id: header
    type: header
  - id: entry_data
    size: header.entry_data_size

types:
  header:
    seq:
      - id: archive_version
        type: u4
      - id: entry_count
        type: u4
      - id: entry_data_size
        type: u4
      - id: padding
        size: 16
  file_entry:
    seq:
      - id: unk0
        type: u4
      - id: name_size
        type: u1
      - id: name
        size: name_size
      - id: unk1
        type: u1
      - id: flags
        type: u1
      - id: file_size
        type: u4
      - id: compressed_file_size
        type: u4
      - id: file_offset
        type: u8
      - id: unk7
        type: u4
