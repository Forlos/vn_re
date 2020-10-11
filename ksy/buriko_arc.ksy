meta:
  id: buriko_arc
  title: buriko arc file
  file-extension: arc
  endian: le

seq:
  - id: magic
    contents: "BURIKO ARC"
  - id: version
    type: str
    size: 2
    encoding: ascii
  - id: entry_count
    type: u4
  - id: file_entries
    type: file_entry
    repeat: expr
    repeat-expr: entry_count

types:
  file_entry:
    seq:
      - id: name
        size: 0x60
      - id: file_offset
        type: u4
      - id: file_size
        type: u4
      - id: unknown
        size: 0x18

instances:
  file_contents_offset:
    value: 0x10 + entry_count * 0x80
