meta:
  id: pfs
  title: pfs file
  file-extension: pfs
  endian: le

seq:
  - id: magic
    contents: "pf8"
  - id: header
    type: header
  - id: entries
    type: file_entry
    repeat: expr
    repeat-expr: header.file_entries_count

types:
  header:
    seq:
      - id: archive_data_size
        type: u4
      - id: file_entries_count
        type: u4
  file_entry:
    seq:
      - id: file_name_size
        type: u4
      - id: file_name
        size: file_name_size
      - id: unk
        type: u4
      - id: file_offset
        type: u4
      - id: file_size
        type: u4

instances:
  raw_archive_data:
    pos: 7
    size: header.archive_data_size
