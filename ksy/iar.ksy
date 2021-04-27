meta:
  id: iar
  title: iar file
  file-extension: iar
  endian: le

seq:
  - id: magic
    contents: "iar "
  - id: header
    type: header
  - id: entry_index_table
    type: u8
    repeat: expr
    repeat-expr: header.entry_count

types:
  header:
    seq:
      - id: major_version
        type: u2
      - id: minor_version
        type: u2
      - id: unk0
        type: u4
      - id: some_size
        type: u4
      - id: timestamp
        type: u4
      - id: unk3
        type: u4
      - id: entry_count
        type: u4
      - id: entry_count2
        type: u4
  file_entry:
    seq:
      - id: version
        type: u4
      - id: unk0
        type: u4
      - id: decompressed_file_size
        type: u4
      - id: unk2
        type: u4
      - id: file_size
        type: u4
      - id: unk3
        type: u4
      - id: unk4
        type: u4
      - id: unk5
        type: u4
      - id: width
        type: u4
      - id: height
        type: u4
      - id: unknown
        size: 32
  sub_image:
    seq:
      - id: parent_index
        type: u4
      - id: top
        type: u4
      - id: height
        type: u4
