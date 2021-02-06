meta:
  id: g00
  title: G00 image format
  file-extension: g00
  endian: le

seq:
  - id: version
    type: u1
  - id: width
    type: u2
  - id: height
    type: u2
  - id: header_count
    type: u4
    if: version == 2
  - id: headers
    type: headers
    size: header_count * 24
    if: version == 2
  - id: pixel_data
    type: pixel_data

types:
  headers:
    seq:
      - id: headers
        type: header
        repeat: eos
  header:
    seq:
      - id: left
        type: u4
      - id: top
        type: u4
      - id: right
        type: u4
      - id: bottom
        type: u4
      - id: unk4
        type: u4
      - id: unk5
        type: u4
  pixel_data:
    seq:
      - id: compressed_image_size
        type: u4
      - id: uncompressed_image_size
        type: u4
      - id: data
        size: compressed_image_size - 8
  sprite:
    seq:
      - id: unk0
        type: u2
      - id: chunk_count
        type: u2
      - id: a
        type: u4
      - id: b
        type: u4
      - id: width
        type: u4
      - id: height
        type: u4
      - id: unk6
        type: u4
      - id: unk7
        type: u4
      - id: full_width
        type: u4
      - id: full_height
        type: u4
  chunk:
    seq:
      # d
      - id: left
        type: u2
        # e
      - id: top
        type: u2
      - id: flag
        type: u2
        # f
      - id: width
        type: u2
        # g
      - id: height
        type: u2
