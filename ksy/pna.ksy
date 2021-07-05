meta:
  id: pna
  title: pna image file
  file-extension: pna
  endian: le

seq:
  - id: magic
    size: 4
  - id: data
    type:
      switch-on: magic
      cases:
        '[0x50, 0x4E, 0x41, 0x50]': pnap
        '[0x57, 0x50, 0x41, 0x50]': wpap
  - id: image_data
    size-eos: true

types:
  pnap:
    seq:
      - id: header
        type: pnap_header
      - id: entries
        type: pnap_entry
        repeat: expr
        repeat-expr: header.some_count
  pnap_header:
    seq:
      - id: unk0
        type: u4
      - id: unk1
        type: u4
      - id: unk2
        type: u4
      - id: some_count
        type: u4
  pnap_entry:
    seq:
      - id: type
        type: u4
      - id: id
        type: u4
      - id: left_offset
        type: u4
      - id: top_offset
        type: u4
      - id: width
        type: u4
      - id: height
        type: u4
      - id: unk0
        size: 12
      - id: size
        type: u4
  wpap:
    seq:
      - id: header
        type: wpap_header
      - id: entries
        type: wpap_entry
        repeat: expr
        repeat-expr: header.some_count
  wpap_header:
    seq:
      - id: unk0
        type: u4
      - id: unk1
        type: u4
      - id: unk2
        type: u4
      - id: some_count
        type: u4
  wpap_entry:
    seq:
      - id: type
        type: u4
      - id: id
        type: u4
      - id: left_offset
        type: u4
      - id: top_offset
        type: u4
      - id: width
        type: u4
      - id: height
        type: u4
      - id: unk0
        size: 12
      - id: size
        type: u4
