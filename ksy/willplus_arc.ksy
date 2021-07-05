meta:
  id: willplus_arc
  title: willplus arc archive file
  file-extension: arc
  endian: le

seq:
  - id: entries_count
    type: u4
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
      - id: file_size
        type: u4
      - id: file_offset
        type: u4
      # - id: file_name
      #   type: strz
      #   encoding: UTF-16LE

instances:
  file_data_offset:
    value: entries_size + 8
