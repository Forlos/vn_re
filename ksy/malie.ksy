meta:
  id: malie
  title: malie archive file
  file-extension: dat
  endian: le

seq:
  - id: header
    size: 16

types:
  header:
    seq:
      - id: magic
        contents: "LIBP"
      - id: file_entries_count
        type: u4
      - id: unk2
        type: u4
      - id: unk3
        type: u4
  file_entry:
    seq:
      - id: name
        type: str
        size: 22
        terminator: 0
        encoding: ascii
      - id: type
        type: u2
      - id: file_offset
        type: u4
      - id: file_size
        type: u4
