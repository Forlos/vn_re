meta:
  id: silky
  title: silky archive file
  file-extension: arc
  endian: le

seq:
  - id: entries_size
    type: u4
  - id: entries
    type: file_entries
    size: entries_size

types:
  file_entries:
    seq:
      - id: entries
        type: file_entry
        repeat: eos
  file_entry:
    seq:
      - id: name_length
        type: u1
      - id: name
        size: name_length
      - id: file_size
        type: u4
      - id: uncompressed_file_size
        type: u4
      - id: file_offset
        type: u4

instances:
  file_data_offset:
    value: entries_size + 4
