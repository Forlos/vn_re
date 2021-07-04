meta:
  id: crx
  title: crx file
  file-extension: crx
  endian: le

seq:
  - id: magic
    contents: "CRXG"
  - id: header
    type: header
  - id: color_table_with_alpha
    if: header.has_alpha == 0x102
    size: 0x400
  - id: color_table
    if: header.has_alpha == 0x101
    size: 0x300
  - id: headers_count
    type: u4
    if: header.unk2 > 2
  - id: headers
    type: headers
    size: headers_count * 16
    if: header.unk2 > 2
  - id: compressed_size
    type: u4
    if: (header.unk3 & 16) != 0
  - id: image_data
    size-eos: true
  # - id: image_data
  #   if: header.unk2 > 2
  #   size:  compressed_size

types:
  headers:
    seq:
      - id: headers
        type: secondary_header
        repeat: eos
  secondary_header:
    seq:
      - id: unk
        size: 16
  header:
    seq:
      - id: unk0
        type: u2
      - id: unk1
        type: u2
      - id: width
        type: u2
      - id: height
        type: u2
      - id: unk2
        type: u2
      - id: unk3
        type: u2
      - id: has_alpha
        type: u2
      - id: unk5
        type: u2
