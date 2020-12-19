meta:
  id: esc_arc2
  title: esc_arc2 file
  file-extension: bin
  endian: le

seq:
  - id: magic
    contents: "ESC-ARC2"
  - id: unk0
    type: u4
  - id: file_count
    type: u4
  - id: unk2
    type: u4

types:
  file_entry:
    seq:
      - id: file_name_table_offset
        type: u4
      - id: file_offset
        type: u4
      - id: file_size
        type: u4

instances:
  key:
    value: 0x65AC9365
  file_entry_size:
    value: 12
